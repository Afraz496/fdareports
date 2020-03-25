import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

for i in range(0,60):
    fdapage = requests.get("https://www.fda.gov/news-events/fda-newsroom/press-announcements?page=" + str(i))
    page = requests.get("https://www.fda.gov/news-events/press-announcements/fda-approves-first-treatment-group-progressive-interstitial-lung-diseases")

    soup = BeautifulSoup(fdapage.content,'lxml')
    urls = set()

    for i in soup.find_all('a',href=re.compile(r'(?<=approves).*')):
        url = i.get('href')
        abs_url = urljoin(fdapage.url, url)
        urls.add(abs_url)
        if urls is not set():
            print(urls)
