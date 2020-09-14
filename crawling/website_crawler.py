#!/usr/bin/env python
import requests


def request(url):
    try:
        return requests.get('http://' + url)
    except requests.exceptions.ConnectionError:
        pass


# http://10.0.2.5
target_url = '10.0.2.5/mutillidae'

with open('/crawling/files-and-dirs-wordlist.list', 'r') as wordlist_file:
    for line in wordlist_file:
        test_url = target_url + '/' + line.strip()
        response = request(test_url)
        if response:
            print('[+] Discovered URL -->' + test_url)
