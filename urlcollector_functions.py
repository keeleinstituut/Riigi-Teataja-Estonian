from pathlib import Path
import openpyxl

import os

CURR_DIR = os.path.dirname(os.path.realpath(__file__))
print(CURR_DIR)

path = 'RT-ET_test\RT-ET-allacts.xlsx'
newpath = os.path.join(CURR_DIR,path)
print(newpath)

def urlcollector(path):
    xlsx_file = Path(path)
    print(xlsx_file)
    wb_obj = openpyxl.load_workbook(xlsx_file) 
    sheet = wb_obj.active
    URLlist = []
    
    # loeb ridahaaval ja kirjutab URLid listi
    for row in sheet.iter_rows():
        for cell in row:
            URLlist.append(cell.value)
    wb_obj.close() 
    
    return URLlist

#x = urlcollector(path)
#print(x)