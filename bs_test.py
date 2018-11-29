from bs4 import BeautifulSoup

import requests
import urllib.robotparser




url = input("Enter a website to extract the URL's from: ")
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data, features="html.parser")
word_dic = {}
links = []
title = soup.title.string

print(title)
print(url)
rp = urllib.robotparser.RobotFileParser()
rp.set_url((url + "/robots.txt"))
rp.read()
for link in soup.find_all('a'):
    next_link = link.get('href')
    if next_link != None:
        if rp.can_fetch("*", next_link):
            links.append(next_link)
            print(next_link)

#print(links)

