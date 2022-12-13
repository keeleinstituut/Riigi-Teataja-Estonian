from FileWriter_functions.writer_functions import urlcollector
import os


act_URLs_path = 'acts_dec\RT-ET-081222-1-chron.xlsx' 
#metapath = r'RT-ET-test\Acts-meta.xlsx'
#meta_file_path = r'RT-ET-test\acts-meta.xlsx' 

current_dir = os.getcwd()
main_folder = "acts_dec"
meta_file_path = os.path.join(current_dir, main_folder, 'acts-meta.xlsx')
acts_folder = "acts"
file_path = os.path.join(current_dir, main_folder, acts_folder)


urlcollector(act_URLs_path, meta_file_path, file_path)
print("DONE")