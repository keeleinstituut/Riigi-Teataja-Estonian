from URLcollector_functions.URL_scraper_functions import starting_point_identifier
from URLcollector_functions.helper_functions import create_chrono_starting_point_urls
#from implementation_url_scraper_functions_fromfile import implementation_acts_writer
import time
#from URLS_from_xlsx import urlcollector
import os
from os.path import exists
from openpyxl import Workbook
import datetime

start_time = time.time()
currentdir = os.getcwd()

# filename = 'RT-ET-allacts_dec.xlsx'
# if not exists(filename):
#     wb = Workbook()
#     wb.save(filename)

current_date = datetime.datetime.now()
today = current_date.strftime("%Y%m%d")

current_dir = os.getcwd()
folder = "acts_dec"
path = os.path.join(current_dir, folder)
filename_preposition = "".join(["RT-ET-", today,"-"])

# süstemaatiline liigitus, Eurovoc, KOV määrused
#URLlist = ["https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=S%C3%9CSTJAOT&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true", 
#             "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=0&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true",
#             "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=KOV&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true"]

# creates chronological distribution URLs for each year since 1989 up until current year 
#chronoURLs = create_chrono_starting_point_urls()
#URLlist += chronoURLs
URLlist=["https://www.riigiteataja.ee/kronoloogia.html?aasta=2022&kpv="]#, "https://www.riigiteataja.ee/kronoloogia.html?aasta=2005&kpv="]
#allActs = urls_to_xlsx_writer(URLlist, filename)
allActs = starting_point_identifier(URLlist, path, filename_preposition)
print(len(allActs))




# acturls = urlcollector(path1)
# print(len(acturls))
# rakendusaktideURLid = implementation_acts_writer(acturls, path2)
# print(len(rakendusaktideURLid))

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# print(kronoURLs)
# kronoacts = mainwriter(kronoURLs, path3, chronoactsfinder)
