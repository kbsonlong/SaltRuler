import urllib2

import time

from threading import Thread

class GetUrlThread(Thread):
    def __init__(self, url):
        self.url = url

        super(GetUrlThread, self).__init__()


    def run(self):
        resp = urllib2.urlopen(self.url)

        print self.url, resp.getcode()


def get_responses():
    urls = [

        'http://www.google.com',

        'http://www.amazon.com',

        'http://www.ebay.com',

        'http://www.alibaba.com',

        'http://www.reddit.com'

    ]

    start = time.time()

    threads = []

    for url in urls:
        t = GetUrlThread(url)
        threads.append(t)
        t.start()


    for t in threads:
        t.join()

    print"Elapsed time: %s" % (time.time() - start)

get_responses()