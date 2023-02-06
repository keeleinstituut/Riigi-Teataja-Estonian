import os
from single_meta_file_writer_functions import start_meta_file

current_dir = os.getcwd()
main_folder = "acts_jan"
mainpath = os.path.join(current_dir, main_folder)
filespath  = os.path.join(mainpath, "acts meta")
metapath = os.path.join(mainpath, 'all-acts-meta-2023-01-27.xlsx')

start_meta_file(metapath, filespath)
