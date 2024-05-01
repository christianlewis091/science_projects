"""
CTD Data for the 2022 Field Season is contained in the following directory, first on Sharepoint, then downloaded to my computer:
# 'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\Preliminary CTD data\SFCS2210_CTD data\ASCII'

The data do not have latitude and longitude comments in the SeaBird file, but I found them on this cruise MetaData file,
now contained here:
# 'H:\Science\Datasets\Fiordland\Past_Field_Season_Data'

I am going to merge and concat all the data together into a GO-SHIP type file that is easier for my to view in Python.
This will help me understand the hydrographic changes throughout the Fiordland, and help me determine where to sample.
"""

"""
First, change all the extensions to .csv so I can see them and python can read them easier
"""
import os
import glob
import shutil
#
# input_directory = r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\Preliminary CTD data\SFCS2210_CTD data\ASCII'
# out_directory = r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\Preliminary CTD data\SFCS2210_CTD data\ASCII\renamed_extensions'
#
# def copy_and_rename_files(source_directory, destination_directory):
#     # Change the current working directory to the source directory
#     os.chdir(source_directory)
#
#     # Find all files with the .asc extension in the source directory
#     for file in glob.glob("*.asc"):
#         # Change the file extension from .asc to .csv
#         new_name = os.path.splitext(file)[0] + ".txt"
#         # Construct the full path for the destination file
#         destination_path = os.path.join(destination_directory, new_name)
#         # Copy the file with the new extension to the destination directory
#         shutil.copy(file, destination_path)
#         print(f"Copied {file} to {destination_path}")
#
# # Call the function to rename the files
# copy_and_rename_files(input_directory, out_directory)

"""
The csv files all have annoying spaces in them which we need to fix before they can be read into python. Replaces all spaces with commas into a new directory:
# (f'H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions_nospaces/{file_list[i]}')

"""
import csv
import pandas as pd
import numpy as np


# files = os.listdir('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions')
# file_list = np.unique(files)
#
# final_dataframe = pd.DataFrame()
# for i in range(0, len(file_list)):
#     # Read the text file
#     with open(f'H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions/{file_list[i]}', 'r') as file:
#         lines = file.readlines()
#
#     # Remove whitespace and split the lines into columns
#     data = [line.strip().split() for line in lines]
#
#     # Create a DataFrame
#     df = pd.DataFrame(data[1:], columns=data[0])
#     df['FileName_ascII'] = file_list[i]
#
#     final_dataframe = pd.concat([final_dataframe, df]).reset_index(drop=True)
#
# final_dataframe.to_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions/concatd_file.xlsx')
#

"""
Now merge the data with the metadata! 
"""

data = pd.read_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions/concatd_file.xlsx')

# need to make sure the filename format is right
data['fileName'] = data['FileName_ascII'].str.slice(0, 21)

# now I can merge with the metadata
metadata = pd.read_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/2022_CTD_metadata.xlsx')
final = pd.merge(metadata, data, on='fileName', how='outer')

final.to_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/merged.xlsx')

"""
This worked ONLY for file types that have three segments in the name, as listed currently on 2022_CTD_metadata.xlsx. 
There are file types with names: 
SFCS2210_20221029_000
and 
SFCS03112022_000

The latter are not contained in the metadata file and therefore not merged with any ctd data. 

Re write the data by dropping nan = latitude and keep only where we have ALL Data
"""
final_final = final.dropna(subset='latitude')
final_final.to_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/2022_CTD_DATAMERGE_LEWIS.xlsx')












