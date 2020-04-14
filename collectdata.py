import requests
from bs4 import BeautifulSoup
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def extract_text(soup, url):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.find_all('p')
    for i in range(3,len(text)):
        # break into lines and remove leading and trailing space on each
        textline = text[i].get_text()
        lines = (line.strip() for line in textline.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text[i] = '\n'.join(chunk for chunk in chunks if chunk)

    #find the date:
    date = text[len(text)-2]

    #Extract company information

    print("The date is " + str(date))
    if text[len(text) - 4] == "":
        approvalsentence = text[len(text) - 6]
        print(text[len(text)-6])
    else:
        approvalsentence = text[len(text) - 5]
        print(text[len(text)-5])

    #this code will definitely find the drug name, you need more control over sentence
    drugdiscoveryCriterion = re.compile(r'(?<=approval of )(.*?)(?= was | to )',re.M)
    drugname = drugdiscoveryCriterion.findall(approvalsentence)

    #---Exception handling when drug name not found------
    if drugname == [""]:
        return

    drugstringCondition = 'approval of ' + ' '.join(drugname) + ' to '
    regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
    pharmanameCriterion = re.compile(regexCondition,re.M)
    pharmaname = pharmanameCriterion.findall(approvalsentence)
    if pharmaname == [""]:
        drugstringCondition = 'approval of ' + ' '.join(drugname) + ' was granted to '
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(approvalsentence)
    #-----Debug Print Suite--------
    print(regexCondition)
    print(drugstringCondition)
    print("The approval sentence is " + str(approvalsentence))
    print("The name of the drug is " + str(drugname))
    print("The name of the pharmacy is " + str(pharmaname))


#---------------In this portion of the script we will be going over URLS over a certain period------------
#Gather all the urls
count = 0
for i in range(0,60):
    fdapage = requests.get("https://www.fda.gov/news-events/fda-newsroom/press-announcements?page=" + str(i))
    page = requests.get("https://www.fda.gov/news-events/press-announcements/fda-approves-first-treatment-group-progressive-interstitial-lung-diseases")

    soup = BeautifulSoup(fdapage.content,'lxml')
    urls = set()

    for i in soup.find_all('a',href=re.compile(r'(?<=approves).*')):
        url = i.get('href')
        abs_url = urljoin(fdapage.url, url)
        if urls is not set():
            temppage = requests.get(abs_url)
            tempsoup = BeautifulSoup(temppage.content,'lxml')
            extract_text(tempsoup,abs_url)
            urls.add(abs_url)
            count += 1

print(count)
#Extract the text in each URL and build the Text classification tool
