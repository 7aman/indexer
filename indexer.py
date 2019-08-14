#!/usr/bin/env python3

import json
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from options import url, root

def human_readable(size):
    size = int(size)
    for unit in ['', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            return "{:03.2f} {}B".format(size, unit)
        size = size / 1024.0

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

def get_files(url, db):
    links = get_links(url)
    for link in links:
        full, cat = full_url_and_cat(url, link)
        if cat == 'subfolder':
            get_files(full, db)
        elif cat == 'other':
            headers = requests.head(full).headers
            if not headers.__contains__('Content-Type'):
                headers['Content-Type'] = 'Null'
            if not headers.__contains__('Content-Length'):
                    headers['Content-Type'] = '0'
            db.append(
                {
                    'url': full,
                    'type': headers['Content-Type'],
                    'size': headers['Content-Length'],
                    'hsize': human_readable(headers['Content-Length'])
                }
            )
        print('.', end='', flush=True)
    print()
    return db

db = list()
db = get_files(url, db)
links = [item['url']+'\n' for item in db]
print(human_readable(sum([int(item['size']) for item in db])))
with open('db.json', 'w') as dbjson:
    json.dump(db, dbjson, indent=2)
with open('links.txt', 'w') as textfile:
    textfile.writelines(links)
