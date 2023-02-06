from URLcollector_functions.type_identifier_functions import starting_point_identifier
from URLcollector_functions.helper_functions import create_chrono_starting_point_urls, create_search_page_urls
from single_meta_file_writer_functions import start_meta_file

import time
import os
from os.path import exists
import datetime
from datetime import date

start_time = time.time()

# prevents requests.exceptions.SSLError: HTTPSConnectionPool(host='www.riigiteataja.ee', port=443): Max retries exceeded with url: /akt/114072020015 (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:997)')))
import imaplib
import ssl
ctx = ssl.create_default_context()
ctx.set_ciphers('DEFAULT')
imapSrc = imaplib.IMAP4_SSL('mail.safemail.it', ssl_context = ctx)

# süstemaatiline liigitus, Eurovoc, KOV määrused
#URLlist = ["https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=S%C3%9CSTJAOT&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true", 
#              "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=0&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true",
#              "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=KOV&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true",
#              "https://www.riigiteataja.ee/jaotused.html?tegevus=&jaotus=RIIGID&avatudJaotused=&suletudJaotused=&jaotusedVaikimisiAvatud=true"
#              ]

# creates chronological distribution URLs for each year since 1989 up until current year 
#chronoURLs = create_chrono_starting_point_urls()
#URLlist += chronoURLs

# search function URLS
currentDate = datetime.date.today()
kuupaev = currentDate.strftime("%d.%m.%Y")
searchURLs = [#'https://www.riigiteataja.ee/algteksti_tulemused.html?doli=v%C3%A4lisleping&nrOtsing=tapne&leht=0&kuvaKoik=true&sorteeri=&kasvav=true',
             #"https://www.riigiteataja.ee/tervikteksti_tulemused.html?kehtivusKuupaev=" + str(kuupaev) + "&nrOtsing=tapne&riigikoguOtsused=false&valislepingud=false&valitsuseKorraldused=false&sakk=koik_otsitavad&leht=0&kuvaKoik=true&sorteeri=&kasvav=true",
             "https://www.riigiteataja.ee/algteksti_tulemused.html?nrOtsing=tapne&leht=0&kuvaKoik=true&sorteeri=&kasvav=true",
             #"https://www.riigiteataja.ee/tervikteksti_tulemused.html?kehtivusKuupaev=" + str(kuupaev) + "&kov=true&nrOtsing=tapne&valj1=K%C3%B5ik+KOV-id&sakk=koik_otsitavad&leht=0&kuvaKoik=true&sorteeri=&kasvav=true",
             #"https://www.riigiteataja.ee/algteksti_tulemused.html?kov=true&nrOtsing=tapne&valj1=K%C3%B5ik+KOV-id&leht=0&kuvaKoik=true&sorteeri=&kasvav=true",
             ]
searchPageURLs = create_search_page_urls(searchURLs)
URLlist = searchPageURLs


# main folder, acts folder and meta paths
current_dir = os.getcwd()
current_month_text = datetime.datetime.now().strftime('%h')
main_folder = "".join(["acts_",current_month_text])
if not exists(main_folder):
    os.mkdir(main_folder) 
mainpath = os.path.join(current_dir, main_folder)
acts_folder = "acts"
file_path = os.path.join(mainpath, acts_folder)
if not exists(file_path):
    os.mkdir(file_path) 

#meta_files_path  = os.path.join(mainpath, "acts_meta")

# current date for meta file name
today = date.today()
metafiledate = "".join(["acts-meta-",str(today),"-"])
metacounter = 1


starting_point_identifier(URLlist, file_path, mainpath, metafiledate, metacounter)

all_metafiledate = "".join(["all-acts-meta-",str(today),".xlsx"])
all_metapath = os.path.join(mainpath, all_metafiledate)

start_meta_file(all_metapath, mainpath)


print("Process finished --- %s seconds ---" % (time.time() - start_time))
