#!/usr/bin/env python
import requests

target_url = 'http://10.0.2.5/dvwa/login.php'
data = {'username': 'admin', 'password': 'password', 'Login': 'submit'}

response = requests.post(target_url, data=data)
print(response.content)
