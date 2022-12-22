#url = "https://www.riigiteataja.ee/akt/24943"
import requests
from bs4 import BeautifulSoup
import re

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
    if topcontent:
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


def subcat_from_main(paragraph):
    subcat1 = ""
    subcat2 = ""
    subcat3 = ""
    subcat4 = ""

    links = paragraph.find_all('a', href=True)
    if links:
        for url in links: 
            url = url['href']
            main_act_id = re.search('id=(\d*)!', url)
            if main_act_id:
                url = "".join(["https://www.riigiteataja.ee/akt/", main_act_id.group(1)])
                
                # subcategories
                subcat = subcatanalyzer(url) 
                if subcat[0]:
                    sub1 = subjoiner(subcat[0])
                    subcat1 = ",".join([subcat1, sub1])

                if subcat[1]:
                    sub2 = subjoiner(subcat[1])
                    subcat2 = ",".join([subcat2, sub2])

                if subcat[2]:
                    sub3 = subjoiner(subcat[2])
                    subcat3 = ",".join([subcat3, sub3])

                if subcat[3]:
                    sub4 = subjoiner(subcat[3])
                    subcat4 = ",".join([subcat4, sub4])


    subcat1 = subcat1.split(",")
    subcat1 = subjoiner(subcat1)
    subcat2 = subcat2.split(",")
    subcat2 = subjoiner(subcat2)
    subcat3 = subcat3.split(",")
    subcat3 = subjoiner(subcat3)
    subcat4 = subcat4.split(",")
    subcat4 = subjoiner(subcat4)

    return subcat1, subcat2, subcat3, subcat4

def subjoiner(subc):
    valuesonly = list(filter(None, subc))
    if len(valuesonly) == 0:
        subcat = "None"
    else:
        subcat = ','.join(valuesonly)

    return subcat



# def subanalyser(subresults, substring):
#     i = 3
#     while i <= 0:
#         if subresults[i]:
#             sub1 = subjoiner(subresults[i])
#             subcat1 = ",".join([subcat1, sub1])