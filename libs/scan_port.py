import socket
import os
from urllib.parse import urlparse
import colorama
from colorama import Fore
from libs.take_screenshot import take_screenshot
import paramiko
import smtplib
from ftplib import FTP

colorama.init(autoreset=True)

DEFAULT_CREDENTIALS = {
    'ftp': [{'username': 'anonymous', 'password': 'anonymous'}],
    'smtp': [{'username': 'user', 'password': 'password'}],
    'ssh': [{'username': 'root', 'password': 'root'}, {'username': 'admin', 'password': 'admin'}],
}

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown service"

def banner_grab(hostname, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock.connect((hostname, port))
        sock.send(b'HEAD / HTTP/1.1\r\nHost: %s\r\n\r\n' % hostname.encode())
        banner = sock.recv(1024).decode().strip()
        sock.close()
        return banner
    except:
        return "No banner"

async def check_default_credentials(hostname, port, service_name):
    if service_name == 'ftp':
        for cred in DEFAULT_CREDENTIALS['ftp']:
            try:
                ftp = FTP()
                ftp.connect(hostname, port, timeout=5)
                ftp.login(user=cred['username'], passwd=cred['password'])
                print(Fore.GREEN + f"FTP: Default credentials correct for {hostname}:{port} - Username: {cred['username']}, Password: {cred['password']}")
                ftp.quit()
                return True
            except Exception:
                continue
        print(Fore.RED + f"FTP: Default credentials incorrect for {hostname}:{port}")

    elif service_name == 'smtp':
        for cred in DEFAULT_CREDENTIALS['smtp']:
            try:
                server = smtplib.SMTP(hostname, port, timeout=5)
                server.login(cred['username'], cred['password'])
                print(Fore.GREEN + f"SMTP: Default credentials correct for {hostname}:{port} - Username: {cred['username']}, Password: {cred['password']}")
                server.quit()
                return True
            except Exception:
                continue
        print(Fore.RED + f"SMTP: Default credentials incorrect for {hostname}:{port}")

    elif service_name == 'ssh':
        for cred in DEFAULT_CREDENTIALS['ssh']:
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, port, username=cred['username'], password=cred['password'], timeout=5)
                print(Fore.GREEN + f"SSH: Default credentials correct for {hostname}:{port} - Username: {cred['username']}, Password: {cred['password']}")
                ssh.close()
                return True
            except Exception:
                continue
        print(Fore.RED + f"SSH: Default credentials incorrect for {hostname}:{port}")

async def scan_ports(url, start_port, end_port):
    # Parse the URL to extract the hostname
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if not hostname:
        print(Fore.RED + "Invalid hostname. Please check the URL.")
        return

    print(f"Scanning ports {start_port}-{end_port} on {hostname}...\n")

    # Iterate over the range of ports
    for port in range(start_port, end_port + 1):
        try:
            # Create a socket object
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Set a timeout for the connection attempt

            # Attempt to connect to the host on the specified port
            result = sock.connect_ex((hostname, port))

            if result == 0:
                service_name = get_service_name(port)
                banner = banner_grab(hostname, port)

                print(Fore.GREEN + f"Port {port} OPEN")
                print(Fore.YELLOW + f"Service: {service_name}")
                print(Fore.CYAN + f"Banner: {banner}")

                try:
                    # Create URL and directory
                    url = f'http://{hostname}:{port}'
                    if not url.startswith(('http://', 'https://')):
                        url = f'http://{hostname}:{port}'

                    directory = f'images/{hostname}'
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    screenshot_path = f'{directory}/{port}.png'

                    # Run the asynchronous function
                    await take_screenshot(url, screenshot_path)

                except Exception as e:
                    print(Fore.RED + f"Error taking screenshot for port {port} on {hostname}: {e}")

                # Check for default credentials
                await check_default_credentials(hostname, port, service_name)

            # Close the socket
            sock.close()
        except socket.error as e:
            print(Fore.RED + f"Error scanning port {port}: {e}")
