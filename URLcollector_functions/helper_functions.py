import requests
from bs4 import BeautifulSoup
from datetime import datetime
from xlsxwriter import Workbook


# grabs all years from 1989 to current year and crates starting point URLs list of them
def create_chrono_starting_point_urls():
    curentdatetime = datetime.now()
    date = curentdatetime.date()
    year=date.strftime("%Y")
    years = list(range(1989,int(year)+1))

    kronourls = []
    for year in years:
        baseurl = f"https://www.riigiteataja.ee/kronoloogia.html?aasta={year}&rtOsaId="
        kronourls.append(baseurl)

    return kronourls

def error_checker(soup):
    results = soup.find("div", class_="message msg-error")
    if results:
        return True
    else:
        return False  

def removeduplicates(lst):
    print(len(lst))
    set_of_urls = set()
    return [x for x in lst if not (x in set_of_urls or set_of_urls.add(x))]


def xlsx_file_writer(urllist, path):
    print("alustab kirjutamist")
    workbook = Workbook(path, {'strings_to_urls': False}) # writes URLs as string bc of row limit
    worksheet = workbook.add_worksheet()
    no = 1
    for el in urllist:
        print(el)
        worksheet.write("".join(["A" , str(no)]), el)
        no += 1
    
    workbook.close()  
    print("lõpetas kirjutamise, sulges faili")

def create_search_page_urls(searchURLs):
    pages = []
    for url in searchURLs:
        pages_list = []
        pagecounter = 0
        searchpagelist = search_page_writer(url, pages_list, pagecounter)
        pages = searchpagelist[2]   
    
    removeduplicates(pages)

    return pages

def search_page_writer(url, pages_list, pagecounter):   
    #search function
    pages_list.append(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #vaatab, kas on veel lehekülgi
    nextpage = soup.find("li", class_="next") 
    if nextpage:
        nextlink = nextpage.find("a")
    

    # kui on veel lehekülgi, siis liigub järgmise juurde
    if nextlink:
        url = url.replace(("leht=" + str(pagecounter)), ("leht=" + str(pagecounter+1)))
        pagecounter += 1
        results = search_page_writer(url, pages_list, pagecounter)
        url = results[0]
        pagecounter = results[1]
        pages_list = results[2]

    return url, pagecounter, pages_list


