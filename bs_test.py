from bs4 import BeautifulSoup

import requests

url = input("Enter a website to extract the URL's from: ")
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data)




#print(soup.get_text("you"))

links = []

for link in soup.find_all('a'):
    links.append(link.get('href'))

print(links[7])
