from bs4 import BeautifulSoup
import time

import requests
import urllib.robotparser
from urllib.parse import urljoin, urldefrag, urlparse
from urlqueue import UrlQueue
from datastore import DataStore
import indexer
from threading import BoundedSemaphore
from datetime import datetime
from functools import lru_cache

thread_count = 64

data_store = DataStore('config.ini')

def fetch(url, **kwargs):
    try:
        return requests.get(url, headers={"User-Agent": "CLocKPJWaRPbot/1.0; (+https://clockpjwarp.com/)"}, **kwargs)
    except:
        return requests.get(url, headers={"User-Agent": "CLocKPJWaRPbot/1.0; (+https://clockpjwarp.com/)"}, **kwargs)

@lru_cache(1024 * thread_count)
def get_robots(domain):
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(fetch(f"http://{domain}/robots.txt").text.splitlines())
    return rp

def crawler_thread(thread_id):
    while True:
        time.sleep(.5)
        url = queue.take_url(thread_id)
        if url != None and get_robots(urlparse(url).hostname).can_fetch("CLocKPJWaRPbot", url):
            r  = fetch(url, allow_redirects=False)
            content_type = r.headers["Content-Type"].lower().partition(";")[0] if "Content-Type" in r.headers else "text/plain"
            print(f"{datetime.now()} {thread_id:02d} {r.status_code} {url} {content_type}")
            if r.status_code == 200 and (content_type.startswith("text/") or content_type in {"application/xhtml+xml", "application/xml"}):
                soup = BeautifulSoup(r.text, features="html.parser")
                del r # Benchmarking shows that allowing early collection of these values saves significant amounts of RAM
                for non_text in soup.find_all(['script', 'style']):
                    non_text.decompose()
                title = soup.title.string if soup.title and soup.title.string else url
                words = indexer.index_text(soup.get_text())
                for link in soup.find_all('a'):
                    next_link = link.get('href')
                    if next_link != None:
                        queue.add_url(urldefrag(urljoin(url, next_link)).url)
                del soup
                data_store.indexPage(url, title, words)
                del title, words
            elif r.status_code in {301, 302, 303, 307, 308}:
                queue.add_url(urldefrag(urljoin(url, r.headers["Location"])).url)

queue = UrlQueue(crawler_thread, thread_count)
queue.add_url("https://en.wikipedia.org/wiki/Main_Page")
queue.add_url("https://stackoverflow.com/")
queue.add_url("http://people.nnu.edu/blmyers/")

while True:
    time.sleep(60)
    print(queue.get_log_stats())
