from bs4 import BeautifulSoup

import requests
import urllib.robotparser
from rlqueue import UrlQueue
queue = UrlQueue

def crawler_thread(domain):
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url((domain+ "/robots.txt"))
    rp.read()
    url = "start"
    while url != None:
        url = queue.take_url(domain)
        if url != None and rp.can_fetch("*", url):
            r  = requests.get(url)
            data = r.text
            soup = BeautifulSoup(data, features="html.parser")
            title = soup.title.string
            for link in soup.find_all('a'):
                next_link = link.get('href')
                if next_link != None
                    if rp.can_fetch("*", next_link):
                        queue.add_url(next_link)
