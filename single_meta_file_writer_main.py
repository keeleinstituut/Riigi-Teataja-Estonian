import os
from single_meta_file_writer_functions import start_meta_file
import datetime

current_dir = os.getcwd()
current_month_text = datetime.datetime.now().strftime('%h')
main_folder = "".join(["acts_",current_month_text])
mainpath = os.path.join(current_dir, main_folder)
acts_folder = "acts"
filespath = os.path.join(mainpath, acts_folder)
date = datetime.datetime.today().date()
metapath = os.path.join(mainpath, "".join(['all-acts-meta-', str(date), '.xlsx']))

start_meta_file(metapath, filespath)
