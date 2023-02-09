import requests
from bs4 import BeautifulSoup
from xlsxwriter import Workbook
from URLcollector_functions.acts_functions import act_checker
from URLcollector_functions.helper_functions import removeduplicates, xlsx_file_writer
from FileWriter_functions.writer_functions import actwriter
import os
import xlsxwriter


# ////////////// PEAMISED FUNKTSIOONID ////////////// 

# identifies, whether the URL belongs to chronological or systematic distribution page
def starting_point_identifier(URLlist, filepath, mainpath, metafiledate, metacounter):
    filenumber = 0

    for url in URLlist:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        
        #systematic, Eurovoc, KOV määrused, välislepingud
        if soup.find("ul", class_="system"): 
            results = soup.find("ul", class_="system")
            metacounter = generalacts_metawriter(results, mainpath, filepath, metafiledate, metacounter)
            filenumber += 1

        #chronological
        elif soup.find_all("td", class_="event"):
            events = soup.find_all("td", class_="event") #finds all events
            metacounter = chronoacts_metawriter(events, mainpath, filepath, metafiledate, metacounter)
            filenumber += 1
        
        #search function
        elif soup.find("table", class_="data"):
            resultstable = soup.find("tbody")
            # vaatab tabelist igat akti eraldi ja kirjutab kogu tulemuste lehe
            metacounter = searchacts_metawriter(resultstable, mainpath, filepath, metafiledate, metacounter)
            filenumber += 1
    
    print('starting_point_identifier lõpp')


# looks for acts in süstemaatiline liigitus, Eurovoc, KOV määrused
def generalacts_metawriter(results, mainpath, filepath, metafiledate, metacounter):
    print('alustab genacts')

    metapath = os.path.join(mainpath, ("".join([metafiledate, str(metacounter), '-general.xlsx'])))

    counter = 0
    metano = 1
    metaworkbook = xlsxwriter.Workbook(metapath) # starts a new .xlsx file
    metaworksheet = metaworkbook.add_worksheet()
    metasheet_header_writer(metaworksheet)
    
    subcategories = results.find_all("a", class_=["name", "viimane-nimi"]) # all subcategories
    
    #actlinks = []
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
                #if actURL not in actlinks:
                actinfo = act_checker(actURL, metano, metaworksheet, counter, filepath)
                metano = actinfo[0]
                counter = actinfo[1]
                #actlinks += implacts

    metaworkbook.close() 
    metacounter += 1
    
    print('genactsfinder lõpp') 
    
    return metacounter

# finds act URLs in chronological distributions
def chronoacts_metawriter(events, mainpath, filepath, metafiledate, metacounter):
    print('alustab chronoacts')
    #actlinks = []

    metapath = os.path.join(mainpath, ("".join([metafiledate, str(metacounter), '-chrono.xlsx'])))
    
    counter = 0
    metano = 1
    metaworkbook = xlsxwriter.Workbook(metapath) # starts a new .xlsx file
    metaworksheet = metaworkbook.add_worksheet()
    metasheet_header_writer(metaworksheet)

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
                actinfo = act_checker(actURL, metano, metaworksheet, counter, filepath)
                metano = actinfo[0]
                counter = actinfo[1]
                #if actURL not in actlinks:
                #    implacts = implementation_acts_finder(actURL)
                #    actlinks += implacts
                #counter +=1 
                #"   print(counter)
                if counter >= 5:
                    break
            if counter >= 5:
                break 
        if counter >= 5:
            break  
    
    metaworkbook.close()
    metacounter += 1                                    
    print('chronoactsfinder lõpp') 
    

    return metacounter

# finds act URLs in chronological distributions
def searchacts_metawriter(resultstable, mainpath, filepath, metafiledate, metacounter):
    print('alustab searchacts')
    #actlinks = []

    metapath = os.path.join(mainpath, ("".join([metafiledate, str(metacounter), '-search.xlsx'])))
    
    counter = 0
    metano = 1
    metaworkbook = xlsxwriter.Workbook(metapath) # starts a new .xlsx file
    metaworksheet = metaworkbook.add_worksheet()
    metasheet_header_writer(metaworksheet)

    links = resultstable.find_all("a")

    # looks at all acts on search results page
    for link in links:
        actURL = link.get("href")
        if actURL:
            actinfo = act_checker(actURL, metano, metaworksheet, counter, filepath)
            metano = actinfo[0]
            counter = actinfo[1]
        else:
            print("Can not find act URL here: ", link)
    
    metaworkbook.close()
    metacounter += 1                                    
    print('searchacts lõpp') 
    

    return metacounter

def metasheet_header_writer(metaworksheet):
    # writes meta headers
    metaworksheet.write('A1', "filename")
    metaworksheet.write('B1', "id")
    metaworksheet.write('C1', "publishing_year")
    metaworksheet.write('D1', "domain_systematic")
    metaworksheet.write('E1', "domain_Eurovoc")
    metaworksheet.write('F1', "domain_KOV")
    metaworksheet.write('G1', "domain_foregin")
    metaworksheet.write('H1', "issuer")
    metaworksheet.write('I1', "act_type")
    metaworksheet.write('J1', "text_type")
    metaworksheet.write('K1', "in_force_from")
    metaworksheet.write('L1', "in_force_until")
    metaworksheet.write('M1', "validity")
    metaworksheet.write('N1', "publishing_note")
    metaworksheet.write('O1', "title")
    metaworksheet.write('P1', "abbrevation")
    metaworksheet.write('Q1', "act_passed")
    metaworksheet.write('R1', "crawl_date")
    metaworksheet.write('S1', "crawl_time")
    metaworksheet.write('T1', "url")
    # metaworksheet.write('U1', "language")




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