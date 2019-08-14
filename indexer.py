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

def get_info(url, link):
    '''
        return full_url, category
        cats are: subfolder, parent, outsite, file, query
    '''
    href = link['href']
    o = urlparse(href)
    if o.scheme and o.netloc:
        return href, 'outsite'
    elif o.query:
        return url + href, 'query'
    elif href[0] == '/':
        b = urlparse(url)
        return f'{b.scheme}://{b.netloc}{href}', 'parent'
    elif href[-1] == '/':
        return url + href, 'subfolder'
    else:
        return url + href, 'file'

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
    print(get_full(url, link))
