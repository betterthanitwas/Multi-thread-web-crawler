from threading import Thread, Lock
from queue import Queue
from urllib.parse import urlparse

class UrlQueue:
    def __init__(self, start_crawler_thread):
        self.start_crawler_thread = start_crawler_thread
        self.queues = {}
        self.lock = Lock()
        self.visited_link = set()

    def add_url(self, url):
        with self.lock:
            if url not in self.visited_link:
                sef.visited_link = set.add(url)
                domain = urlparse(url).hostname
                if not domain in self.queues:
                    self.queues[domain] = Queue()
                    Thread(None, self.start_crawler_thread, domain, (domain)).start()
                self.queues[domain].put(url)

    # Returns either a URL or None. If it returns None, the calling thread should terminate.
    def take_url(self, domain):
        with self.lock:
            if self.queues[domain].empty(): 
                del self.queues[domain]
                return None
            else:
                return self.queues[domain].get()
