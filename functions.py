import requests
from bs4 import BeautifulSoup
import re
import datetime
import xlsxwriter

def actsfinder(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("ul", class_="system")
    subcategories = results.find_all("a", class_=["name", "viimane-nimi"]) # all subcategories
    
    actlinks = []
    # looks for subpages in category
    for subpage in subcategories:
        partofurl = subpage['id'].replace('nimi.','')
        newURL = "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=" + partofurl + "&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true&leht=0&kuvaKoik=true&sorteeri=&kasvav=true"

        page2 = requests.get(newURL) # goes to subcategory page
        soup2 = BeautifulSoup(page2.content, "html.parser")
        results2 = soup2.find("tbody")
        acts = results2.find_all("a")

        # looks for acts in the subcategory
        if len(acts) > 0:
            for act in acts: # looks at specific act
                actURL = act.get("href") # Estonian act url
                if actURL not in actlinks:
                    actlinks.append(actURL)

            #print('aktide lõpp')
        #print('subpage lõpp')
    print('actsfinder lõpp') 
    return actlinks

def removeduplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# süstemaatiline liigitus, Eurivoc ja KOV STEP 1
def mainwriter(URLlist, path, func):
    # writes .xlsx file
    workbook = xlsxwriter.Workbook(path) # starts a new .xlsx file
    worksheet = workbook.add_worksheet()
        
    actlinks = []
    for url in URLlist:
        linklist = func(url)
        actlinks += linklist
        
    noduplicates = removeduplicates(actlinks)
    
    no = 1
    for el in noduplicates:
        worksheet.write('A'+str(no), str(el))
        no += 1
    
    workbook.close()  
    print("DONE")
    return noduplicates


# Rakendusaktide STEP 2
def rakenduslist(rakendusaktid):
    # avab rakendusaktide lehe
    URL = str(rakendusaktid) + "&leht=0&kuvaKoik=true&sorteeri=kehtivuseAlgus&kasvav=false"
    page = requests.get(URL)
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
    workbook = xlsxwriter.Workbook(path2) # starts a new .xlsx file
    worksheet = workbook.add_worksheet()
    no = 1
    
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

    for act in noduplicates:
        worksheet.write('A'+str(no), act)
        no += 1

    #print(no)
    workbook.close()
    print('DONE') 

    return raklist


# grabs all years from 1989 to current year and crates starting point URLs list of them
def kronoloogia():
    curentdatetime = datetime.datetime.now()
    date = curentdatetime.date()
    year=date.strftime("%Y")
    years = list(range(1989,int(year)+1))

    kronourls = []
    for year in years:
        baseurl = f"https://www.riigiteataja.ee/kronoloogia.html?aasta={year}&rtOsaId="
        kronourls.append(baseurl)

    return kronourls

# kronoloogilise jaotuse järgi aktide URLide otsija
def chronoactsfinder(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    events = soup.find_all("td", class_="event") #all events
    #subcategories = results.find_all("a", class_=["name", "viimane-nimi"]) # all subcategories
    #print(events)

    actlinks = []
    # looks for subpages in category
    for event in events:
        #partofurl = event['id'].replace('nimi.','')
        #newURL = "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=" + partofurl + "&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true&leht=0&kuvaKoik=true&sorteeri=&kasvav=true"
        eventurl = event.find('a')
        newURL = eventurl['href']
        newURL = newURL + "&rtOsaId=&leht=0&kuvaKoik=true&sorteeri=id&kasvav=false"
        
        page2 = requests.get(newURL) # goes to subcategory page
        soup2 = BeautifulSoup(page2.content, "html.parser")
        results2 = soup2.find("tbody")
        acts = results2.find_all("a")

        # looks for acts in the subcategory
        if len(acts) > 0:
            for act in acts: # looks at specific act
                actURL = act.get("href") # Estonian act url
                if actURL not in actlinks:
                    actlinks.append(actURL)

            #print('aktide lõpp')
        #print('subpage lõpp')
    print('actsfinder lõpp') 
    return actlinks


def newwriter(acturls, rakacturls, URLlist, path, func):
        
    actlinks = []
    for url in URLlist:
        linklist = func(url)
        #if url not in acturls and url not in rakacturls:
        actlinks += linklist
        
    noduplicates = removeduplicates(actlinks)
    
    # writes .xlsx file
    
    workbook = xlsxwriter.Workbook(path, {'strings_to_urls': False}) # starts a new .xlsx file
    worksheet = workbook.add_worksheet()

    no = 1
    for el in noduplicates:
        if el not in acturls and el not in rakacturls:
            worksheet.write('A'+str(no), str(el))
            no += 1
    
    workbook.close()  
    print("DONE2")
    return noduplicates
