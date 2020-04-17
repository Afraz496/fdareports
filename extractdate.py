import requests
from bs4 import BeautifulSoup
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import xlwt
from xlwt import Workbook

def extract_date(url):
    fdapage = requests.get(url)
    soup = BeautifulSoup(fdapage.content,'lxml')
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.find_all('p')


    #Extract company information
    try:
        if text_copy[len(text_copy) - 4] == "":
            approvalsentence = text_copy[len(text_copy) - 6%len(text_copy)].get_text()
        else:
            approvalsentence = text_copy[len(text_copy) - 5%len(text_copy)].get_text()
    except:
        text = soup.find_all("div")
        text_copy = text
        if text_copy[len(text_copy) - 4] == "":
            approvalsentence = text_copy[len(text_copy) - 6%len(text_copy)].get_text()
        else:
            approvalsentence = text_copy[len(text_copy) - 5%len(text_copy)].get_text()

    #find the date:
    date = ""
    try:
        date = soup.find("div", {"class": "release-date"}).find("div", {"class": "col-md-9"}).get_text()
    except:
        date_search = soup.find_all('strong')
        for i in range(0,len(date_search)):
            if date_search[i] == "<strong>For Immediate Release:</strong>" or date_search[i] == "<strong>For Immediate Release: </strong>":
                date = date_search[i].get_text()
    if date == "":
        date_search = soup.find_all('strong')
        for i in range(0,len(date_search)):
            print(date_search[i].get_text())
            print(date_search[i].next_sibling)
            if date_search[i].get_text() == "For Immediate Release:\n" or date_search[i].get_text() == "For Immediate Release: \n" or date_search[i] == "<strong>For Immediate Release:\n</strong>" or date_search[i] == "<strong>For Immediate Release: \n</strong>":
                print("Hello")

    print("The date is " + str(date))
    text_copy = text


extract_date("https://wayback.archive-it.org/7993/20170112023834/http://www.fda.gov/NewsEvents/Newsroom/PressAnnouncements/ucm396585.htm")
