#!/usr/bin/env python

import netfilterqueue
import subprocess


def create_queue():
    # targetting
    # subprocess.call('iptables -I FORWARD -j NFQUEUE --queue-num 0', shell=True)
    # local
    subprocess.call('iptables -I OUTPUT -j NFQUEUE --queue-num 0', shell=True)
    subprocess.call('iptables -I INPUT -j NFQUEUE --queue-num 0', shell=True)


def remove_queue():
    subprocess.call('iptables --flush', shell=True)


def process_packet(packet):
    print(packet)
    packet.drop()


create_queue()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    print('\n[-] Detected CTRL + C ...... Resetting ip tables. Please wait ...')
    remove_queue()
