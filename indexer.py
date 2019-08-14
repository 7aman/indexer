#!/usr/bin/env python3

import json
from urllib.parse import urlparse
from time import sleep
import requests
from bs4 import BeautifulSoup
from options import url, root


session = requests.Session()


def human_readable(size):
    size = int(size)
    for unit in ['', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            return "{:03.2f} {}B".format(size, unit)
        size = size / 1024.0

def get_links(url):
    MAXDELAY = 32
    gotit = False
    delay = 1
    while not gotit:
        try:
            page = session.get(url)
            gotit = True
        except Exception as e:
            print(e)
            print('sleeping...')
            sleep(delay)
            delay = max(MAXDELAY, 2*delay)
    page.encoding = 'utf-8'
    soup = BeautifulSoup(page.text, 'html.parser')
    return {a['href'] for a in soup.select('a')}

def get_headers(url):
    MAXDELAY = 32
    gotit = False
    delay = 1
    while not gotit:
        try:
            headers = session.head(url).headers
            gotit = True
        except Exception as e:
            print(e)
            print('sleeping...')
            sleep(delay)
            delay = max(MAXDELAY, 2*delay)
    if not headers.__contains__('Content-Type'):
        headers['Content-Type'] = 'Null'
    if not headers.__contains__('Content-Length'):
            headers['Content-Length'] = '0'
    return headers

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
    headers = get_headers(url)
    if 'text/html' in headers['Content-Type']:
        return False
    return True

def get_files(url, db):
    links = get_links(url)
    for link in links:
        full, cat = full_url_and_cat(url, link)
        if cat == 'subfolder':
            get_files(full, db)
        elif cat == 'other':
            headers = get_headers(full)
            db['files'].append(
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

db = dict()
db['root'] = url
db['files'] = list()
try:
    db = get_files(url, db)
except Exception as e:
    print(e)
    print('terminated with error!')
    pass
links = [item['url']+'\n' for item in db['files']]
print(human_readable(sum([int(item['size']) for item in db['files']])))
with open('db.json', 'w') as dbjson:
    json.dump(db, dbjson, indent=2)
with open('links.txt', 'w') as textfile:
    textfile.writelines(links)

print('\a')