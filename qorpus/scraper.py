from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse

class QorpusScraper(object):
    def __init__(self, spider=None, strip_fn=None, urls=[], async=False):
        self.spider = spider
        self.urls = (u for u in urls) if urls else []
        self.strip_fn = strip_fn
        self.async = async

    def run(self):
        #Decide generator function
        if not self.spider:
            gtr = self.urls
        else:
            gtr = self.spider.run()

        for ln in gtr:
            if self.async:
                yield self.strip_fn.delay(BeautifulSoup(self.spider.urlopen(ln)))
            else:
                doc = BeautifulSoup(self.spider.urlopen(ln))
                yield self.strip_fn(doc)


class QorpusSpider(object):
    def __init__(self, start, base=None, strategies=[]):
        self.start = start
        self.base = base if base else "%s://%s/" % (urlparse(self.start).scheme, urlparse(self.start).netloc)
        self.strategies = strategies

    def add_strategies(self, *strategies):
        for strat in strategies:
            self.strategies.append(strat)

    def urlopen(self, ln):
        try:
            doc = urlopen(ln)
        except ValueError:
            try:
                doc = urlopen(self.base + ln)
            except ValueError:
                doc = ''
        return doc

    def run(self, url=None, depth=0):
        url = url['url'] if url else self.start
        doc = BeautifulSoup(self.urlopen(url))
        if self.strategies:
            strategy = self.strategies[depth]
            urls = strategy(doc)
            if depth == len(self.strategies)-1:
                for url in urls:
                    yield url
            else:
                for url in urls:
                    for u in self.run(url, depth+1):
                        yield u
