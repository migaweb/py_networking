#!/usr/bin/env python
import requests


def request(url):
    try:
        return requests.get('http://' + url)
    except requests.exceptions.ConnectionError:
        pass


# http://10.0.2.5
target_url = 'google.com'

with open('/crawling/files-and-dirs-wordlist.list', 'r') as wordlist_file:
    for line in wordlist_file:
        test_url = line.strip() + '.' + target_url
        response = request(test_url)
        if response:
            print('[+] Discovered sub domain -->' + test_url)
