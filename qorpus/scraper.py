from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse

class QorpusScraper(object):
    def __init__(self, spider=None, strip_fn=None):
        self.spider = spider
        self.strip_fn = strip_fn

    def run(self):
        #if isinstance(self.strip_fn, app.task):
        #    for ln in self.spider.run():
        #        yield self.strip_fn.delay(urlopen(ln))
        #else:
        for ln in self.spider.run():
            doc = BeautifulSoup(self.spider.urlopen(ln))
            #try:
            #    doc = urlopen(ln)
            #except ValueError:
            #    doc = urlopen(self.spider.base + ln)
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
        url = url if url else self.start
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
