import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.fda.gov/news-events/press-announcements/fda-approves-first-treatment-group-progressive-interstitial-lung-diseases")

soup = BeautifulSoup(page.content,'html.parser')

text = soup.find_all('p')

for t in text:
    print(t.text)
