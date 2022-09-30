import requests
from bs4 import BeautifulSoup
#import re
from datetime import datetime
from xlsxwriter import Workbook

# ////////////// PEAMISED FUNKTSIOONID ////////////// 


# grabs all years from 1989 to current year and crates starting point URLs list of them
def kronoloogia():
    curentdatetime = datetime.now()
    date = curentdatetime.date()
    year=date.strftime("%Y")
    years = list(range(1989,int(year)+1))

    kronourls = []
    for year in years:
        baseurl = f"https://www.riigiteataja.ee/kronoloogia.html?aasta={year}&rtOsaId="
        kronourls.append(baseurl)

    return kronourls

# finds act URLs in chronological distributions
def chronoacts(events):
    print('alustab chronoacts')
    actlinks = []

    # looks for days when new changes were posted
    for event in events:
        eventurl = event.find('a')
        newURL = eventurl['href']
        newURL = newURL + "&rtOsaId=&leht=0&kuvaKoik=true&sorteeri=id&kasvav=false"
        
        page2 = requests.get(newURL) # goes to event/day page
        soup2 = BeautifulSoup(page2.content, "html.parser")
        results2 = soup2.find("tbody")
        acts = results2.find_all("a")

        # looks for acts posted on the day
        if len(acts) > 0:
            for act in acts: # looks at specific act
                actURL = act.get("href") # Estonian act url
                if actURL not in actlinks:
                    actlinks.append(actURL)

            #print('aktide lõpp')
        print('eventi lõpp')
    print('chronoactsfinder lõpp') 
    return actlinks

# looks for acts in süstemaatiline liigitus, Eurovoc, KOV määrused
def generalacts(results):
    print('alustab genacts')

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
        print('subpage lõpp')
    print('genactsfinder lõpp') 
    return actlinks

# identifies, whether the URL belongs to chronological or systematic distribution page
def actsfinder(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    
    if soup.find("ul", class_="system"): #systematic (incl. Eurovoc, KOV määrused)
        print('on genact')
        results = soup.find("ul", class_="system")
        actlinks = generalacts(results)
    elif soup.find_all("td", class_="event"): #chronological
        print('on chronoact')
        events = soup.find_all("td", class_="event") #finds all events
        actlinks = chronoacts(events)
    
    print('actsfinder lõpp')
    return actlinks

def removeduplicates(lst):
    seen = set()
    return [x for x in lst if not (x in seen or seen.add(x))]

# general acts STARTING POINT. Creates list of all acts found in chronological and systematic distribution. Removes duplicates. Writes URLs in .xlxs file.
def mainwriter(URLlist, path):
       
    actlinks = []
    for url in URLlist:
        linklist = actsfinder(url)
        actlinks += linklist
        print('linke lisati listi')
        
    noduplicates = removeduplicates(actlinks)
    print('duplikaadid eemaldatud')

    # writes .xlsx file
    workbook = Workbook(path, {'strings_to_urls': False}) # starts a new .xlsx file, writes URLs as string bc of row limit
    worksheet = workbook.add_worksheet()
    no = 1
    for el in noduplicates:
        worksheet.write("".join(["A" , str(no)]), el)
        no += 1
    
    workbook.close()  
    print("DONE")
    return noduplicates
