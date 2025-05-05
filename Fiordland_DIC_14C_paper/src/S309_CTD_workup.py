"""
This script procseses the CTD data from S309 for later use.
Verified and run on May 2 2025
"""

"""
HIGH RES COASTLINE!
https://ctroupin.github.io/posts/2019-09-02-fine-coast/
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import os
import glob
import shutil
import pandas as pd
import numpy as np

def copy_and_rename_files(source_directory, destination_directory):
    # Change the current working directory to the source directory
    os.chdir(source_directory)

    # Find all files with the .asc extension in the source directory
    for file in glob.glob("*.cnv"):
        # Change the file extension from .asc to .csv
        new_name = os.path.splitext(file)[0] + ".txt"
        # Construct the full path for the destination file
        destination_path = os.path.join(destination_directory, new_name)
        # Copy the file with the new extension to the destination directory
        shutil.copy(file, destination_path)
        print(f"Copied {file} to {destination_path}")

# # Call the function to rename the files
# copy_and_rename_files(input_directory, out_directory)

"""
I'm drawing functions from my SFCS2405_CTD_dataworkup.py to analyze the CTD data
"""

input_directory1 = r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\S309_CTD_raw'
out_directory1 = r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step1'

copy_and_rename_files(input_directory1, out_directory1)


"""
STEP2. Dealwith Preamble
"""

# read in the data that was created above, this line finds the directory
files = os.listdir(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step1')

# make a list with all the file names
file_list = np.unique(files)

# create a dummy dataframe to store the data later
final_dataframe = pd.DataFrame()

# loop through each of the CTD files that we're going to alter in format
for i in range(0, len(file_list)):

    # open the file
    with open(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step1/{file_list[i]}', 'r') as fp:

        """
        This whole subsection below is to find where the preable ENDS and the data begins
        """

        # set columns for later
        column_name = ['depSM', 'prDM', 'timeJ', 'timeH', 'timeM', 'timeM','nbf','latitude','longitude','t090C','t190C','pottempt090C','potemp190C','COSm','C1sm','sal00','sal11','sigma00','sigma11','sbox0Mm/Kg','sbox1Mm/kg','sbeox0PS','sboeox1PS','f1ECO-AFL','turbWETntu0','par','svCM','sbeox0MLL','altM','flag']

        # attach these set columns to the dummy dataframe
        dataframe1 = pd.DataFrame(columns=column_name)

        # read all lines using readline()
        lines = fp.readlines()

        """
        This for loop reads in each ROW of the file that we're currently looking at. If it finds that its NOT
        the pre-amble, it will strip the whitespace from the data and attach it to a dataframe.
        """
        for row in lines:
            # check if these characters exist in the data
            word = '#'
            word2 = '*'
            #print(row.find(word))
            # find() method returns -1 if the value is not found
            # if found it returns index of the first occurrence of the substring
            if row.find(word) != -1:  # we found the character
                x = 1
            elif row.find(word2) != -1:  # we found the character
                x = 1
            elif row == '\n':
                x = 1
            else:
                data = [row.strip().split()]
                data = pd.DataFrame(data, columns=column_name)
                dataframe1 = pd.concat([dataframe1, data]).reset_index(drop=True)

        filename = file_list[i].replace(".txt", "")
        dataframe1['FileName'] = filename

        # these casts seem to incude the downcast AND the upcast.
        # I want to only include the downcast.

        dataframe1.to_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step2/{filename}.xlsx')

"""
Now we'll run the concat STEP3
"""

files = os.listdir(r'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step2/')

# make a list with all the file names
file_list = np.unique(files)

# create a dummy dataframe to store the data later
concat_df = pd.DataFrame()

for i in range(0, len(file_list)):
    sub_df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step2/{file_list[i]}')
    concat_df = pd.concat([concat_df, sub_df]).reset_index(drop=True)

concat_df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\s309_step3/Concatonated_CTD_SONNE.xlsx')
concat_df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/S309_CTD_DATA_FINAL.xlsx')

"""
Check they match the right locations on the map
"""

concat_df = pd.read_excel(f'H:\Science\Datasets\Fiordland\RVSONNE\STEP3/Concatonated_CTD_SONNE.xlsx')
print(concat_df.columns)

fig = plt.figure(figsize=(16, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent((166.3, 168.25, -46.0, -44))
coast = cf.GSHHSFeature(scale="l")
ax.add_feature(coast)

filenames = np.unique(concat_df['FileName'])

for i in range(0, len(filenames)):
    sub1 = concat_df.loc[concat_df['FileName'] == filenames[i]].reset_index()
    lat1 = sub1['latitude']
    lat1 = lat1[0]
    lon1 = sub1['longitude']
    lon1 = lon1[0]

    sc = ax.scatter(lon1, lat1, color='black', transform=ccrs.PlateCarree(), label='RVSONNE', marker='o')

plt.show()

"""
LOCATIONS ON MAP LOOK GOOD! 
"""











