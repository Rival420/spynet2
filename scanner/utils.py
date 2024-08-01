import netifaces
import ipaddress

def get_internal_network() -> str:
    gateways = netifaces.gateways()
    default_iface = gateways.get('default', {}).get(netifaces.AF_INET, [None])[1]
    if default_iface:
        iface_data = netifaces.ifaddresses(default_iface).get(netifaces.AF_INET, [{}])[0]
        addr = iface_data.get('addr')
        netmask = iface_data.get('netmask')
        if addr and netmask:
            network = ipaddress.IPv4Network(f"{addr}/{netmask}", strict=False)
            return str(network)
    return "127.0.0.1/32"
