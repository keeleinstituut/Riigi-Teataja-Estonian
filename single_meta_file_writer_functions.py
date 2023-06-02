import os
from pathlib import Path
import openpyxl
import xlsxwriter
from bs4 import BeautifulSoup
import re 

def start_meta_file(metapath, filespath):        
    metaworkbook = xlsxwriter.Workbook(metapath, {'strings_to_urls': False}) # starts a new .xlsx file
    metaworksheet = metaworkbook.add_worksheet()
    metasheet_header_writer(metaworksheet)
    row_counter = 1

    for file in os.listdir(filespath):
        if file.endswith(".xml"):
            filepath = os.path.join(filespath, file)
            row_counter = write_to_metafile(filepath, metaworksheet, row_counter)

    metaworkbook.close() 



def write_to_metafile(filepath, metaworksheet, row_counter):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = f.read()

        data = re.sub(r'/"', r"/'", data)

        Bs_data = BeautifulSoup(data, "lxml")
        doc = Bs_data.find('doc')
        filename = doc.get('filename')
        id = doc.get('id')
        publishing_year = doc.get('publishing_year')
        domain_systematic = doc.get('domain_systematic')
        domain_Eurovoc = doc.get('domain_eurovoc')
        domain_KOV = doc.get('domain_kov')
        domain_foregin = doc.get('domain_foregin')
        issuer = doc.get('issuer')
        act_type = doc.get('act_type')
        text_type = doc.get('text_type')
        in_force_from = doc.get('in_force_from')
        in_force_until = doc.get('in_force_until')
        validity = doc.get('validity')
        publishing_note = doc.get('publishing_note')
        #title = doc.get('title')
        match = re.search(r'title="(.*?)" abbrevation', data)
        if match:
            title = match.group(1)
        else:
            title = doc.get('title')
        abbrevation = doc.get('abbrevation')
        act_passed = doc.get('act_passed')
        crawl_date = doc.get('crawl_date')
        crawl_time = doc.get('crawl_time')
        url = doc.get('url')

    # copying values from source xml file to destination xlsx file
    metaworksheet.write((row_counter), (0), filename)
    metaworksheet.write((row_counter), (1), id)
    metaworksheet.write((row_counter), (2), publishing_year)
    metaworksheet.write((row_counter), (3), domain_systematic)
    metaworksheet.write((row_counter), (4), domain_Eurovoc)
    metaworksheet.write((row_counter), (5), domain_KOV)
    metaworksheet.write((row_counter), (6), domain_foregin)
    metaworksheet.write((row_counter), (7), issuer)
    metaworksheet.write((row_counter), (8), act_type)
    metaworksheet.write((row_counter), (9), text_type)
    metaworksheet.write((row_counter), (10), in_force_from)
    metaworksheet.write((row_counter), (11), in_force_until)
    metaworksheet.write((row_counter), (12), validity)
    metaworksheet.write((row_counter), (13), publishing_note)
    metaworksheet.write((row_counter), (14), title)
    metaworksheet.write((row_counter), (15), abbrevation)
    metaworksheet.write((row_counter), (16), act_passed)
    metaworksheet.write((row_counter), (17), crawl_date)
    metaworksheet.write((row_counter), (18), crawl_time)
    metaworksheet.write((row_counter), (19), url)

    row_counter += 1

    return row_counter


def metasheet_header_writer(metaworksheet):
    # writes meta headers
    metaworksheet.write('A1', "filename")
    metaworksheet.write('B1', "id")
    metaworksheet.write('C1', "publishing_year")
    metaworksheet.write('D1', "domain_systematic")
    metaworksheet.write('E1', "domain_Eurovoc")
    metaworksheet.write('F1', "domain_KOV")
    metaworksheet.write('G1', "domain_foregin")
    metaworksheet.write('H1', "issuer")
    metaworksheet.write('I1', "act_type")
    metaworksheet.write('J1', "text_type")
    metaworksheet.write('K1', "in_force_from")
    metaworksheet.write('L1', "in_force_until")
    metaworksheet.write('M1', "validity")
    metaworksheet.write('N1', "publishing_note")
    metaworksheet.write('O1', "title")
    metaworksheet.write('P1', "abbrevation")
    metaworksheet.write('Q1', "act_passed")
    metaworksheet.write('R1', "crawl_date")
    metaworksheet.write('S1', "crawl_time")
    metaworksheet.write('T1', "url")
