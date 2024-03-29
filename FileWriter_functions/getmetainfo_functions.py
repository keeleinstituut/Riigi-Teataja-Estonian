import re
from datetime import datetime


def get_issuer(res_meta):
    issuer = 'issuer="NONE"'
    metaissuer = "NONE"
    
    if "Väljaandja" in res_meta:
        issuer = 'issuer="'+str(res_meta["Väljaandja"])+'"'
        metaissuer = str(res_meta["Väljaandja"])
        KOVIssuerList = ['linnavolikogu', 'vallavolikogu', 'vallavalitsus', 'linnavalitsus', 'alevivalitsus', 'alevivolikogu']
        isIssuedByKOV = any(ele in metaissuer.lower() for ele in KOVIssuerList)
        if isIssuedByKOV:
            metaissuer = "KÕIK KOVID,KÕIK KOVID::"+str(res_meta["Väljaandja"])
        else:
            metaissuer = "KÕIK ÜLERIIGILISED,KÕIK ÜLERIIGILISED::"+str(res_meta["Väljaandja"])
        issuer = 'issuer="'+str(metaissuer)+'"'        

    return issuer, metaissuer
    

def get_acttype(res_meta):
    act_type = 'act_type="NONE"'
    
    if "Akti liik" in res_meta:
        act_type = 'act_type="'+str(res_meta["Akti liik"])+'"'

    return act_type


def get_texttype(res_meta):
    text_type = 'text_type="NONE"'

    if "Teksti liik" in res_meta:
        text_type = 'text_type="'+str(res_meta["Teksti liik"])+'"'

    return text_type
        
        
def get_inforcefrom(res_meta, vv):
    in_force_from = 'in_force_from="NONE"'
    metain_force_from = 'NONE'
    
    if "Redaktsiooni jõustumise kp" in res_meta:
        in_force_from = 'in_force_from="'+str(res_meta["Redaktsiooni jõustumise kp"])+'"'
        metain_force_from = str(res_meta["Redaktsiooni jõustumise kp"])
    elif "Jõustumise kp" in res_meta:
        in_force_from = 'in_force_from="'+str(res_meta["Jõustumise kp"])+'"'
        metain_force_from = str(res_meta["Jõustumise kp"])
 
    return in_force_from, metain_force_from


def get_inforceuntil(res_meta):
    in_force_until = 'in_force_until="NONE"'
    metain_force_until = "NONE"
    
    if "Redaktsiooni kehtivuse lõpp" in res_meta and res_meta["Redaktsiooni kehtivuse lõpp"] != "":
        in_force_until = 'in_force_until="'+str(res_meta["Redaktsiooni kehtivuse lõpp"])+'"'
        metain_force_until = str(res_meta["Redaktsiooni kehtivuse lõpp"])
    elif "Kehtivuse lõpp" in res_meta and res_meta["Kehtivuse lõpp"] != "":
        in_force_until = 'in_force_until="'+str(res_meta["Kehtivuse lõpp"])+'"' 
        metain_force_until = str(res_meta["Kehtivuse lõpp"])       
    
    return in_force_until, metain_force_until

def get_publishingnote(res_meta):
    publishing_note = 'publishing_note="NONE"'
    metapublishing_note = "NONE"

    if "Avaldamismärge" in res_meta:
        if len(res_meta["Avaldamismärge"]) > 0:
            publishing_note = 'publishing_note="'+str(res_meta["Avaldamismärge"])+'"'
            metapublishing_note = str(res_meta["Avaldamismärge"])
    
    return publishing_note, metapublishing_note

def get_validity(metain_force_until, now):
    validity = "NONE"
    # validity parameter: Hetkel kehtiv, kehtetu, NONE
    date_in_force = ""
    if bool(re.search('\d+\.\d+\.\d\d\d\d', metain_force_until)):
        date_in_force=datetime.strptime(metain_force_until, "%d.%m.%Y")
        if date_in_force >= now:
            validity = "Hetkel kehtiv"
        elif date_in_force < now:
            validity = "Kehtetu"

    validity_note = 'validity="'+str(validity)+'"'

    return validity_note

def get_titleabb(soup):
    # act title and abbrevation
    title_long = soup.find("h1", class_="fixed").text
    title_long = title_long.strip()
    title_long = title_long.replace('"', "/'")
    abbrevation = "NONE"
   
    m = re.search(r'\(lühend\s-\s(.*?)\)', title_long)
    if m:
        abbrevation = m.group(1)
        n = re.search('(.*)+(lühend)', title_long)
        title_long = n.group(0).replace(' (lühend','')        
    
    title = 'title="'+str(title_long)+'"' 
    abbrevation_act = 'abbrevation="'+str(abbrevation)+'"' 

    return title_long, title, abbrevation, abbrevation_act

def get_timestamp(metain_force_from, metapublishing_note):
    # Timestamp parameter: YYYY form in_force_form or publishing_note
    timestamp_yearmonthday = "NONE"
    
    if metain_force_from != "NONE":
        yyyy = re.search('(\d{4})', metain_force_from)
        if yyyy:
         timestamp_yearmonthday = yyyy.group()
    elif metapublishing_note != "NONE":
        yyyy = re.search('(\d{4})', metapublishing_note)
        timestamp_yearmonthday = yyyy
        if yyyy:
            timestamp_yearmonthday = yyyy.group()

    publishing_year = 'publishing_year="'+str(timestamp_yearmonthday)+'"'

    return timestamp_yearmonthday, publishing_year