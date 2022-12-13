import requests
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
from URLcollector_functions.impl_acts_functions import implementation_acts_finder
from URLcollector_functions.helper_functions import removeduplicates, xlsx_file_writer
import os

# ////////////// PEAMISED FUNKTSIOONID ////////////// 

# identifies, whether the URL belongs to chronological or systematic distribution page
def starting_point_identifier(URLlist, path, filename_preposition):
    filenumber = 0

    for url in URLlist:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        if soup.find("ul", class_="system"): #systematic, Eurovoc, KOV määrused
            results = soup.find("ul", class_="system")
            actlinks = generalacts_urlfinder(results)
            filenumber += 1
            filename = "".join([filename_preposition, str(filenumber),"-sys.xlsx"])

        elif soup.find_all("td", class_="event"): #chronological
            events = soup.find_all("td", class_="event") #finds all events
            actlinks = chronoacts_urlfinder(events)
            filenumber += 1
            filename = "".join([filename_preposition, str(filenumber),"-chron.xlsx"])

        filepath = os.path.join(path, filename)
        xlsx_file_writer(actlinks, filepath)
    
    #print('actsfinder lõpp')
    return actlinks


# looks for acts in süstemaatiline liigitus, Eurovoc, KOV määrused
def generalacts_urlfinder(results):
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
                    implacts = implementation_acts_finder(actURL)
                    actlinks += implacts

    print('genactsfinder lõpp') 
    return actlinks

# finds act URLs in chronological distributions
def chronoacts_urlfinder(events):
    print('alustab chronoacts')
    actlinks = []
    counter = 0

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
                    implacts = implementation_acts_finder(actURL)
                    actlinks += implacts
                    counter +=1 
                    print(counter)
                    if counter >= 5:
                        break
                if counter >= 5:
                    break
            if counter >= 5:
                break 
        if counter >= 5:
            break  
                                         

    print('chronoactsfinder lõpp') 
    return actlinks






# general acts STARTING POINT. Creates list of all acts found in chronological and systematic distribution. Removes duplicates. Writes URLs in .xlxs file.
# def urls_to_xlsx_writer(URLlist, path):
       
#     actlinks = []
#     for url in URLlist:
#         linklist = starting_point_identifier(url)
#         actlinks += linklist
#         #print('linke lisati listi')
        
#     noduplicates = removeduplicates(actlinks)
#     #print('duplikaadid eemaldatud')

#     # writes .xlsx file
#     print("alustab kirjutamist")
#     workbook = Workbook(path, {'strings_to_urls': False}) # writes URLs as string bc of row limit
#     worksheet1 = workbook.add_worksheet()
#     no = 1
#     for el in noduplicates:
#         worksheet1.write("".join(["A" , str(no)]), el)
#         no += 1
    
#     workbook.close()  
#     print("DONE")
#     return noduplicates