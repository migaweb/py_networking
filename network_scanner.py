#!/usr/bin/env python

import scapy.all as scapy
import argparse


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP / IP range.")
    options = parser.parse_args()
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    # broadcast MAC address
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    # SendReceive
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []

    for element in answered_list:
        clients_list.append({'ip': element[1].psrc, 'mac': element[1].hwsrc})

    return clients_list


def print_result(clients_list):
    print('IP\t\t\tMAC Address\n-------------------------------------')

    for client in clients_list:
        print(client['ip'] + '\t\t' + client['mac'])


options = get_arguments()
result_list = scan(options.target)
print_result(result_list)
