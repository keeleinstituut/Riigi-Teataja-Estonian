import os
from pathlib import Path
import openpyxl
import xlsxwriter
from URLcollector_functions.type_identifier_functions import metasheet_header_writer

def start_meta_file(metapath, filespath):    
    metafileslist = get_metafiles_as_list(filespath)
    
    metaworkbook = xlsxwriter.Workbook(metapath, {'strings_to_urls': False}) # starts a new .xlsx file
    metaworksheet = metaworkbook.add_worksheet()
    metasheet_header_writer(metaworksheet)
    row_counter = 0

    for url in metafileslist:
        row_counter = write_to_metafile(url, metaworksheet, row_counter)

    metaworkbook.close() 


def get_metafiles_as_list(filespath):
    metafileslist = []
    for file in os.listdir(filespath):
        if file.endswith(".xlsx"):
            metafileslist.append(os.path.join(filespath, file))
    
    return metafileslist


def write_to_metafile(path, metaworksheet, row_counter):
    xlsx_file = Path(path)
    wb_obj = openpyxl.load_workbook(xlsx_file) 
    sheet = wb_obj.active

    rows_in_sheet = sheet.max_row - 1
    colums = sheet.max_column
    rows = rows_in_sheet + row_counter

    # copying the cell values from source excel file to destination excel file
    for i in range (1, rows_in_sheet + 1):
        for j in range (1, colums + 1):
            # reading cell value from source excel file
            cell = sheet.cell(row = i+1, column = j)

            # writing the read value to destination excel file
            metaworksheet.write((i+row_counter), (j-1), cell.value)

    return rows


