"""
Main API
"""

from __future__ import absolute_import

import re
import logging
import json
import pickle

import redis
import trie

from urllib.request import urlopen
from bs4 import BeautifulSoup

from scraper import QorpusScraper, QorpusSpider
from cel.tasks import crawl_link, stripper

START_URL = 'http://ohhla.com/favorite.html'
ROOT = 'http://ohhla.com/'
REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)


logging.basicConfig(filename='logs/scraper.log')
LOGGER = logging.getLogger('scraperLog')


def qorpus_scrape():
    def strat_1(doc):
        return [{ 'url': lk.get('href')}
                for lk in doc.find_all('a') if lk.get('href') and re.search("^YFA(.*)", lk.get('href'))]

    def strat_2(doc):
        return [{ 'url': lk.get('href') }
                for lk in doc.find_all('a') if lk.get('href') and re.search("\.txt$", lk.get('href'))]

    spider = QorpusSpider(START_URL)
    spider.add_strategies(strat_1, strat_2)
    scrp = QorpusScraper(spider=spider, strip_fn=stripper, async=True)
    for txt in scrp.run():
        REDIS.append(name, txt)

def scrape_all():
    doc = BeautifulSoup(urlopen(START_URL))
    to_crawl = [(lk.text, lk.get('href')) for lk in doc.find_all('a')
                if lk.get('href') and re.search("^YFA(.*)", lk.get('href'))]

    #Spawn celery process
    for cl in to_crawl:
        crawl_link.delay(cl)


def build_tries():
    for key in REDIS.keys():
        artist = key.decode()
        try:
            ly = REDIS.get(key).decode()
        except:
            print("Ignoring", key)
            pass

        my_trie = trie.Trie()
        words = [word.strip().lower() for word in re.findall (r'\w+', ly)]
                    #Parse only words, ignoring punctuation and spaces

        for word in words:
            if my_trie.lookup(word) == None:
                my_trie.add(word, 1) # if word not contained in trie, add it
            else:
                #print "found word ", word, " again"
                my_trie.add(word,my_trie.lookup(word) + 1) #Otherwise increment its frequency value

        #Post to MongoDB
        from pymongo import MongoClient
        client = MongoClient()
        db = client.tries_db
        collection = db.main_collection
        print ("Inserting ", artist)
        entry = pickle.dumps(my_trie)
        to_insert = { 'artist': artist, 'trie': entry }
        collection.insert(to_insert)


if __name__ == '__main__':
    build_tries()
