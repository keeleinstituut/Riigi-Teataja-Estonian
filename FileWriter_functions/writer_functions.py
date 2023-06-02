# reads act URLs file for each act. Writes new .xlsx file of each ET-EN act. Writes all acts metadata in a separate file.
# loeb URLlistist iga akti, kirjutab eraldi .xlsx paralleelsesse ET-EN faili. Kõigi aktide andmetest eraldi metafail.

import requests
from bs4 import BeautifulSoup
import os
from os.path import exists
from datetime import datetime

from FileWriter_functions.domainwriter import subcatanalyzer, subcat_from_main, subjoiner
from FileWriter_functions.getmetainfo_functions import *

def actwriter(url, filepath, soup):
    # parse act
    try:
        # page = requests.get(url, timeout=30)
        # soup = BeautifulSoup(page.content, "lxml")
        
        metacontent = soup.find("table", class_="meta") # metadata
        bodycontent = soup.find("div", id="article-content") # body text
        # eemaldab tühjad tagid
        for x in bodycontent.find_all():
            if len(x.get_text(strip=True)) == 0 and x.name not in ['br']:
                x.extract()
        for t in bodycontent.select(".wrap"):
            t.extract()

        # finds "vastu võetud" for abbrevation purposes
        vastu_voetud = soup.find("p", class_="vv")
        if vastu_voetud and vastu_voetud.text != "":
            vv = vastu_voetud.br.previous_sibling.text
            vv = vv.replace('Vastu võetud ','')
        else:
            vv = "NONE"

        no = 1

        for br in bodycontent.find_all("br"):
            br.replace_with("\n")
        bodyparagraphs = bodycontent.find_all(["h1", "h2", "h3", "p", "pre", "div"])
        if len(bodyparagraphs) > 1 and not bodyparagraphs[-1].text == "Muudetud järgmiste aktidega (näita)":
            
            fileid = url.split('/')[-1]
            filename2 = 'RT-' +str(fileid) + ".xml"
            path = os.path.join(filepath, filename2)
            if not exists(path):
                with open(path, 'w',encoding='utf-8') as f:
                    
                    # writes act metadata
                    metadataET = metaparser(metacontent, soup, url, fileid, vv, bodyparagraphs)
                    f.write(metadataET)
                    f.write('\n')

                    # writes act body text
                    paragraphs = len(bodyparagraphs)-1 # number of paragraphs found
                    n = 0 # paragraph index
                    while n<=paragraphs:
                        tulemus = paralyzer(bodyparagraphs, n)
                        if len(tulemus[1]) != 0:
                            n = tulemus[0]
                            paraname = tulemus[2]
                            paratext = "<"+paraname+">"+tulemus[1]+"</"+paraname+">"
                            no += 1
                            f.write(paratext)
                            f.write('\n')
                        else:
                            n += 1
                    no += 1
                    f.write("</doc>")

                    print("---------------- kirjutas faili ---------------", fileid)

    except requests.exceptions.RequestException as e:
        print(url)
        print("!!!!!!! Error !!!!!!! ", e)



def metaparser(results, soup, url, fileid, vv, bodyparagraphs):   
    #filename and file id
    filename = 'filename='+'"RT-'+str(fileid)+'"'        
    idno = 'id='+'"'+str(fileid)+'"'

    #url
    url_actmeta = 'url="'+str(url)+'"' 

    # current date and time
    now = datetime.now() 
    crawltime = now.strftime("%H:%M:%S")
    crawldate = now.strftime("%Y-%m-%d") 
    crawl_date = 'crawl_date="'+crawldate+'"'
    crawl_time = 'crawl_time="'+crawltime+'"'

    # other
    passed = 'act_passed="'+vv+'"'

    # subcategories
    subcat = subcatanalyzer(soup) 
    subcat1 = subjoiner(subcat[0])
    subcat2 = subjoiner(subcat[1])
    subcat3 = subjoiner(subcat[2])
    subcat4 = subjoiner(subcat[3])

    if subcat1 == subcat2 == subcat3 == subcat4 == "NONE":
        for paragraph in bodyparagraphs:        
            if "Määrus kehtestatakse" in paragraph.text:
                subcats = subcat_from_main(paragraph)
                subcat1 = subcats[0]
                subcat2 = subcats[1]
                subcat3 = subcats[2]
                subcat4 = subcats[3]
                break

    sub1 = 'domain_systematic="'+subcat1+'"' 
    sub2 = 'domain_Eurovoc="'+subcat2+'"' 
    sub3 = 'domain_KOV="'+subcat3+'"' 
    sub4 = 'domain_foregin="'+subcat4+'"' 

    # other metainfo
    metainfo1 = results.find_all("th") # key             
    metainfo2 = results.find_all("td") # value
    metainfo1 = [x.text.replace(":","") for x in metainfo1]
    metainfo2 = [" ".join(x.text.split()) for x in metainfo2]
    res_meta = {metainfo1[i]: metainfo2[i] for i in range(len(metainfo1))} # dictionary
    
    titleabb_res = get_titleabb(soup)
    title = titleabb_res[1]
    abbrevation_act = titleabb_res[3]

    issuer_res = get_issuer(res_meta)
    issuer = issuer_res[0]
    metaissuer = issuer_res[1]
    
    act_tye_res = get_acttype(res_meta)
    act_type = act_tye_res
    
    text_type_res = get_texttype(res_meta)
    text_type = text_type_res
    
    in_force_from_res = get_inforcefrom(res_meta, vv)
    in_force_from = in_force_from_res[0]
    metain_force_from = in_force_from_res[1]

    in_force_until_res = get_inforceuntil(res_meta)
    in_force_until = in_force_until_res[0]
    metain_force_until = in_force_until_res[1]
    
    publishing_note_res = get_publishingnote(res_meta)
    publishing_note = publishing_note_res[0]
    metapublishing_note = publishing_note_res[1]

    validity_res = get_validity(metain_force_until, now)
    validity_note = validity_res
   
    timestamp_res = get_timestamp(metain_force_from, metapublishing_note)
    publishing_year = timestamp_res[1]   
       
    # creates meta for act file
    metadata = " ".join(['<doc', filename, idno, publishing_year,  sub1, sub2, sub3,  sub4, issuer, act_type, text_type,  in_force_from, in_force_until, validity_note, publishing_note, title, abbrevation_act, passed, crawl_date, crawl_time, url_actmeta,'>'])

    return metadata



def paralyzer(bodyparagraphs, n):
    value = ""
    paraname = bodyparagraphs[n].name
    if paraname in ["div", "pre"]:
        paraname = "p" 

    para1 = bodyparagraphs[n].text
    para1 = ' '.join((' '.join(para1.splitlines())).split())

    n += 1
    value += para1

    return n, value, paraname


