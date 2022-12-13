import re
from datetime import datetime


def get_issuer(res_meta):
    if "Väljaandja" in res_meta:
        issuer = 'issuer="'+res_meta["Väljaandja"]+'"'
        metaissuer = str(res_meta["Väljaandja"])
    else:
        issuer = 'issuer="None"'
        metaissuer = "None"

    return issuer, metaissuer
    

def get_acttype(res_meta, metaissuer):
    if "Akti liik" in res_meta:
        act_type = 'act_type="'+res_meta["Akti liik"]+'"'
        metaact_type = str(res_meta["Akti liik"])
        if metaact_type == 'määrus':
            KOVIssuerList = ['linnavolikogu', 'vallavolikogu', 'vallavalitsus', 'linnavalitsus', 'alevivalitsus', 'alevivolikogu']
            isIssuedByKOV = any(ele in metaissuer.lower() for ele in KOVIssuerList)
            if isIssuedByKOV:
                act_type = 'act_type=KOV määrus'
                metaact_type = 'KOV määrus'   
            else:
                act_type = 'act_type=üleriigiline määrus'
                metaact_type = 'üleriigiline määrus'  
    else:
        act_type = 'act_type="None"'
        metaact_type = "None"

    return act_type, metaact_type


def get_texttype(res_meta):
    if "Teksti liik" in res_meta:
        text_type = 'text_type="'+res_meta["Teksti liik"]+'"'
        metatext_type = str(res_meta["Teksti liik"])
    else:
        text_type = 'text_type="None"'
        metatext_type = "None"

    return text_type, metatext_type
        
        
def get_inforcefrom(res_meta, vv):
    if "Redaktsiooni jõustumise kp" in res_meta:
        in_force_from = 'in_force_from="'+res_meta["Redaktsiooni jõustumise kp"]+'"'
        metain_force_from = str(res_meta["Redaktsiooni jõustumise kp"])
    elif "Jõustumise kp" in res_meta:
        in_force_from = 'in_force_from="'+res_meta["Jõustumise kp"]+'"'
        metain_force_from = str(res_meta["Jõustumise kp"])
    else:
        date_from_vv = vv.split(" ")
        contains_date = any([char.isdigit() for char in date_from_vv[0]])
        if contains_date:
            in_force_from = 'in_force_from="' +date_from_vv[0]+ '""'
            metain_force_from = date_from_vv[0]
        else:
            in_force_from = 'in_force_from="None"'
            metain_force_from = 'None'

    return in_force_from, metain_force_from


def get_inforceuntil(res_meta):
    if "Redaktsiooni kehtivuse lõpp" in res_meta and res_meta["Redaktsiooni kehtivuse lõpp"] != "":
        in_force_until = 'in_force_until="'+res_meta["Redaktsiooni kehtivuse lõpp"]+'"'
        metain_force_until = str(res_meta["Redaktsiooni kehtivuse lõpp"])
    elif "Kehtivuse lõpp" in res_meta and res_meta["Kehtivuse lõpp"] != "":
        in_force_until = 'in_force_until="'+res_meta["Kehtivuse lõpp"]+'"' 
        metain_force_until = str(res_meta["Kehtivuse lõpp"])
    else:
        in_force_until = 'in_force_until="None"'
        metain_force_until = "None"
    
    return in_force_until, metain_force_until

def get_publishingnote(res_meta):
    if "Avaldamismärge" in res_meta:
        publishing_note = 'publishing_note="'+res_meta["Avaldamismärge"]+'"'
        metapublishing_note = str(res_meta["Avaldamismärge"])
    else:
        publishing_note = 'publishing_note="None"'
        metapublishing_note = "None"
    
    return publishing_note, metapublishing_note

def get_validity(metain_force_until, now):
    validity = "None"
    # validity parameter: Hetkel kehtiv, kehtetu, None
    date_in_force = ""
    if any(chr.isdigit() for chr in metain_force_until):
        date_in_force=datetime.strptime(metain_force_until, "%d.%m.%Y")
        if date_in_force >= now:
            validity = "Hetkel kehtiv"
        elif date_in_force < now:
            validity = "Kehtetu"
    else:
        validity = metain_force_until

    validity_note = 'validity="'+validity+'"'
    metavalidity_note = str(validity)

    return validity_note, metavalidity_note

def get_titleabb(soup):
    # act title and abbrevation
    title_long = soup.find("h1", class_="fixed").text
    title_long = title_long.strip()# title_long.replace("\s+","")
    m = re.search(r'\(lühend\s-\s(.*?)\)', title_long)
    if m:
        abbrevation = m.group(1)
        n = re.search('(.*)+(lühend)', title_long)
        title_long = n.group(0).replace(' (lühend','')
    else:
        abbrevation = "None"
    
    title = 'title="'+title_long+'"' 
    abbrevation_act = 'abbrevation="'+abbrevation+'"' 

    return title_long, title, abbrevation, abbrevation_act

def get_timestamp(metain_force_from, metapublishing_note):
    # Timestamp parameter: YYYY form in_force_form or publishing_note
    if metain_force_from != "None":
        yyyy = re.findall('(\d{4})', metain_force_from)
        timestamp_yearmonthday = yyyy[0]
    elif metapublishing_note != "None":
        yyyy = re.findall('(\d{4})', metapublishing_note)
        timestamp_yearmonthday = yyyy[0]
    else:
        timestamp_yearmonthday = "None"

    publishing_year = 'publishing_year="'+timestamp_yearmonthday+'"'

    return timestamp_yearmonthday, publishing_year