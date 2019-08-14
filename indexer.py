#!/usr/bin/env python3

import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from options import url, root


def get_links(url):
    page = requests.get(url)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')
    return {a['href'] for a in soup.select('a')}

def full_url_and_cat(url, href):
    '''
        return full_url, category
        cats are: subfolder, parent, outsite, query, other
    '''
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
        return url + href, 'other'

def is_file(url):
    if 'text/html' in requests.head(url).headers['Content-Type']:
        return False
    return True

def get_files(url, textfile):
    links = get_links(url)
    for link in links:
        full, cat = full_url_and_cat(url, link)
        if cat == 'subfolder':
            get_files(full, textfile)
        elif cat == 'other':
            print(full)
            textfile.write(full+'\n')

with open('links.txt', 'w') as textfile:
    get_files(url, textfile)
