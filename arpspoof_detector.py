#!/usr/bin/env python
import argparse
import scapy.all as scapy


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface")
    options = parser.parse_args()
    return options


def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    # broadcast MAC address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    # SendReceive
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc


def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_package)
    # Do not store packets in mem.


def process_sniffed_package(packet):
    if packet.hasLayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac = get_mac(packet[scapy.ARP].psrc)
            response_mac = packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print('[+] You are under attack!')
        except IndexError:
            pass


sniff(get_arguments().interface)
