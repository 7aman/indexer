#!/usr/bin/env python3
import sys
import json
from urllib.parse import urlparse
from time import sleep
from pathlib import Path
import requests
from bs4 import BeautifulSoup

__version__ = '0.0.1'


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
    return db


def save_as_json(db):
    with open('db.json', 'w') as dbjson:
        json.dump(db, dbjson, indent=2)


def save_links(db):
    with open('links.txt', 'w') as textfile:
        links = [item['url']+'\n' for item in db['files']]
        textfile.writelines(links)


def save4aria(db):
    url = db['root']
    root = Path('.').joinpath('root')
    files = sorted(db['files'], key=lambda x: x['url'])
    with open('aria.list', 'w') as txtfile:
        for file in files:
            path_parts = file['url'].replace(url, '')  # remove base url
            path_parts = path_parts.replace('%20', ' ').split('/')
            path = root.joinpath(*path_parts)
            txtfile.write(f"{file['url']}\n")
            txtfile.write(f'  dir={path.parent}\n')
            txtfile.write(f'  out={path.name}\n')
            txtfile.write(f"# size: {file['hsize']}\n\n")


def print_info(db):
    sizes = [int(item['size']) for item in db['files']]
    total_size = human_readable(sum(sizes))
    print(f'Total number of files: {len(sizes)}')
    print(f'Estimated total size:  {total_size}')
    print(f'Largest file size:     {human_readable(max(sizes))}')
    print()
    print('\nUse "aria2c -i aria.list -c -j1 --file-allocation=none" to download files.\n')


def main():
    db = dict()
    url = sys.argv[1]
    if not url[-1] == '/':
        url += '/'
    db = {'root': url, 'files': []}
    try:
        db = get_files(url, db)
    except Exception as e:
        print(e)
        print('terminated with error!')
    finally:
        print()
    save_as_json(db)
    save_links(db)
    save4aria(db)
    print_info(db)


if __name__ == "__main__":
    main()
    print('\a')
