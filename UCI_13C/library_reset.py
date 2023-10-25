"""
Have downloaded all these files for EndNote but I hate endnote and want to use Zotero. Now I need to extract all the pdf's
from my Endnote library.
"""


import pandas.errors
from os import listdir
import shutil
from os.path import isfile, join
import numpy as np
import pandas as pd

#
folders = [f for f in listdir(r'H:\Science\Papers\ZOTERO\PDF')]
for i in range(0, len(folders)):
    file_name = [f for f in listdir(f'H:\Science\Papers\ZOTERO\PDF\{folders[i]}')]
    file_name = file_name[0]
    full_directory = f'H:\Science\Papers\ZOTERO\PDF\{folders[i]}\{file_name}'

    # Specify the path of the destination directory you want to copy the file into
    destination_directory = ('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/test')

    print(full_directory)
    print(destination_directory)
    print()
    print()

    # file_to_copy = file_to_copy[0]
    # Use the shutil.copy2() method to copy the file to the destination directory
    shutil.copyfile(full_directory, destination_directory)



# source_directory = r'H:\Science\Papers\ZOTERO\PDF'
# destination_directory = r'H:\Science\Papers\ZOTERO'
#
# folders = [f for f in listdir(source_directory)]
#
# for folder in folders:
#     folder_path = join(source_directory, folder)
#     files_to_copy = [f for f in listdir(folder_path)]
#
#     for file_to_copy in files_to_copy:
#         source_path = join(folder_path, file_to_copy)
#         destination_path = join(destination_directory, folder, file_to_copy)
#
#         # Use the shutil.copy2() method to copy the file to the destination directory
#         shutil.copy2(source_path, destination_path)
#
# print("PDF files copied to the destination directory.")