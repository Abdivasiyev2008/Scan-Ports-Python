#!/usr/bin/python3
import socket
import os
import re
from urllib.parse import urlparse
import colorama
from colorama import Fore
from libs.take_screenshot import take_screenshot
import paramiko
import smtplib
from ftplib import FTP
import nmap
import mysql.connector
import asyncio
import logging

paramiko.util.log_to_file('paramiko.log')

colorama.init(autoreset=True)

DEFAULT_CREDENTIALS = {
    'ftp': [{'username': 'anonymous', 'password': 'anonymous'}],
    'smtp': [{'username': 'user', 'password': 'password'}],
    'ssh': [
        {'username': 'root', 'password': 'root'},
        {'username': 'root', 'password': 'admin'},
        {'username': 'root', 'password': 'user'},
        {'username': 'root', 'password': 'niko'},
        {'username': 'root', 'password': 'guest'},
        {'username': 'root', 'password': 'password'},
        {'username': 'root', 'password': '1234'},

        {'username': 'user', 'password': 'root'},
        {'username': 'user', 'password': 'admin'},
        {'username': 'user', 'password': 'user'},
        {'username': 'user', 'password': 'niko'},
        {'username': 'user', 'password': 'guest'},
        {'username': 'user', 'password': 'password'},
        {'username': 'user', 'password': '1234'},

        {'username': 'niko', 'password': 'root'},
        {'username': 'niko', 'password': 'admin'},
        {'username': 'niko', 'password': 'user'},
        {'username': 'niko', 'password': 'niko'},
        {'username': 'niko', 'password': 'guest'},
        {'username': 'niko', 'password': 'password'},
        {'username': 'niko', 'password': '1234'},

        {'username': 'guest', 'password': 'root'},
        {'username': 'guest', 'password': 'admin'},
        {'username': 'guest', 'password': 'user'},
        {'username': 'guest', 'password': 'niko'},
        {'username': 'guest', 'password': 'guest'},
        {'username': 'guest', 'password': 'password'},
        {'username': 'guest', 'password': '1234'},

        {'username': 'admin', 'password': 'admin'},
        {'username': 'admin', 'password': 'user'},
        {'username': 'admin', 'password': 'niko'},
        {'username': 'admin', 'password': 'guest'},
        {'username': 'admin', 'password': 'password'},
        {'username': 'admin', 'password': 'root'},
        {'username': 'admin', 'password': '1234'},
    ],
    'mysql': [
        {'username': 'root', 'password': ''},
        {'username': 'root', 'password': 'mysql'},
        {'username': 'root', 'password': 'root'},
        {'username': 'root', 'password': 'password'},
        {'username': 'root', 'password': '1234'},
        {'username': 'root', 'password': 'mysql'},

        {'username': 'mysql', 'password': 'mysql'},
        {'username': 'mysql', 'password': 'root'},
        {'username': 'mysql', 'password': 'password'},
        {'username': 'mysql', 'password': '1234'},
        {'username': 'mysql', 'password': 'mysql'},
        {'username': 'mysql', 'password': 'admin'},

        {'username': 'admin', 'password': 'mysql'},
        {'username': 'admin', 'password': 'root'},
        {'username': 'admin', 'password': 'admin'},
        {'username': 'admin', 'password': 'password'},
        {'username': 'admin', 'password': '1234'},
        {'username': 'admin', 'password': 'mysql'},
    ],
}

def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Noma'lum xizmat"

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
        return "Banner yo'q"

async def perform_nmap_scan(hostname, port):
    try:
        nm = nmap.PortScanner()
        print(f"{hostname}:{port} manzilda SYN skanerlashni bajarish")
        nm.scan(hostname, str(port), arguments='-sS')
        if hostname in nm.all_hosts():
            print(f"SYN skanerlash natijasi: {nm[hostname]['tcp'][port]}")
        else:
            print(Fore.RED + f"{hostname} uchun natijalar topilmadi")
    except nmap.PortScannerError as e:
        print(Fore.RED + f"Nmap skanerlash xatosi: {e}")

async def check_default_credentials(hostname, port, service_name):
    if service_name == 'ftp':
        for cred in DEFAULT_CREDENTIALS['ftp']:
            print(Fore.YELLOW + f"FTP uchun tekshirilayotgan kredensialar: Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
            try:
                ftp = FTP()
                ftp.connect(hostname, port, timeout=5)
                ftp.login(user=cred['username'], passwd=cred['password'])
                print(
                    Fore.GREEN + f"FTP: Default kredensialar to'g'ri {hostname}:{port} - Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
                ftp.quit()
            except Exception:
                continue

    elif service_name == 'smtp':
        for cred in DEFAULT_CREDENTIALS['smtp']:
            print(Fore.YELLOW + f"SMTP uchun tekshirilayotgan kredensialar: Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
            try:
                server = smtplib.SMTP(hostname, port, timeout=5)
                server.login(cred['username'], cred['password'])
                print(
                    Fore.GREEN + f"SMTP: Default kredensialar to'g'ri {hostname}:{port} - Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
                server.quit()
            except Exception:
                continue

    elif service_name == 'ssh':
        for cred in DEFAULT_CREDENTIALS['ssh']:
            print(Fore.YELLOW + f"SSH uchun tekshirilayotgan kredensialar: Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname, port, username=cred['username'], password=cred['password'], timeout=5)
                print(
                    Fore.GREEN + f"SSH: Default kredensialar to'g'ri {hostname}:{port} - Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
                ssh.close()
            except Exception:
                continue

    elif service_name == 'mysql':
        for cred in DEFAULT_CREDENTIALS['mysql']:
            print(
                Fore.YELLOW + f"MySQL uchun tekshirilayotgan kredensialar: Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
            try:
                conn = mysql.connector.connect(host=hostname, port=port, user=cred['username'],
                                               password=cred['password'])
                if conn.is_connected():
                    print(
                        Fore.GREEN + f"MySQL: Default kredensialar to'g'ri {hostname}:{port} - Foydalanuvchi: {cred['username']}, Parol: {cred['password']}")
                    conn.close()
            except mysql.connector.Error:
                continue

async def scan_ports(target, start_port, end_port):
    # IP manzil yoki URLni aniqlash
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if ip_pattern.match(target):
        hostname = target
    else:
        parsed_url = urlparse(target)
        hostname = parsed_url.hostname

    if not hostname:
        print(Fore.RED + "Noto'g'ri hostname yoki IP manzil. Iltimos, maqsadni tekshiring.")
        return

    print(f"{hostname} manzilida {start_port}-{end_port} portlarini skanerlash...\n")

    # Portlar oralig'ida iteratsiya
    for port in range(start_port, end_port + 1):
        try:
            # Socket obyektini yaratamiz
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)  # Ulashuv urinish uchun vaqt chegarasini belgilaymiz

            # Belirtilgan portda xostga ulanishga harakat qilamiz
            result = sock.connect_ex((hostname, port))

            if result == 0:
                service_name = get_service_name(port)
                banner = banner_grab(hostname, port)

                print(Fore.GREEN + f"Port {port} OCHIQ")
                print(Fore.YELLOW + f"Xizmat: {service_name}")
                print(Fore.CYAN + f"Banner: {banner}")

                # Agar port web xizmatlariga tegishli bo'lmasa, screenshot olishni o'tkazib yuborish
                if port in []:
                    print(Fore.YELLOW + f"Web port bo'lmagan port uchun screenshot o'tkazib yuboriladi: {port}")
                else:
                    try:
                        # URL va katalogni yaratamiz
                        url = f'http://{hostname}:{port}'
                        directory = f'images/{hostname}'
                        if not os.path.exists(directory):
                            os.makedirs(directory)

                        screenshot_path = f'{directory}/{port}.png'

                        # Asinxron funksiyani ishga tushiramiz
                        await take_screenshot(url, screenshot_path)

                    except Exception as e:
                        # print(Fore.RED + f"Port {port} uchun screenshot olishda xato: {e}")
                        pass

                # Standart ma'lumotlarni tekshirish
                await check_default_credentials(hostname, port, service_name)

                # Nmap skanerlashni ishga tushiramiz
                await perform_nmap_scan(hostname, port)

            # Socketni yopamiz
            sock.close()
        except socket.error as e:
            print(Fore.RED + f"Port {port}ni skanerlashda xato: {e}")

