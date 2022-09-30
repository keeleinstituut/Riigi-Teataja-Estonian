import requests
from bs4 import BeautifulSoup
#import re
from datetime import datetime
from xlsxwriter import Workbook
from main_functions import removeduplicates


#pageURL = 'https://www.riigiteataja.ee/akt/32035' # probleemne (File "c:\Users\tiiu.uksik\Documents\RTkorpus\scraper.py", line 46, in <module>
   # rakendusaktideURLid = rakendusaktide_lugeja(acturls, path2)
   # rakendusaktid = results.select_one("a[href*='/akt_rakendusaktid']"))
#pageURL = 'https://www.riigiteataja.ee/akt/13088392' # mitte-probleemne, ei ole rakendusakte
pageURL = 'https://www.riigiteataja.ee/akt/109122021012' #mitte-probleemne, rakendusaktid olemas
page = requests.get(pageURL)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find("ul", class_="tabs clear")
rakendusaktid = results.select_one("a[href*='/akt_rakendusaktid']")
print(results)