#!/usr/bin/python3
from urllib.parse import urlparse
from colorama import Fore
from libs.scan_port import scan_ports
import argparse, asyncio, re

def main():
    parser = argparse.ArgumentParser(description="Kengaytirilgan port skaner.")
    parser.add_argument('target', type=str, help='Skanerlanadigan URL yoki IP manzil.')
    parser.add_argument('--start', type=int, default=1, help='Skanerlanadigan portlar uchun boshlang\'ich port raqami.')
    parser.add_argument('--end', type=int, default=65535, help='Skanerlanadigan portlar uchun tugash port raqami.')

    args = parser.parse_args()
    target = args.target

    # IP manzil yoki URLni aniqlash
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if ip_pattern.match(target):
        # Target is an IP address
        hostname = target
    else:
        # Target is a URL
        parsed_url = urlparse(target)
        if not parsed_url.scheme:
            # If no scheme, add http://
            target = 'http://' + target
            parsed_url = urlparse(target)
        if parsed_url.scheme not in ['http', 'https']:
            print(Fore.RED + "URLning noto'g'ri protokoli. Iltimos, http:// yoki https:// ishlating.")
            return
        hostname = parsed_url.hostname
        if not hostname:
            print(Fore.RED + "Noto'g'ri hostname. Iltimos, URLni tekshiring.")
            return

    # Hostname yoki IP manzilni chop etamiz
    print(Fore.GREEN + f"Target hostname/IP: {hostname}")
    try:
        # Asinxron skanerlashni ishga tushiramiz
        asyncio.run(scan_ports("https://"+hostname, args.start, args.end))

    except:
        asyncio.run(scan_ports(hostname, args.start, args.end))

if __name__ == "__main__":
    main()
