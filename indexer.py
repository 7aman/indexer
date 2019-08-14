#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from options import url, root


def get_soup(url):
    page = requests.get(url)
    page.encoding = 'utf-8'
    return BeautifulSoup(page.text, 'html.parser')

def get_links(soup):
    return soup.select('a')

def get_full(url, link):
    if link['href'][0] == '/':
        url.split('/')
    else:
        return url + link['href']
def is_folder(link):
    if link['href'][-1] == '/':
        if link['href'][0] != '/':
            return True
    else:
        return False

def is_file(url):
    if 'text/html' in requests.head(url).headers['Content-Type']:
        return False
    return True
    
soup = get_soup(url)
links = get_links(soup)

for link in links:
    if is_folder(link):
        print('folder:')
        print(url + link['href'])
    elif is_file(url + link['href']):
        print('file:')
        print(url + link['href'])
    else:
        print('neither:')
        print(url + link['href'])