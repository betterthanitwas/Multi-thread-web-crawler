from bs4 import BeautifulSoup
import time

import requests
import urllib.robotparser
from urllib.parse import urljoin, urldefrag
from urlqueue import UrlQueue
from datastore import DataStore
import indexer
from threading import BoundedSemaphore

data_store = DataStore('config.ini')

def fetch(url, **kwargs):
    try:
        return requests.get(url, headers={"User-Agent": "CLocKPJWaRPbot/1.0; (+https://clockpjwarp.com/)"}, **kwargs)
    except:
        return requests.get(url, headers={"User-Agent": "CLocKPJWaRPbot/1.0; (+https://clockpjwarp.com/)"}, **kwargs)

concurrency_limit = BoundedSemaphore(20)

def crawler_thread(domain):
    rp = urllib.robotparser.RobotFileParser()
    rp.parse(fetch(f"http://{domain}/robots.txt").text.splitlines())
    url = "start"
    while url != None:
        time.sleep(.5)
        with concurrency_limit:
            url = queue.take_url(domain)
            if url != None and rp.can_fetch("*", url):
                print(url)
                r  = fetch(url, allow_redirects=False)
                content_type = r.headers["Content-Type"].lower() if "Content-Type" in r.headers else "text/plain"
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
                            if rp.can_fetch("CLocKPJWaRPbot", next_link):
                                queue.add_url(urldefrag(urljoin(url, next_link)).url)
                    del soup
                    data_store.indexPage(url, title, words)
                    del title, words
                elif r.status_code in {301, 302, 303, 307, 308}:
                    queue.add_url(urldefrag(urljoin(url, r.headers["Location"])).url)

queue = UrlQueue(crawler_thread)
queue.add_url("https://en.wikipedia.org/wiki/Main_Page")
queue.add_url("https://stackoverflow.com/")
queue.add_url("http://people.nnu.edu/blmyers/")
