#!/usr/bin/env python
import requests
import re
import urlparse

target_url = 'http://10.0.2.5/mutillidae/'
target_links = []
max_rec = 2


def extract_links_from(url):
    response = requests.get(url)
    if response and response.status_code == 200:
        return re.findall('(?:href=")(.*?)"', response.content)
    else:
        return []


def crawl(url):
    href_links = extract_links_from(url)
    for link in href_links:
        link = urlparse.urljoin(url, link)

        if '#' in link:
            link = link.split('#')[0]

        if target_url in link and link not in target_links:
            target_links.append(link)
            print(link)
            crawl(link)


crawl(target_url)
