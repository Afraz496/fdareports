import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import re
import nltk
from urllib.parse import urljoin
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import xlwt
import pandas as pd
from xlwt import Workbook

def check_approval_sentence(text):
    if "approves" in text or "Approval" in text or "approve" in text or "approval" in text or "granted" in text:
        return True
    return False

def findPharmaName(pharmanames, text):
    for i in range(0, len(pharmanames)):
        if pharmanames[i].upper() in text.upper():
            return pharmanames[i]
    return ""

def findPharmaNamebyfirstname(pharmanames,text):
    for i in range(0,len(pharmanames)):
        lastname = pharmanames[i].split()
        if lastname[len(lastname)-1] == "CO":
            lastname[len(lastname)-1] = "Corporation"
        if lastname[len(lastname)-1] == "LTD":
            lastname[len(lastname)-1] = "Limited"
        if lastname[len(lastname)-1] == "PHARMA":
            lastname[len(lastname)-1] = "Pharmaceuticals"
        lastname = " ".join(lastname)
        if lastname.upper() in text.upper():
            return pharmanames[i]
    return "Not Found"

def extract_data(df,url):
    # get text
    temppage = requests.get(url)
    soup = BeautifulSoup(temppage.content,'lxml')
    text = soup.find_all('p')
    text_copy = text
    approvalsentence = ""

    for i in range(0,len(text_copy)):
        if check_approval_sentence(text_copy[i].get_text()):
            approvalsentence = text_copy[i].get_text()
    #----New Pharmacy Name Idea------
    pharmaname = ""
    pharmaname = findPharmaName(df, approvalsentence)
    if pharmaname == "":
        pharmaname = findPharmaNamebyfirstname(df, approvalsentence)
    #-----If the approval sentence is wrong-----
    if pharmaname == "":
        while(pharmaname == ""):
            for i in range(0, len(text_copy)):
                if check_approval_sentence(text_copy[i].get_text()):
                    approvalsentence = text_copy[i].get_text()
                    pharmaname = findPharmaName(df, approvalsentence)
                    if pharmaname == "":
                        pharmaname = findPharmaNamebyfirstname(df,approvalsentence)
                    if pharmaname != "":
                        break
            pharmaname = "Not Found"
    if pharmaname == "Not Found":
        while(pharmaname == "Not Found"):
            for i in range(0, len(text_copy)):
                if check_approval_sentence(text_copy[i].get_text()):
                    approvalsentence = text_copy[i].get_text()
                    pharmaname = findPharmaNamebyfirstname(df, approvalsentence)
                    if pharmaname != "Not Found":
                        break
            pharmaname = "Not Found Again"
    print("My pharmacy name is " + pharmaname)

data = pd.read_excel("listofpharmacies.xls")
df = data['Pharmacy Name'].values.tolist()
data = pd.read_excel("problematicpharmanames.xlsx")
df2 = data['URL'].values.tolist()
for i in range(0, len(df2)):
    extract_data(df,df2[i])
