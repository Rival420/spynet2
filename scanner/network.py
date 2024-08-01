import ipaddress
import asyncio
from scapy.all import ARP, Ether, srp

async def scan_port(ip: str, port: int, semaphore: asyncio.Semaphore) -> bool:
    async with semaphore:
        try:
            _, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=1)
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError):
            return False
        except Exception as e:
            print(f"Error scanning port {port} on {ip}: {e}")
            return False

async def scan_ports(ip: str, ports: list, max_concurrency: int) -> dict:
    open_ports = []
    semaphore = asyncio.Semaphore(max_concurrency)
    tasks = [asyncio.create_task(scan_port(ip, port, semaphore)) for port in ports]

    for i, task in enumerate(tasks):
        result = await task
        if result:
            open_ports.append(ports[i])

    return {"ip": ip, "ports": open_ports}

def arp_scan(ip: str) -> bool:
    arp_req = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip)
    ans, _ = srp(arp_req, timeout=1, verbose=0)
    return len(ans) > 0

def get_ip_range(target_ip):
    """Calculate the IP range from the given target."""
    if "-" in target_ip:
        start_ip, end_ip = target_ip.split("-")
        ip_range = list(ipaddress.summarize_address_range(
            ipaddress.IPv4Address(start_ip.strip()), 
            ipaddress.IPv4Address(end_ip.strip())
        ))
    elif "/" in target_ip:
        network = ipaddress.IPv4Network(target_ip, strict=False)
        ip_range = [ip for ip in network.hosts()]  # Exclude network and broadcast addresses
    else:
        ip_range = [ipaddress.IPv4Address(target_ip)]

    return ip_range