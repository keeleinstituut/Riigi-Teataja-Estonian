import requests
from bs4 import BeautifulSoup
#import re
from datetime import datetime
from xlsxwriter import Workbook
from main_functions import removeduplicates

# ////////////// RAKENDUSAKTIDE LUGEJA ////////////// 

# Rakendusaktide STEP 2
def rakenduslist(rakendusaktid):
    # avab rakendusaktide lehe
    url = str(rakendusaktid) + "&leht=0&kuvaKoik=true&sorteeri=kehtivuseAlgus&kasvav=false"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("tbody")
    rakendusaktid = results.find_all("a")
    
    # vaatab akthaaval, võtab URLi
    newlist = []
    for akt in rakendusaktid:
        akturl = akt['href']
        newlist.append(akturl)
        print(akturl)
      
    return newlist
    

# Rakendusaktide STEP 1
def rakendusaktide_lugeja(URLlist, path2):
    # siia hakkab koguma rakendusaktide URLe. Kui URL juba listis, siis ei lisa ka tabelisse uuesti.
    raklist = [] 
    
    # loeb üks url korraga
    for url in URLlist:
        print("uurin seda: ", url)
        
        # avab lehe ja otsib infot
        pageURL = url
        page = requests.get(pageURL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("ul", class_="tabs clear")
        rakendusaktid = results.select_one("a[href*='/akt_rakendusaktid']")
        
        # kui aktil on rakendusaktid
        if rakendusaktid:
            rakendusaktid = rakendusaktid['href']
            print("rakendusaktid olemas", pageURL)
            # vaatab läbi kõik rakendusaktid
            aktiscan = rakenduslist(rakendusaktid)
            raklist += aktiscan
            
        else:
            print("ei ole rakendusakte", pageURL)
    
    noduplicates = removeduplicates(raklist)

    workbook = Workbook(path2, {'strings_to_urls': False}) # starts a new .xlsx file
    worksheet = workbook.add_worksheet()
    no = 1
    for act in noduplicates:
        if act not in URLlist:
            worksheet.write("".join(["A" , str(no)]), act)
            no += 1

    #print(no)
    workbook.close()
    print('DONE') 

    return raklist





