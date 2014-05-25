from __future__ import absolute_import

import re
from urllib.request import urlopen

import redis
from bs4 import BeautifulSoup

from cel.celery import app

REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)
ROOT = 'http://ohhla.com/'

@app.task
def crawl_link(cl):
    name, url = cl[0], cl[1]
    print ("Scraping ", name)
    for txt in scrape_txt_from_url(url):
        REDIS.append(name, txt)

@app.task
def stripper(doc):
    try:
        text_container = doc.pre if doc.pre else doc.body
    except AttributeError:
        text_container = doc

    txt = text_container.text
    return clean_text(txt)

def scrape_txt_from_url(url):
    d = BeautifulSoup(urlopen(ROOT + url))
    lyric_urls = [lk.get('href') for lk in d.find_all('a')
                  if lk.get('href') and re.search("\.txt$", lk.get('href'))]
    for lyric in lyric_urls:
        ly = BeautifulSoup(urlopen(ROOT + lyric))
        print ("Yielding", lyric)
        try:
            text_container = ly.pre if ly.pre else ly.body
        except AttributeError:
            text_container = ly
            print ("No Pre")

        yield clean_text(text_container.text)

def clean_text(txt):
    try:
        raw_lines = txt.split('\n')
        for line in list(raw_lines):
            if line.strip() == '' or line.isspace() or line.strip() == '[Chorus]':
                raw_lines.remove(line)
        return ' '.join(raw_lines) + ' '
    except IOError:
        return ' '
