"""
Main API
"""

from __future__ import absolute_import

import os
import re
import logging

import docx

from multiprocessing import Pool, cpu_count
from urllib.request import urlopen
from bs4 import BeautifulSoup

from constants import *
from cel.tasks import crawl_link

BASE_URL = 'http://ohhla.com/favorite.html'
ROOT = 'http://ohhla.com/'

logging.basicConfig(filename='logs/scraper.log')
LOGGER = logging.getLogger('scraperLog')

class Qorpus(object):
    def __init__(self, name=None, raw_text=None, filepath=None):
        self.name = name
        if filepath:
            _, extension = os.path.splitext(filepath)
            if extension not in ALLOWED_EXTENSIONS:
                raise ValueError('Extension %s is not supported by Qorpus. Allowed extensions are %s'
                        % (extension, ALLOWED_EXTENSIONS) )

            if extension in PYTHON_DOCX_EXTENSIONS:
                try:
                    self.document = docx.Document(filepath)
                except Exception as e:
                    print ("Python-docx failed to open document : %s" % e)

        self.raw_text = raw_text if raw_text else ''

    @classmethod
    def concat_all(cls, qs, name=None):
        acc = ''
        for q in qs:
            acc.join(q.raw_text)
        return Qorpus(name=name, raw_text=acc)

    def add_raw_text(self, txt):
        self.raw_text = self.raw_text.join(txt)

def scrape_all():
    doc = BeautifulSoup(urlopen(BASE_URL))
    to_crawl = [(lk.text, lk.get('href')) for lk in doc.find_all('a')
                if lk.get('href') and re.search("^YFA(.*)", lk.get('href'))]

    #Spawn celery process
    for cl in to_crawl:
        crawl_link.delay(cl)

if __name__ == '__main__':
    scrape_all()
