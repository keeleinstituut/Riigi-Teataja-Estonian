import requests
from bs4 import BeautifulSoup
from URLcollector_functions.acts_functions import act_checker
from URLcollector_functions.helper_functions import check_if_exists


# identifies, whether the URL belongs to chronological or systematic distribution page
def starting_point_identifier(URLlist, filepath):

    for url in URLlist:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        print(url)
        
        #systematic, Eurovoc, KOV määrused, välislepingud
        if soup.find("ul", class_="system"): 
            results = soup.find("ul", class_="system")
            generalacts_metawriter(results, filepath)

        #chronological
        elif soup.find_all("td", class_="event"):
            events = soup.find_all("td", class_="event") #finds all events
            chronoacts_metawriter(events, filepath)
        
        #search function
        elif soup.find("table", class_="data"):
            resultstable = soup.find("tbody")
            # vaatab tabelist igat akti eraldi ja kirjutab kogu tulemuste lehe
            searchacts_writer(resultstable, filepath)
    
    print('starting_point_identifier lõpp')


# looks for acts in süstemaatiline liigitus, Eurovoc, KOV määrused
def generalacts_metawriter(results, filepath):
    print('alustab genacts')
    
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
                fileid = actURL.split('/')[-1]
            
                if check_if_exists(filepath, fileid):
                    act_checker(actURL, filepath)
    
    print('genactsfinder lõpp') 
    

# finds act URLs in chronological distributions
def chronoacts_metawriter(events, filepath):
    print('alustab chronoacts')

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
                fileid = actURL.split('/')[-1]
            
                if check_if_exists(filepath, fileid):
                    act_checker(actURL, filepath)
                   
    print('chronoactsfinder lõpp') 
  

# finds act URLs in chronological distributions
def searchacts_writer(resultstable, filepath):
    print('alustab searchacts')

    links = resultstable.find_all("a")

    # looks at all acts on search results page
    for link in links:
        actURL = link.get("href")
        if actURL:
            fileid = actURL.split('/')[-1]
            
            if check_if_exists(filepath, fileid):
                act_checker(actURL, filepath)

        else:
            print("Can not find act URL here: ", link)
    
    print('searchacts lõpp') 
    