import requests
from bs4 import BeautifulSoup
from URLcollector_functions.helper_functions import error_checker
from FileWriter_functions.writer_functions import actwriter


# ////////////// RAKENDUSAKTIDE URLIDE KIRJUTAJA ////////////// 
   
# avab lehe ja kontrollib, kas on rakendusakte
def act_checker(actURL, metano, metaworksheet, counter, filepath):       
    #print(actURL)
    #acturllist = []
    pageURL = actURL
    print("alustab aktiga: ", pageURL)
    page = requests.get(pageURL)
    soup = BeautifulSoup(page.content, "html.parser")

    # kontrollib, kas aktil on sisutekst
    error = error_checker(soup)

    if not error:
        #acturllist.append(pageURL)
        result = actwriter(pageURL, metaworksheet, metano, filepath)
        metano = result[1]
        counter +=1
        print(counter, "done act: ", actURL, "metadata row:", metano)

        implacts = impl_acts_checker(soup, pageURL, metaworksheet, counter, metano, filepath)
        metano = implacts[0]
        counter = implacts[1]
        

    else:
        print("oli error aktis: "+ pageURL)
        
    return metano, counter

def impl_acts_checker(soup, pageURL, metaworksheet, counter, metano, filepath):
    results = soup.find("ul", class_="tabs clear")
    rakendusaktid = results.select_one("a[href*='/akt_rakendusaktid']")

    if rakendusaktid:
        #print("on rakendusaktid: "+ pageURL)
        rakendusaktid = rakendusaktid['href']
        raklist = impl_act_writer(rakendusaktid, metaworksheet, counter, metano, filepath)
        metano = raklist[0]
        counter = raklist[1]
    
    return metano, counter


def impl_act_writer(rakendusaktid, metaworksheet, counter, metano, filepath):
    # avab rakendusaktide lehe
    url = str(rakendusaktid) + "&leht=0&kuvaKoik=true&sorteeri=kehtivuseAlgus&kasvav=false"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find("tbody")
    rakendusaktid = results.find_all("a")
    
    # vaatab akthaaval, kirjutab faili
    #newlist = []
    for akt in rakendusaktid:
        akturl = akt['href']
        print("alustab rakendusaktiga: ", akturl)
        page = requests.get(akturl)
        soup = BeautifulSoup(page.content, "html.parser")
        error = error_checker(soup)
        if not error:
            result = actwriter(akturl, metaworksheet, metano, filepath)
            metano = result[1]
            counter +=1
            print(counter, "done implact: ", akturl, "metadata row:", metano)
            #newlist.append(akturl)
        else:
            print("oli error rakendusaktis: "+ akturl)
      
    return metano, counter