import requests
from bs4 import BeautifulSoup
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import xlwt
from xlwt import Workbook

def lexicon_analysis(text):
    return

def clean_text(text):
    blankstr = ""
    for i in range(3,len(text)-2):
        blankstr += text[i].get_text()
    return blankstr

def clean_pharmaname(pharmaname):
    if len(pharmaname) > 1:
        pharmaname = pharmaname[len(pharmaname)-1]
    else:
        pharmanme = " ".join(pharmaname)
    return pharmaname

def check_drug_name(drugname):
    drugnameLong = False
    if len(drugname) > 1:
        drugnameLong = True
        drugname = drugname[len(drugname)-1]
    return drugname, drugnameLong

def extract_text(soup, url,excel_data_pointer, workbook):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.find_all('p')
    #find the date:
    date = text[len(text)-2].get_text()
    text_copy = text

    text = clean_text(text)

    #Extract company information
    if text_copy[len(text_copy) - 4] == "":
        approvalsentence = text_copy[len(text_copy) - 6].get_text()
    else:
        approvalsentence = text_copy[len(text_copy) - 5].get_text()

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
        drugdiscoveryCriterion = re.compile(r"(?<= approval of the )(.*?)(?= was )",re.M)
        drugname = drugdiscoveryCriterion.findall(text)

    #-----If Regex caught more than one sentence always make drugname the last one------
    drugnameLong = False
    drugname, drugnameLong = check_drug_name(drugname)
#------------Finding the name of the pharmaceutical from the text-------------
    if drugnameLong == True:
        drugstringCondition = drugstringCondition = 'The FDA granted approval of ' + drugname + ' to '
    else:
        drugstringCondition = 'The FDA granted approval of ' + ' '.join(drugname) + ' to '
    regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
    pharmanameCriterion = re.compile(regexCondition,re.M)
    pharmaname = pharmanameCriterion.findall(text)

    #-------Exception handling when drug name not found----------
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = ' approval of ' + drugname + ' was granted to '
        else:
            drugstringCondition = ' approval of ' + ' '.join(drugname) + ' was granted to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'The FDA granted the approval of ' + drugname + ' to '
        else:
            drugstringCondition = 'The FDA granted the approval of ' + ' '.join(drugname) + ' to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'The FDA granted Priority Review of ' + drugname + ' to '
        else:
            drugstringCondition = 'The FDA granted Priority Review of ' + ' '.join(drugname) + ' to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = ' the approved generic version of ' + drugname + ' is '
        else:
            drugstringCondition = ' the approved generic version of ' + ' '.join(drugname) + ' is '
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = ' FDA granted approvals of ' + drugname + ' to '
        else:
            drugstringCondition = ' FDA granted approvals of ' + ' '.join(drugname) + ' to '
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'The sponsor of the approved generic version of ' + drugname + ' is '
        else:
            drugstringCondition = 'The sponsor of the approved generic version of ' + ' '.join(drugname) + ' is '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'Approval of ' + drugname + ' was granted to '
        else:
            drugstringCondition = 'Approval of ' + ' '.join(drugname) + ' was granted to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=,|\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'Approval of ' + drugname + ' were granted to '
        else:
            drugstringCondition = 'Approval of ' + ' '.join(drugname) + ' were granted to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=,|\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = ' approval of ' + drugname + ' was granted to '
        else:
            drugstringCondition = ' approval of ' + ' '.join(drugname) + ' was granted to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=,|\.)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
        if pharmaname == []:
            if drugnameLong == True:
                drugstringCondition = ' approval of the ' + drugname + ' was granted to '
            else:
                drugstringCondition = ' approval of the ' + ' '.join(drugname) + ' was granted to '
            regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=,|\.)'
            pharmanameCriterion = re.compile(regexCondition,re.M)
            pharmaname = pharmanameCriterion.findall(text)
            if len(pharmaname) > 1:
                pharmaname = pharmanameCriterion.findall(approvalsentence)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'Approvals of ' + drugname + ' were granted to '
        else:
            drugstringCondition = 'Approvals of ' + ' '.join(drugname) + ' were granted to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=,|\.)'
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
    if pharmaname == []:
        regexCondition = r'(?<=\.)(.*?)(?= holds the application )'
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
    #--------This code is exhaustive for multiple pharmaceuticals on the same drug---------
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'The FDA granted approvals for the generic versions of ' + drugname + ' to '
        else:
            drugstringCondition = 'The FDA granted approvals for the generic versions of ' + ' '.join(drugname) + ' to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\n|$)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
    if pharmaname == []:
        if drugnameLong == True:
            drugstringCondition = 'The FDA granted approvals for the ' + drugname + ' to '
        else:
            drugstringCondition = 'The FDA granted approvals for the ' + ' '.join(drugname) + ' to '
        regexCondition = r'(?<='+drugstringCondition+')(.*?)(?=\n|$)'
        pharmanameCriterion = re.compile(regexCondition,re.M)
        pharmaname = pharmanameCriterion.findall(text)
        if len(pharmaname) > 1:
            pharmaname = pharmanameCriterion.findall(approvalsentence)
    #-----Debug Print Suite--------
    """
    print("The name of the drug is " + str(drugname))
    print("The name of the pharmacy is " + str(pharmaname))
    print("The date is " + str(date))
    """
    #-------Why certain pharmacy names are not found----------
    if pharmaname == [] and drugname != []:
        print("The length of the whole HTML is: " + str(len(text_copy)))
        print(approvalsentence)
        print("Drugname: " + str(drugname))
        print(pharmanameCriterion)
        print(url)

    #-----Add data to excel-------
    pharmaname = clean_pharmaname(pharmaname)
    sheet.write(excel_data_pointer,0,pharmaname)
    sheet.write(excel_data_pointer,1,date)
    workbook.save('FDA.xls')
    #sheet.write(excel_data_pointer,2,'Dangerous')
#---------------In this portion of the script we will be going over URLS over a certain period------------
#Create Excel File
wb = Workbook()

sheet = wb.add_sheet('FDA Mined Data')

#Create column names
sheet.write(0,0,'Pharmacy Name')
sheet.write(0,1,'Date')
sheet.write(0,2,'Dangerous')

#Gather all the urls
excel_data_pointer = 1
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
            extract_text(tempsoup,abs_url,excel_data_pointer,wb)
            urls.add(abs_url)
            excel_data_pointer += 1

#-----TODO: Add a script on 2013-2018 data------------

#Extract the text in each URL and build the Text classification tool
