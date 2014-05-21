"""
Main API
"""

from __future__ import absolute_import

import re
import logging

from urllib.request import urlopen
from bs4 import BeautifulSoup

from scraper import QorpusScraper, QorpusSpider
from cel.tasks import crawl_link

START_URL = 'http://ohhla.com/favorite.html'
ROOT = 'http://ohhla.com/'

logging.basicConfig(filename='logs/scraper.log')
LOGGER = logging.getLogger('scraperLog')


def qorpus_scrape():
    def strat_1(doc):
        return [lk.get('href') for lk in doc.find_all('a') if lk.get('href') and re.search("^YFA(.*)", lk.get('href'))]


    def strat_2(doc):
        return [lk.get('href') for lk in doc.find_all('a')
                      if lk.get('href') and re.search("\.txt$", lk.get('href'))]

    spider = QorpusSpider(START_URL)
    spider.add_strategies(strat_1, strat_2)

    def stripper(doc):
        try:
            text_container = doc.pre if doc.pre else doc.body
        except AttributeError:
            text_container = doc

        txt = text_container.text
        for line in txt.split('\n'):
            if "Artist" in line:
                print (line)

        return clean_text(txt)

    scrp = QorpusScraper(spider, stripper)
    for txt in scrp.run():
        pass
        #print(txt)

def clean_text(txt):
    try:
        raw_lines = txt.split('\n')
        for line in list(raw_lines):
            if line.strip() == '' or line.isspace() or line.strip() == '[Chorus]':
                raw_lines.remove(line)
        return '\n'.join(raw_lines)
    except IOError:
        return ' '


def scrape_all():
    doc = BeautifulSoup(urlopen(START_URL))
    to_crawl = [(lk.text, lk.get('href')) for lk in doc.find_all('a')
                if lk.get('href') and re.search("^YFA(.*)", lk.get('href'))]

    #Spawn celery process
    for cl in to_crawl:
        crawl_link.delay(cl)

if __name__ == '__main__':
    qorpus_scrape()
