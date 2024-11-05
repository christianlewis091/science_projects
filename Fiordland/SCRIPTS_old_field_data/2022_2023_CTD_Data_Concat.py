"""
CTD Data for the 2022 and 2023 Field Season is contained in the following directory, first on Sharepoint, then downloaded to my computer:
# 'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\Preliminary CTD data\SFCS2210_CTD data\ASCII' (2022 data)
# Documents/Field Seasons/SFCS2305 (2023 data)

The data do not have latitude and longitude comments in the SeaBird file, but I found them on this cruise MetaData file,
now contained here:
# 'H:\Science\Datasets\Fiordland\Past_Field_Season_Data' (2022 data)
# H:\Science\Datasets\Fiordland\Past_Field_Season_Data\sfcs2305_ctdData (2023 data)

I am going to merge and concat all the data together into a GO-SHIP type file that is easier for my to view in Python.
This will help me understand the hydrographic changes throughout the Fiordland, and help me determine where to sample.
"""

"""
First, change all the extensions to .csv so I can see them and python can read them easier
"""
import os
import glob
import shutil
import csv
import pandas as pd
import numpy as np


"""
First, move all the 2022 Data from ASC to TXT and move them to a new directory
"""
input_directory = r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\Preliminary CTD data\SFCS2210_CTD data\ASCII'
out_directory = r'C:\Users\clewis\IdeaProjects\GNS\Fiordland\OUTPUT\2022_2023_CTD_Data_Concat/STEP1_2022_CTD_TXT'

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
Similarly, lets move the 2023 Data from CNV to TXT and into a similarly new directory 
"""

input_directory = r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\sfcs2305_ctdData\otagoUniCtd\ou_Cnv'
out_directory = r'C:\Users\clewis\IdeaProjects\GNS\Fiordland\OUTPUT\2022_2023_CTD_Data_Concat/STEP1_2023_CTD_TXT'
#
# def copy_and_rename_files(source_directory, destination_directory):
#     # Change the current working directory to the source directory
#     os.chdir(source_directory)
#
#     # Find all files with the .asc extension in the source directory
#     for file in glob.glob("*.cnv"):
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

#
"""
Now, lets convert all of the 2022 files from their current format into nice Pandas Dataframes. The 2022 data needs to be
altered so that the white spaces are gone.
"""

# files = os.listdir(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland\OUTPUT\2022_2023_CTD_Data_Concat/STEP1_2022_CTD_TXT')
# file_list = np.unique(files)
#
# final_dataframe = pd.DataFrame()
# for i in range(0, len(file_list)):
#     # Read the text file
#     print(file_list[i])
#     with open(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP1_2022_CTD_TXT/{file_list[i]}', 'r') as file:
#         lines = file.readlines()
#
#     # Remove whitespace and split the lines into columns
#     data = [line.strip().split() for line in lines]
#
#     # Create a DataFrame
#     df = pd.DataFrame(data[1:], columns=data[0])
#     filename = file_list[i].replace(".txt", "")
#     df['FileName'] = filename
#
#     df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP2_2022_CTD_PANDAS/{filename}.xlsx')
#


"""
The data from 2023 needs to be altered differently because there is a preamble which has commented lined with # and * characters, 
as well as empty spaces. 
"""

# # read in the data that was created above, this line finds the directory
# files = os.listdir(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland\OUTPUT\2022_2023_CTD_Data_Concat/STEP1_2023_CTD_TXT')
#
# # make a list with all the file names
# file_list = np.unique(files)
#
# # create a dummy dataframe to store the data later
# final_dataframe = pd.DataFrame()
#
# # loop through each of the CTD files that we're going to alter in format
# for i in range(0, len(file_list)):
#
#     # open the file
#     with open(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP1_2023_CTD_TXT/{file_list[i]}', 'r') as fp:
#
#         """
#         This whole subsection below is to find where the preable ENDS and the data begins
#         """
#
#         # set columns for later
#         column_name = ['DepSM', 'Sal00', 'T090C', 'Sbeox0PS', 'Sbeox0Mg/L', 'WetStar','Density00','Flag']
#         column_name6 = ['DepSM', 'Sal00', 'T090C', 'Sbeox0PS', 'Sbeox0Mg/L', 'WetStar','Flag']
#         # attach these set columns to the dummy dataframe
#         dataframe1 = pd.DataFrame(columns=column_name)
#
#         # read all lines using readline()
#         lines = fp.readlines()
#
#         """
#         This for loop reads in each ROW of the file that we're currently looking at. If it finds that its NOT
#         the pre-amble, it will strip the whitespace from the data and attach it to a dataframe.
#         """
#         for row in lines:
#             # check if these characters exist in the data
#             word = '#'
#             word2 = '*'
#             #print(row.find(word))
#             # find() method returns -1 if the value is not found
#             # if found it returns index of the first occurrence of the substring
#             if row.find(word) != -1:  # we found the character
#                 x = 1
#             elif row.find(word2) != -1:  # we found the character
#                 x = 1
#             elif row == '\n':
#                 x = 1
#             else:
#                 data = [row.strip().split()]
#
#                 # I dont know why but a few of the datasheets are missing the pressure data,
#                 # so this try/except catches that by adding a different column name with 6 headers instead of 7
#                 try:
#                     data = pd.DataFrame(data, columns=column_name)
#                     dataframe1 = pd.concat([dataframe1, data]).reset_index(drop=True)
#
#                 except ValueError as e:
#                     data = pd.DataFrame(data, columns=column_name6)
#                     dataframe1 = pd.concat([dataframe1, data]).reset_index(drop=True)
#
#         filename = file_list[i].replace(".txt", "")
#         dataframe1['FileName'] = filename
#
#         dataframe1.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP2_2023_CTD_PANDAS/{filename}.xlsx')
#

"""
Now, we can concatonate the files from those two folders into one. AFTER this, we'll merge with the lat lon and comments data. 
"""

"""
First, move all the data into one shared folder
"""
#
# # Source and destination directories
# source2022_dir = 'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP2_2022_CTD_PANDAS'
# source2023_dir = 'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP2_2023_CTD_PANDAS'
# destination_dir = 'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP3_Concat'
#
# # move 2022 data
# files = os.listdir(source2022_dir)
# for file in files:
#     source_file = os.path.join(source2022_dir, file)
#     destination_file = os.path.join(destination_dir, file)
#     shutil.copyfile(source_file, destination_file)
#
# # move 2023 data
# files = os.listdir(source2023_dir)
# for file in files:
#     source_file = os.path.join(source2023_dir, file)
#     destination_file = os.path.join(destination_dir, file)
#     shutil.copyfile(source_file, destination_file)
#
# """
# Now we'll run the concat
# """
#
# files = os.listdir(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland\OUTPUT\2022_2023_CTD_Data_Concat/STEP3_Concat')
#
# # make a list with all the file names
# file_list = np.unique(files)
#
# # create a dummy dataframe to store the data later
# concat_df = pd.DataFrame()
#
# for i in range(0, len(file_list)):
#     sub_df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/STEP3_Concat/{file_list[i]}')
#     concat_df = pd.concat([concat_df, sub_df]).reset_index(drop=True)
#
# concat_df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/Concatonated_Data.xlsx')
#

"""
NOW, we can finally merge the CTD data with its metadata. PREP THE METADATA
The metadata is split between two files ('CTDBottleData', 'CTDSiteData') 

"""

metadata_2022 = pd.read_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/2022_CTD_metadata.xlsx')
metadata_2022['expedID'] = 'SFCS2210'

# # read in and match 2023 columns more or less with that of 2022
metadata_2023 = pd.read_csv('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/sfcs2305_ctdData/ctdBottleData.csv')
metadata_2023 = metadata_2023.rename(columns={'siteCode':'ctdSampleLocation',
                              'siteDescription':'locationDescription',
                              'sampleID': 'fileName',
                              'dropComments': 'comment'})
metadata_2023_2 = pd.read_csv('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/sfcs2305_ctdData/ctdSiteData.csv')
metadata_2023_2 = metadata_2023_2.rename(columns={'siteCode':'ctdSampleLocation',
                                              'siteDescription':'locationDescription',
                                              'sampleID': 'fileName',
                                              'dropComments': 'comment'})

metadata_total= pd.concat([metadata_2022, metadata_2023])
metadata_total = pd.concat([metadata_total, metadata_2023_2])
metadata_total = metadata_total.dropna(subset='latitude')
metadata_total = metadata_total.dropna(subset='fileName')

# save and get rid of NAN's
metadata_total.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/Metadata.xlsx')

"""
Final Merge
"""

#reimport the data
data = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/Concatonated_Data.xlsx')
metadata = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/Metadata.xlsx')
metadata = metadata.rename(columns={'fileName': 'FileName'})

# -----------------------------------------------------------
# Concatonated data needs "_bin" removed from where it exists
import re

# Define the pattern to match '_bin'
pattern = r'_bin'

names = data['FileName']
# Replace '_bin' with an empty string in each name
cleaned_names = [re.sub(pattern, '', name) for name in names]

data['FileName'] = cleaned_names

# 2023 Metadata has dashed where they should be underscores...
fixednames = metadata['FileName']
fixednames = fixednames.str.replace('-','_')
metadata['FileName'] = fixednames


# -----------------------------------------------------------

# list1 = np.unique(metadata['FileName'])
# list2 = np.unique(data['FileName'])
# print('METADATA')
# print(list1)
# print()
# print('DATA')
# print(list2)
# print()
# matches = [x for x in list1 if x in list2]
# print(matches)

# """
# GIANT ROADBLOCK: ALL (except 1) of the Filenames from MetaData and Data are off by the cast number...
# UPDATE: Fixed after i found additional excel sheet "ctdSiteData"
# """


final = pd.merge(metadata, data, on='FileName', how='outer')
final = final.dropna(subset='latitude')
final = final.dropna(subset='T090C')
final = final.drop(columns=['Unnamed: 0_x', 'siteNumber','device','dropNumber','waterDepth','bottleNumber','bottleWaterDepth','longitudev','Unnamed: 0.1_y','Unnamed: 0_y'])

final.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/FINAL_merged.xlsx')

listss = pd.DataFrame(np.unique(final['FileName']))
listss.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/FINAL_merged_uniqueCTDlist.xlsx')

#


#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# """
# The csv files all have annoying spaces in them which we need to fix before they can be read into python. Replaces all spaces with commas into a new directory:
# # (f'H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions_nospaces/{file_list[i]}')
#
# """
# import csv
# import pandas as pd
# import numpy as np
#
#
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
# final_dataframe.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/Fiordland_2022_Field_Season_Concat/concatd_file.xlsx')
#
#
# """
# Now merge the data with the metadata!
# """
#
# data = pd.read_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/Preliminary CTD data/SFCS2210_CTD data/ASCII/renamed_extensions/concatd_file.xlsx')
#
# # need to make sure the filename format is right
# data['fileName'] = data['FileName_ascII'].str.slice(0, 21)
#
# # now I can merge with the metadata
# metadata = pd.read_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/2022_CTD_metadata.xlsx')
# final = pd.merge(metadata, data, on='fileName', how='outer')
#
# final.to_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/merged.xlsx')
#
# """
# This worked ONLY for file types that have three segments in the name, as listed currently on 2022_CTD_metadata.xlsx.
# There are file types with names:
# SFCS2210_20221029_000
# and
# SFCS03112022_000
#
# The latter are not contained in the metadata file and therefore not merged with any ctd data.
#
# Re write the data by dropping nan = latitude and keep only where we have ALL Data
# """
# final_final = final.dropna(subset='latitude')
# final_final.to_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/2022_CTD_DATAMERGE_LEWIS.xlsx')
#
"""
May 3, 2024.
I may have found the CTD data for 2023 field season, which i can then add on top of the concatonated data above

I hvae downloaded the following folders onto my computer:
Originally in Sharepoint: Documents/Field Seasons/SFCS2305

Now on my computer: H:\Science\Datasets\Fiordland\Past_Field_Season_Data\sfcs2305_ctdData

Similar to above, the lat lons are contained in a differnt file (ctdbottledata.csv)
"""
#
# """
# First step is to convert the .cnv files with the data to python readable files
# """
#
# input_directory = r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\sfcs2305_ctdData\otagoUniCtd\ou_Cnv'
# out_directory = r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\sfcs2305_ctdData\otagoUniCtd\ou_Cnv\renamed_extensions'
#
# def copy_and_rename_files(source_directory, destination_directory):
#     # Change the current working directory to the source directory
#     os.chdir(source_directory)
#
#     # Find all files with the .asc extension in the source directory
#     for file in glob.glob("*.cnv"):
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
#
#
# """
# Now try to open all the text files, and concatonate the ctd data onto one file, attaching the filename on it as well
# """
#
# files = os.listdir(r'H:\Science\Datasets\Fiordland\Past_Field_Season_Data\sfcs2305_ctdData\otagoUniCtd\ou_Cnv\renamed_extensions')
# file_list = np.unique(files)
#
# final_dataframe = pd.DataFrame()
# # for i in range(0, len(file_list)):
# for i in range(0, len(file_list)):
#     # Read the text file
#     print(file_list[i])
#     with open(f'H:/Science/Datasets/Fiordland/Past_Field_Season_Data/sfcs2305_ctdData/otagoUniCtd/ou_Cnv/renamed_extensions/{file_list[i]}', 'r') as fp:
#
#         """
#         This whole subsection below is to find where the preable ENDS and the data begins
#         """
#
#         column_name = ['depSM', 'sal00', 't090C', 'sbeox0PS', 'sbeox0ML/L', 'wetStar','prSM','flag']
#         dataframe1 = pd.DataFrame(columns=column_name)
#         # read all lines using readline()
#         lines = fp.readlines()
#         for row in lines:
#             # check if these characters exist in the data
#             word = '#'
#             word2 = '*'
#             #print(row.find(word))
#             # find() method returns -1 if the value is not found
#             # if found it returns index of the first occurrence of the substring
#             if row.find(word) != -1:  # we found the character
#                 x = 1
#             elif row.find(word2) != -1:  # we found the character
#                 x = 1
#             elif row == '\n':
#                 x = 1
#             else:
#                 data = [row.strip().split()]
#                 data = pd.DataFrame(data, columns=column_name)
#
#                 dataframe1 = pd.concat([dataframe1, data]).reset_index(drop=True)
#
#         dataframe1['fileName'] = f'{file_list[i]}'
#     final_dataframe = pd.concat([dataframe1, final_dataframe]).reset_index(drop=True)
# #
# final_dataframe.to_excel(f'H:/Science/Datasets/Fiordland/Past_Field_Season_Data/sfcs2305_ctdData/otagoUniCtd/ou_Cnv/renamed_extensions/test.xlsx')
#









































