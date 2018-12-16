from threading import Thread, Lock
from queue import Queue
from urllib.parse import urlparse

class UrlQueue:
    def __init__(self, start_crawler_thread, thread_count):
        self.thread_count = thread_count
        self.queues = [Queue() for _ in range(thread_count)]
        self.lock = Lock()
        self.seen_urls = set()
        for i in range(thread_count):
            Thread(None, start_crawler_thread, f"crawler {i}", (i,)).start()

    def add_url(self, url):
        with self.lock:
            if url not in self.seen_urls:
                self.seen_urls.add(url)
            else:
                return
        thread_id = hash(urlparse(url).hostname) % self.thread_count
        self.queues[thread_id].put(url)

    def take_url(self, thread_id):
        return self.queues[thread_id].get(True)

    def get_log_stats(self):
        with self.lock:
            seen_url_count = len(self.seen_urls)
        return f"Seen {seen_url_count} urls, queue lengths {[queue.qsize() for queue in self.queues]}"
