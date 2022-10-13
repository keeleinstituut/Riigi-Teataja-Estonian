url = "https://www.riigiteataja.ee/akt/24943"
import requests
from bs4 import BeautifulSoup
import re

#STEP 2
def domainwriter(sub, pathtext):
    pathtext = pathtext.replace("Süstemaatiline liigitus:","")
    pathtext = pathtext.replace("Eurovoc: ","")
    pathtext = pathtext.replace("Välislepingute liigitus poolte alusel: ","")
    pathtext = pathtext.replace("KOV määruste valdkondlik liigitus: ","")
    pathtext = pathtext.replace("\n","")
    pathtext = pathtext.strip()
    pathtext = pathtext.replace(" → ","::")
    if pathtext not in sub:
        sub.append(pathtext)
        el = pathtext
    while re.search(r'(.*?)::(?=[\w\s\d]+$)', el):
        el = re.search(r'(.*?)::(?=[\w\s\d]+$)', el)[1]
        if el not in sub:
            sub.append(el)
    return sub

# STEP1 
def subcatanalyzer(url): 
    # parse act
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")
    sub1 = []
    sub2 = []
    sub3 = []
    sub4 = []
    
    topcontent = soup.find("div", id="path")
    eurovocs = topcontent.find("div", class_="eurovoc")
    
    #eurovoc
    if eurovocs:
        eurovoc = eurovocs.find_all("p", class_="path")
        for e in eurovoc:
            etext = e.text
            sub2 = domainwriter(sub2, etext)    
    
    #süstemaatiline liigitus, KOV ja välislepingud
    if topcontent:
        pathinfo = topcontent.find_all("p", class_="path", recursive=False)
        for path in pathinfo:
            pathtext = path.text
            if "Süstemaatiline liigitus:" in pathtext:
                sub1 = domainwriter(sub1, pathtext)
            elif "KOV määruste valdkondlik liigitus:" in pathtext:
                sub3 = domainwriter(sub3, pathtext)
            elif "Välislepingute liigitus poolte alusel:" in pathtext:
                sub4 = domainwriter(sub4, pathtext)

    return sub1, sub2, sub3, sub4