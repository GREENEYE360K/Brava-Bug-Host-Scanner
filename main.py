import socket

import requests

import concurrent.futures

import sys

import os

from termcolor import colored


# Configuration

PORTS = [80, 443, 8080]  # Common ports to check

TIMEOUT = 2  # Timeout for socket connections

responsive_hosts = []  # Store responsive hosts


# Stylish welcome message


def display_welcome():

    print(
        colored(
            """  
    ██████╗ ██████╗  █████╗ ██╗   ██╗ █████╗ 
    ██╔══██╗██╔══██╗██╔══██╗██║   ██║██╔══██╗
    ██████╔╝██████╔╝███████║██║   ██║███████║
    ██╔═══╝ ██╔═══╝ ██╔══██║╚██╗ ██╔╝██╔══██║
    ██║     ██║     ██║  ██║ ╚████╔╝ ██║  ██║
    ╚═╝     ╚═╝     ╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝
                »»ᅳC-AVAᅳ►

            Bug Host Scanner v2.5 
               
                     """,
            "magenta",
        )
    )


# Ask user for file input


def get_hosts_file():

    file_name = input(colored("Enter hosts file name (e.g., hosts.txt): \n", "cyan"))

    if not os.path.isfile(file_name):

        print(colored(f"[-] File '{file_name}' not found. Exiting...", "red"))

        sys.exit(1)

    return file_name


# Load hosts from a file


def load_hosts(file_path):

    with open(file_path, "r") as file:

        hosts = [line.strip() for line in file if line.strip()]

        return hosts


# Check if a port is open


def scan_port(host, port):

    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.settimeout(TIMEOUT)

            s.connect((host, port))

            return True

    except (socket.timeout, ConnectionRefusedError):

        return False


# Identify CDN Provider


def detect_cdn(host):

    try:

        response = requests.get(f"http://{host}", timeout=TIMEOUT)

        headers = response.headers

        server_header = headers.get("Server", "").lower()

        via_header = headers.get("Via", "").lower()

        if "cloudflare" in server_header or "cloudflare" in via_header:

            return "Cloudflare"

        if "fastly" in server_header or "fastly" in via_header:

            return "Fastly"

        if "bunnycdn" in server_header or "bunnycdn" in via_header:

            return "BunnyCDN"

        if "cloudfront" in server_header or "cloudfront" in via_header:

            return "CloudFront"

        return "Unknown"

    except requests.RequestException:

        return "Unknown"


# Get HTTP Response Status


def get_http_response(host):

    try:

        response = requests.get(f"http://{host}", timeout=TIMEOUT)

        return response.status_code

    except requests.RequestException:

        return "N/A"


# Main scan function


def scan_target(host):

    open_ports = [port for port in PORTS if scan_port(host, port)]

    if open_ports:

        cdn_provider = detect_cdn(host)

        http_status = get_http_response(host)

        responsive_hosts.append(
            {
                "host": host,
                "ports": open_ports,
                "cdn": cdn_provider,
                "status": http_status,
            }
        )

        print(
            colored(f"[#] {host}\n", "dark_grey")
            + colored(f"Ports: {open_ports} | CDN: {cdn_provider}\n", "dark_grey")
            + colored(f"Status: {http_status}", "dark_grey")
        )

    else:

        print(colored(f"[!] {host} | No open ports found.", "red"))


# Final Results Summary


def display_summary(total_hosts):

    active_hosts = len(responsive_hosts)

    inactive_hosts = total_hosts - active_hosts

    print(colored("\n[+] Scan Completed!", "cyan"))

    print(colored(f"Total Hosts Scanned: {total_hosts}", "yellow"))

    print(colored(f"Active Hosts: {active_hosts}", "green"))

    print(colored(f"Inactive Hosts: {inactive_hosts}", "red"))

    if active_hosts > 0:

        print(colored("\n[+] Responsive Hosts:", "light_magenta"))

        for host in responsive_hosts:

            print(colored(f"{host['host']}", "green"))
            print(
                colored(
                    f"  Ports: {host['ports']} | CDN: {host['cdn']}",
                    "cyan",
                )
            )
            print(
                colored(
                    f"  Status: {host['status']}",
                    "cyan",
                )
            )


# Main

if __name__ == "__main__":

    display_welcome()

    hosts_file = get_hosts_file()

    targets = load_hosts(hosts_file)

    if not targets:

        print(colored("[-] No hosts found in the file. Exiting...", "red"))

        sys.exit(1)

    print(colored(f"[+] Loaded {len(targets)} hosts. Starting scan...\n", "cyan"))

    with concurrent.futures.ThreadPoolExecutor() as executor:

        executor.map(scan_target, targets)

    display_summary(len(targets))
