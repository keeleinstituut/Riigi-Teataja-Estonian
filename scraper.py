from main_functions import mainwriter, kronoloogia
from rakendusaktid_functions import rakendusaktide_lugeja
import time
from urlcollector_functions import urlcollector
from os.path import exists
from openpyxl import Workbook

start_time = time.time()




path1 = 'RT-ET_test\RT-ET-allacts.xlsx'
if not exists(path1):
    wb = Workbook()
    wb.save(path1)
path2 = 'RT-ET_test\RT-rakendusaktid-all.xlsx'
if not exists(path2):
    wb = Workbook()
    wb.save(path2)
path3 = 'RT-ET_test\RT-kronoloogia-2.xlsx'
#path4 = 'RT-ET_test\RT-kronoloogia2-2.xlsx'







# süstemaatiline liigitus, Eurovoc, KOV määrused
URLlist = ["https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=S%C3%9CSTJAOT&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true", 
             "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=0&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true",
             "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=KOV&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true"]

# creates chronological distribution URLs for each year since 1989 up until current year 
chronoURLs = kronoloogia()
URLlist += chronoURLs
allActs = mainwriter(URLlist, path1)
print(len(allActs))




acturls = urlcollector(path1)
print(len(acturls))
rakendusaktideURLid = rakendusaktide_lugeja(acturls, path2)
print(len(rakendusaktideURLid))

print("Process finished --- %s seconds ---" % (time.time() - start_time))

# print(kronoURLs)
# kronoacts = mainwriter(kronoURLs, path3, chronoactsfinder)
