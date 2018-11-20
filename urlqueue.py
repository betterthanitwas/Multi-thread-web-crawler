from threading import Thread, Lock
from queue import Queue
from urllib.parse import urlparse

# TODO this should be a function that takes a domain and a UrlQueue and starts crawling that domain
crawlerThread = None

class UrlQueue:
    def __init__(self):
        self.queues = {}
        self.lock = Lock()

    def addUrl(self, url):
        with self.lock:
            domain = urlparse(url).hostname
            if not domain in self.queues:
                self.queues[domain] = Queue()
                Thread(None, crawlerThread, domain, (domain, self)).start()
            self.queues[domain].put(url)

    # Returns either a URL or None. If it returns None, the calling thread should terminate.
    def takeUrl(self, domain):
        with self.lock:
            if self.queues[domain].empty(): 
                del self.queues[domain]
                return None
            else:
                return self.queues[domain].get()
