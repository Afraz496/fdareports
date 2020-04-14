import requests
from bs4 import BeautifulSoup
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def clean_text(text):
    blankstr = ""
    for i in range(3,len(text)-2):
        blankstr += text[i].get_text()
    return blankstr

def extract_text(soup, url,count):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.find_all('p')
    #find the date:
    date = text[len(text)-2].get_text()
    text = clean_text(text)
    """
    #Extract company information
    if text[len(text) - 4] == "":
        approvalsentence = text[len(text) - 6]
        print(text[len(text)-6])
    else:
        approvalsentence = text[len(text) - 5]
        print(text[len(text)-5])
    """
    #this code will definitely find the drug name, you need more control over sentence
    drugdiscoveryCriterion = re.compile(r'(?<=The FDA granted approval of )(.*?)(?= was | to )',re.M)
    drugname = drugdiscoveryCriterion.findall(text)

    #---Exception handling when drug name not found------
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<= the approval of )(.*?)(?= was | to )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<= granted Priority Review of )(.*?)(?= was | to )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<=The approval of )(.*?)(?= was | to )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<=Approval of )(.*?)(?= was | were | to )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<= holds the application for )(.*?)(?=\.)',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<= approvals for the generic version of )(.*?)(?= to )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<= approvals of )(.*?)(?= to | were )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<= approvals for the )(.*?)(?= to | were )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r'(?<=The sponsor of the approved generic version of )(.*?)(?= is )',re.M)
        drugname = drugdiscoveryCriterion.findall(text)
    if drugname == []:
        drugdiscoveryCriterion = re.compile(r"(?<=Today's approval of the )(.*?)(?= was )",re.M)
        drugname = drugdiscoveryCriterion.findall(text)

    drugstringCondition = 'The FDA granted approval of ' + ' '.join(drugname) + ' to '
    regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
    pharmanameCriterion = re.compile(regexCondition,re.M)
    pharmaname = pharmanameCriterion.findall(text)
    if pharmaname == []:
        drugstringCondition = 'approval of ' + ' '.join(drugname) + ' was granted to '
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
        if pharmaname == []:
            drugstringCondition = 'granted the approval of ' + ' '.join(drugname) + ' to '
            pharmanameCriterion = re.compile(regexCondition,re.M)
            pharmaname = pharmanameCriterion.findall(text)
    #-----Debug Print Suite--------
    """
    print("The name of the drug is " + str(drugname))
    print("The name of the pharmacy is " + str(pharmaname))
    print("The date is " + str(date))
    """

    if drugname == [] and pharmaname == []:
        count+=1
        print(url)
        print(count)
#---------------In this portion of the script we will be going over URLS over a certain period------------
#Gather all the urls
count = 0
#----------------This is to gather 2019/2020 data---------------
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
            extract_text(tempsoup,abs_url,count)
            urls.add(abs_url)

print(count)
#Extract the text in each URL and build the Text classification tool
