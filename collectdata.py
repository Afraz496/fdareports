import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

fdapage = requests.get("https://www.fda.gov/news-events/fda-newsroom/press-announcements")
page = requests.get("https://www.fda.gov/news-events/press-announcements/fda-approves-first-treatment-group-progressive-interstitial-lung-diseases")

soup = BeautifulSoup(fdapage.content,'lxml')
urls = set()

for i in soup.find_all('a',href=re.compile(r'(?<=approves).*')):
    url = i.get('href')
    abs_url = urljoin(fdapage.url, url)
    urls.add(abs_url)
print(urls)

text = soup.find_all('p')

for t in text:
    print(t.text)
