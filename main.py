#!/usr/bin/python3
from urllib.parse import urlparse
from colorama import Fore
from libs.scan_port import scan_ports
import argparse, asyncio


def main():
    parser = argparse.ArgumentParser(description="Kengaytirilgan port skaner.")
    parser.add_argument('target', type=str, help='Skanerlanadigan URL yoki IP manzil.')
    parser.add_argument('--start', type=int, default=1, help='Skanerlanadigan portlar uchun boshlang\'ich port raqami.')
    parser.add_argument('--end', type=int, default=65535, help='Skanerlanadigan portlar uchun tugash port raqami.')

    args = parser.parse_args()

    parsed_url = urlparse(args.target)
    hostname = parsed_url.hostname

    if not hostname:
        print(Fore.RED + "Invalid hostname. Please check the URL.")
        return

    asyncio.run(scan_ports(args.target, args.start, args.end))


if __name__ == "__main__":
    main()
