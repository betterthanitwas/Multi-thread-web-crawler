from bs4 import BeautifulSoup
import time

import requests
import urllib.robotparser
from urllib.parse import urljoin, urldefrag
from urlqueue import UrlQueue
from datastore import DataStore
import indexer

data_store = DataStore('localhost', 'webcrawl', 'root', '')

def crawler_thread(domain):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url((f"http://{domain}/robots.txt"))
    rp.read()
    url = "start"
    while url != None:
        time.sleep(.5)
        url = queue.take_url(domain)
        if url != None and rp.can_fetch("*", url):
            r  = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, features="html.parser")
            title = soup.title.string if soup.title else url
            words = indexer.index_text(soup.get_text())
            data_store.indexPage(url, title, words)
            for link in soup.find_all('a'):
                next_link = link.get('href')
                if next_link != None:
                    if rp.can_fetch("*", next_link):
                        queue.add_url(urldefrag(urljoin(url, next_link)).url)

queue = UrlQueue(crawler_thread)
queue.add_url("https://en.wikipedia.org/wiki/Main_Page")
queue.add_url("https://stackoverflow.com/")
queue.add_url("http://people.nnu.edu/blmyers/")
