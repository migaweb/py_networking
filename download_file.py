#!/usr/bin/env python
import requests
import subprocess


def download(url):
    get_response = requests.get(url)
    file_name = url.split('/')[-1]
    with open(file_name, 'wb', ) as out_file:
        out_file.write(get_response.content)


download('https://zsecurity.org/wp-content/uploads/2018/09/zs-top-left.png')