import requests
from bs4 import BeautifulSoup
from URLcollector_functions.helper_functions import error_checker

# ////////////// RAKENDUSAKTIDE URLIDE KIRJUTAJA ////////////// 
   
# avab lehe ja kontrollib, kas on rakendusakte
def implementation_acts_finder(actURL):       
    #print(actURL)
    acturllist = []
    pageURL = actURL
    page = requests.get(pageURL)
    soup = BeautifulSoup(page.content, "html.parser")

    # kontrollib, kas aktil on sisutekst
    error = error_checker(soup)

    if not error:
        acturllist.append(pageURL)
        results = soup.find("ul", class_="tabs clear")
        rakendusaktid = results.select_one("a[href*='/akt_rakendusaktid']")

        if rakendusaktid:
            print("on rakendusaktid: "+ pageURL)
            rakendusaktid = rakendusaktid['href']
            raklist = create_implact_list(rakendusaktid)
            acturllist += raklist
    else:
        print("oli error aktis: "+ pageURL)
    
    # TODO siin peaks kirjutama kõik faili
    
    return acturllist

def create_implact_list(rakendusaktid):
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
        page = requests.get(akturl)
        soup = BeautifulSoup(page.content, "html.parser")
        error = error_checker(soup)
        if not error:
            newlist.append(akturl)
        else:
            print("oli error rakendusaktis: "+ akturl)
      
    return newlist