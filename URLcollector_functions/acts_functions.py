import requests
from bs4 import BeautifulSoup
from URLcollector_functions.helper_functions import error_checker, check_if_exists
from FileWriter_functions.writer_functions import actwriter


# ////////////// RAKENDUSAKTIDE URLIDE KIRJUTAJA ////////////// 
   
# avab lehe ja kontrollib, kas on rakendusakte
def act_checker(actURL, filepath):       

    print("alustab aktiga: ", actURL)   
    
    try:
        page = requests.get(actURL, timeout=30)
        soup = BeautifulSoup(page.content, "lxml")
        
        # kas on sisutekst?
        error = error_checker(soup)

        if not error:                   
            # kirjutab akti
            actwriter(actURL, filepath, soup)
            
            # kas on rakendusakte?
            impl_acts_checker(soup, filepath)

        else:
            print("oli error aktis: "+ actURL)
    
    except requests.exceptions.RequestException as e:
        print(actURL)
        print("!!!!!!! Error !!!!!!! ", e)


def impl_acts_checker(soup, filepath):
    results = soup.find("ul", class_="tabs clear")
    if results:
        rakendusaktid = results.select_one("a[href*='/akt_rakendusaktid']")

        if rakendusaktid:
            rakendusaktid = rakendusaktid['href']
            impl_act_writer(rakendusaktid, filepath)


def impl_act_writer(rakendusaktid, filepath):
    # avab rakendusaktide lehe
    url = str(rakendusaktid) + "&leht=0&kuvaKoik=true&sorteeri=kehtivuseAlgus&kasvav=false"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("tbody")
    if results:
        rakendusaktid = results.find_all("a")
        
        # vaatab akthaaval, kirjutab faili
        for akt in rakendusaktid:
            akturl = akt['href']
            print("alustab rakendusaktiga: ", akturl)
            fileid = akturl.split('/')[-1]
            
            # kas akt on juba kirjutatud?
            if check_if_exists(filepath, fileid):
                page = requests.get(akturl)
                soup = BeautifulSoup(page.content, "lxml")
                error = error_checker(soup)
                if not error:
                    actwriter(akturl, filepath, soup)
                    #print("done implact: ", akturl)
                else:
                    print("oli error rakendusaktis: "+ akturl)
    else:
        print("Technical error opening oli implementing acts: "+ url)
