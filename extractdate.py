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
    fdapage = fdapage.content
    soup = BeautifulSoup(fdapage,'lxml')
    # kill all script and style elements
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


    #-----Exception handling for the 2013-2014 data-------

    if date == "":
        #Clean out </br> tags
        for br in soup.find_all('br'):
            br.extract()
        try:
            date_search = soup.find_all("b")
            for i in range(0,len(date_search)):
                if date_search[i] == "<b>For Immediate Release:</b>" or date_search[i] == "<b>For Immediate Release: </b>":
                    date = date_search[i].get_text()
        except:
            pass

        try:
            date_search = soup.find_all("div")

            for i in range(0,len(date_search)):
                if date_search[i] == "<b>For Immediate Release:</b>" or date_search[i] == "<b>For Immediate Release: </b>":
                    date = date_search[i].next_sibling

            if date == "":
                date_search = soup.find("div", {"class": "main"}).find_all("div")
                date_search = str(date_search)

                date_writtenCriterion = re.compile(r'(?<=<div>For Immediate Release: )(.*?)(?=</div>)',re.M)
                date = date_writtenCriterion.findall(date_search)
                date = date[0]
                date = str(date)

            if date == "":
                date_search = soup.find_all("div").find_all("strong")
                for i in range(0,len(date_search)):
                    if date_search[i] == "<strong>For Immediate Release:</strong>" or date_search[i] == "<strong>For Immediate Release: </strong>":
                        date = date_search[i].get_text()

        except:
            pass
    if date == "":
        try:
            date_search = soup.find('strong')
            date = date_search.next_sibling
        except:
            pass
    if date == "":
        print(date_search)

    print("The date is " + str(date))


extract_date("https://wayback.archive-it.org/7993/20170112023900/http://www.fda.gov/NewsEvents/Newsroom/PressAnnouncements/ucm345528.htm")
