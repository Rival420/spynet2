import asyncio
import argparse
import logging
import time
from db import init_db, get_db
from models import Host, Port
from network import arp_scan, scan_ports, get_ip_range
from utils import get_internal_network
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy.orm import Session

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to INFO for less verbose logging
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def scan_host(ip, ports_range, max_concurrency):
    """Scan a single host and return the scan result."""
    logger.info(f"Scanning IP: {ip}")
    if arp_scan(str(ip)):
        logger.info(f"Host {ip} is alive. Scanning ports...")
        scan_result = await scan_ports(str(ip), ports_range, max_concurrency)
        if scan_result['ports']:
            logger.info(f"Host {ip} has open ports: {scan_result['ports']}")
        else:
            logger.info(f"Host {ip} has no open ports.")
        return {"ip": ip, "ports": scan_result['ports']}
    else:
        logger.info(f"Host {ip} is not alive.")
        return {"ip": ip, "ports": []}

def save_to_db(db: Session, host_data):
    """Save a single host's data to the database."""
    logger.info(f"Saving scan results for {host_data['ip']} to the database...")
    try:
        host = Host(ip=host_data['ip'])
        db.add(host)
        db.commit()
        logger.info(f"Added host {host.ip} to the database.")

        for port in host_data['ports']:
            port_entry = Port(port=port, host_id=host.id)
            db.add(port_entry)
        
        db.commit()
        logger.info(f"Scan results for {host_data['ip']} saved to the database.")
    
    except IntegrityError as e:
        logger.error(f"IntegrityError: Could not save data for {host_data['ip']} due to duplicate entry. Error: {e}")
        db.rollback()
    
    except Exception as e:
        logger.error(f"Unexpected error saving to the database for {host_data['ip']}: {e}")
        db.rollback()

async def main():
    parser = argparse.ArgumentParser(description='Spynet')
    parser.add_argument('-i', '--ip', default=get_internal_network(), help="Target IP or IP range (e.g., '192.168.1.1', '192.168.1.1-192.168.1.5' or '192.168.1.0/24')")
    parser.add_argument('-p', '--port', default='1-10000', help="Target port or port range (e.g., '80', '80-100' or 'all')")
    parser.add_argument('-c', '--concurrency', type=int, default=100, help="Max number of concurrent port scans")
    args = parser.parse_args()

    target_ip = args.ip
    target_ports = args.port
    max_concurrency = args.concurrency

    logger.info(f"Starting scan on IP range: {target_ip} with port range: {target_ports}")

    ip_range = get_ip_range(target_ip)
    logger.info(f"Number of IPs to scan: {len(ip_range)}")

    if target_ports.lower() == "all":
        ports_range = range(1, 65536)
    elif "-" in target_ports:
        start_port, end_port = target_ports.split("-")
        ports_range = range(int(start_port.strip()), int(end_port.strip()) + 1)
    else:
        ports_range = [int(target_ports)]

    logger.info(f"Number of ports to scan: {len(ports_range)}")

    retries = 10
    for i in range(retries):
        try:
            logger.info("Attempting to initialize the database...")
            init_db()  # No arguments needed here
            logger.info("Database initialized.")

            # Scan hosts dynamically
            db = next(get_db())
            for ip in ip_range:
                scan_result = await scan_host(str(ip), ports_range, max_concurrency)
                if scan_result['ports']:  # Only save hosts with open ports
                    save_to_db(db, scan_result)
                    logger.info(f"Results for host {scan_result['ip']} saved to database.")
            break

        except OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            logger.info(f"Retrying in 5 seconds ({i + 1}/{retries})...")
            time.sleep(5)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            break
    else:
        logger.error("Failed to connect to the database after several attempts.")

if __name__ == "__main__":
    asyncio.run(main())
