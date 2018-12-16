from threading import Thread, Lock
from queue import Queue
from urllib.parse import urlparse

class UrlQueue:
    def __init__(self, start_crawler_thread, thread_count):
        self.thread_count = thread_count
        self.queues = [Queue() for _ in range(thread_count)]
        self.lock = Lock()
        self.visited_links = set()
        for i in range(thread_count):
            Thread(None, start_crawler_thread, f"crawler {i}", (i,)).start()

    def add_url(self, url):
        with self.lock:
            if url not in self.visited_links:
                self.visited_links.add(url)
            else:
                return
        thread_id = hash(urlparse(url).hostname) % self.thread_count
        self.queues[thread_id].put(url)

    def take_url(self, thread_id):
        return self.queues[thread_id].get(True)
