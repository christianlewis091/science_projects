"""
August 21, 2024
Jack sent me some cnv files of cruise data from DBT. Lets see if I can get it into a readable file...

"""

"""
First step is to convert the .cnv files with the data to python readable files
"""
import matplotlib.pyplot as plt
import os
import glob
import shutil
import csv
import pandas as pd
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf

"""
STEP1. Change to txt
"""

input_directory = r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\SFCS2405_CTD_raw'
out_directory = r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step1'
#
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

# Call the function to rename the files
copy_and_rename_files(input_directory, out_directory)

"""
STEP2. Dealwith Preamble
"""

# read in the data that was created above, this line finds the directory
files = os.listdir(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step1')

# make a list with all the file names
file_list = np.unique(files)

# create a dummy dataframe to store the data later
final_dataframe = pd.DataFrame()

# loop through each of the CTD files that we're going to alter in format
for i in range(0, len(file_list)):

    # open the file
    with open(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step1/{file_list[i]}', 'r') as fp:

        """
        This whole subsection below is to find where the preable ENDS and the data begins
        """

        # set columns for later
        column_name = ['DepSM', 'bpos', 'T090C', 'Sal00', 'Sbeox0Mg/L', 'sbeox0PS','fls','prdM','flag']

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

        dataframe1.to_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step2/{filename}.xlsx')


"""
Now we'll run the concat STEP3
"""

files = os.listdir(r'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step2/')

# make a list with all the file names
file_list = np.unique(files)

# create a dummy dataframe to store the data later
concat_df = pd.DataFrame()

for i in range(0, len(file_list)):
    sub_df = pd.read_excel(f'H:\Science\Datasets\Fiordland\SFCS2405_CTD\STEP2/{file_list[i]}')
    concat_df = pd.concat([concat_df, sub_df]).reset_index(drop=True)

concat_df.to_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step3/Concatonated_Data.xlsx')

"""
Add lat lons from a metadata file
"""

# # first a rough check I was sent the propoer profiles. Do they aligm on the maP?
# lat lons are not in original CTD profiles, so I have to mereg them from a metadata file
mets = pd.read_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\metadata.xlsx', comment='#')
concat_df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step3/Concatonated_Data.xlsx')
concat_df2 = pd.merge(mets, concat_df, on='FileName')
concat_df2.to_csv(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_CTD_DATA_FINAL.csv')

"""
Check they match the right locations on the map
"""

concat_df = pd.read_csv(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2405_CTD_DATA_FINAL.csv')
print(concat_df.columns)

filenames = np.unique(concat_df['FileName'])

for i in range(0, len(filenames)):

    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent((166.3, 168.25, -46.0, -44))
    coast = cf.GSHHSFeature(scale="l")
    ax.add_feature(coast)

    sub1 = concat_df.loc[concat_df['FileName'] == filenames[i]].reset_index()
    lat1 = sub1['Lat']
    lat1 = lat1[0]
    lon1 = sub1['Lon']
    lon1 = lon1[0]

    sc = ax.scatter(lon1, lat1, transform=ccrs.PlateCarree(), label=f'{filenames[i]}')
    plt.legend()

    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step3/map_checks/{filenames[i]}', dpi=300, bbox_inches="tight")
    plt.close()


"""
Greer is debating with me about whether or not there is an error
"""

mets = pd.read_excel(r'H:\Science\Datasets\Fiordland\SFCS2405_CTD\metadata.xlsx', comment='#')
filenames = np.unique(mets['FileName'])

for i in range(0, len(filenames)):

    fig = plt.figure(figsize=(16, 8))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent((166.3, 168.25, -46.0, -44))
    coast = cf.GSHHSFeature(scale="l")
    ax.add_feature(coast)

    sub1 = mets.loc[mets['FileName'] == filenames[i]].reset_index()
    lat1 = sub1['Lat']
    lat1 = lat1[0]
    lon1 = sub1['Lon']
    lon1 = lon1[0]

    sc = ax.scatter(lon1, lat1, transform=ccrs.PlateCarree(), label=f'{filenames[i]}')
    plt.legend()

    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\intermediate\sfcs2405_step3/map_checks/gg_cbl/{filenames[i]}', dpi=300, bbox_inches="tight")
    plt.close()









#