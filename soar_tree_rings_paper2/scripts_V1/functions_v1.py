"""
Dec 16, 24
This scripts relates to the second iteration of our tree-ring based research on Southern Ocean change.
I am trying to be more "pythonic" in this version of the analysis, and part of that is simply better organization.
In this scripts, I'll keep all the functions I write - AND - I'll try to write more functions to do simple things, to
clean up the actual script itself
"""

import pandas as pd
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import re
import pandas.errors
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf

# A FUNCTION CREATED TO DEAL WITH SOME ISSUES IN GO-SHIP DATA: REMOVES SEPARATORS FROM A STRING. Written by ChatGPT
def clean_strings(strings):
    """
    Remove leading or trailing whitespace from all strings in a list.

    Args:
        strings (list of str): List of strings to clean.

    Returns:
        list of str: Cleaned list of strings with no leading or trailing whitespace.
    """
    return [s.strip() for s in strings]


def glodap_C14(name):
    """
    # Clean up GLODAP merged master file, for the purposes of this work.

    Args:
        name: the name used will only be used as a file name for a saved csv file

    Returns:
        nothign really...the function saves a csv file, which I'll read in later in a differnt script

    """
    df = pd.read_csv('H:\Science\Datasets\GLODAPv2.2023_Merged_Master_File.csv', dtype=str)
    t0 = len(df) # find the length, to compare with later when we have sliced and diced it to our needs
    df = df[['G2expocode', 'G2cruise', 'G2station', 'G2region', 'G2cast', 'G2year', 'G2month', 'G2day',
             'G2hour', 'G2minute', 'G2latitude', 'G2longitude','G2pressure','G2temperature','G2salinity',
             'G2salinityf', 'G2nitrate','G2salinityqc','G2c14', 'G2c14f', 'G2c14err','G2sigma0']] # simplify by dropping unnecessary columns
    flags = np.unique(df['G2c14f']) # are there flagged 14C data?

    df = df.loc[df['G2c14'].astype(float) > -999] # find 14C data that are greater than -999. One could similarly tell python that the 'nan' value is -999 but I'll leave this for now.
    df = df.loc[df['G2latitude'].astype(float) <= -5] # We want Southern Hemisphere data
    df = df.loc[df['G2pressure'].astype(float) < 100] # We want surface samples
    df = df.loc[df['G2c14'].astype(float) > -999] # remove nans
    df = df.loc[df['G2year'].astype(float) > 1979]   # we're interested in investigating post 1980s
    t1 = len(df)
    cruises = len(np.unique(df['G2expocode']))
    # print a report based on this data
    print()
    print(f'GLODAP FUNCTION REPORT.\n '
          f'The original lenght of the GLODAP data GLODAPv2.2023_Merged_Master_File.csv is {t0}.\n ' 
          f'After removing -999s (no data), filtering for south of 5S, shallower than 100m, and post 1980, the length is {t1},\n'
          f'Date ranges from {np.min(df["G2year"].astype(float))} to {np.max(df["G2year"].astype(float))}\n'
          f'C14 ranges from {np.min(df["G2c14"].astype(float))} to {np.max(df["G2c14"].astype(float))}\n'
          f'Lat ranges from {np.min(df["G2latitude"].astype(float))} to {np.max(df["G2latitude"].astype(float))}\n'
          f'This subset of data has been saved to, alongside a list of unique expocodes from this subset, of which there are {cruises}')

    expocodes = np.unique(df['G2expocode'])
    expocodes = pd.DataFrame({"G2expocode": expocodes})
    df.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/{name}.csv')
    expocodes.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/glodap_expocodes.csv')


"""
# Compare CCHDO https://cchdo.ucsd.edu/search?bbox=-180,-90,180,-40 data to GLODAP expocodes, so I can add cruises that arent captured by GLODAP.
The following was entered into the search box above to find the data in cchdo_results directory below
entered bbox -180,-90,180,-5, and 1980-2024.
"""
"""
Loop through the files that were output from CCHDO, and find where DELC14 is in the column headers. From there, concatonate all the data together. 
"""

def cchdo_C14(name):
    """
    # Concatonated up data output from CCHDO: https://cchdo.ucsd.edu/search/advanced
    # I put into the "Advanced Search"
    # bbox=-180,-90,180,-40
    # Starts After 1980
    # Starts Before 2024
    But the data is still "messy" and will be cleane by the next function

    Args:
        name: the name used will only be used as a file name for a saved csv file

    Returns:
        nothign really...the function saves a csv file, which I'll read in later in a differnt script

    """
    cchdo_data = pd.DataFrame()
    onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\cchdo_results') if isfile(join(r'H:\Science\Datasets\Hydrographic\cchdo_results', f))]
    for i in range(0, len(onlyfiles)):
        data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\cchdo_results/{onlyfiles[i]}', skiprows=2, comment='#')
        if 'DELC14' in data.columns:
            cchdo_data = pd.concat([cchdo_data, data]) # if C14 data is in the file, add it to the initialized database
            # print(len(cchdo_data))

    cchdo_data.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/{name}_messy.csv')
    print()
    print(f'CCHDO FUNCTION REPORT.\n '
          f'Messy version of data includes a row of units, and some "END DATA" row at the end.\n '
          f'{len(onlyfiles)} files read in and concatenated')


def cchdo_cleaning():
    """
    # Concatonated data from cchdo_c14 function needs to be cleaned
    # we also need to filter it the same way we filter the GLODAP DATA

    Args:
        name: the name used will only be used as a file name for a saved csv file

    Returns:
        nothign really...the function saves a csv file, which I'll read in later in a differnt script

    """
    cchdo = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/cchdo_dataset_messy.csv',low_memory=False)
    t0 = len(cchdo)
    cchdo = cchdo.dropna(subset='EXPOCODE') # remove unit line
    cchdo = cchdo.loc[cchdo['EXPOCODE'] != 'END_DATA'] # remove END_DATA row
    cchdo['EXPOCODE'] = cchdo['EXPOCODE'].astype(str)
    cchdo['EXPOCODE'] = clean_strings(cchdo['EXPOCODE']) # remove white space from EXPOCODES

    cchdo = cchdo.loc[cchdo['DELC14'].astype(float) > -999] # find 14C data that are greater than -999. One could similarly tell python that the 'nan' value is -999 but I'll leave this for now.
    cchdo = cchdo.loc[cchdo['LATITUDE'].astype(float) <= -5] # We want Southern Hemisphere data
    cchdo = cchdo.loc[cchdo['CTDPRS'].astype(float) < 100] # We want surface samples
    t1 = len(cchdo)
    cchdo.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/cchdo_clean.csv')

    cchdo_expocodes = np.unique(cchdo['EXPOCODE'])
    cchdo_expocodes = pd.DataFrame({'EXPOCODE': cchdo_expocodes})
    cchdo_expocodes.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/cchdo_expocodes.csv')
    print()
    print(f'CCHDO_CLEANING REPORT.\n '
      f'The messy CCHDO dataaset had length {t0} \n '
      f'After filtering the same was as GLODAP, for south of 5S, and shallower than 100m, CCHDO has lentgh {t1}\n'
      f'Date ranges from {np.min(cchdo["DATE"].astype(float))} to {np.max(cchdo["DATE"].astype(float))}\n'
      f'C14 ranges from {np.min(cchdo["DELC14"].astype(float))} to {np.max(cchdo["DELC14"].astype(float))}\n'
      f'Lat ranges from {np.min(cchdo["LATITUDE"].astype(float))} to {np.max(cchdo["LATITUDE"].astype(float))}\n'
      )

# TODO
"""
When checking via the map, I found a lot of duplicate GLODAP CCHDO cruises that WERE duplicates and not captured here. I may be better off just dealing with it manually...
Make one map per year, make sure nothing looks crazy
"""

def glodap_cchdo_merge():
    """
    # Reads in GLODAP and CCHDO datasets; cleans up data headers, merges files together

    Args:
        None

    Returns:
        merged dataset of GLODAP and CCHDO
    """
    cchdo = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/cchdo_clean.csv')
    glodap = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/glodap_v1.csv')

    # the column names need to be made the same
    # print(list(cchdo.columns))
    # print(list(glodap.columns))

    # here is the list of GLODAP columns
    glodap = glodap[['Unnamed: 0', 'G2expocode', 'G2cruise', 'G2station', 'G2region',
                     'G2cast', 'G2year', 'G2month', 'G2day', 'G2hour', 'G2minute',
                     'G2latitude', 'G2longitude', 'G2pressure', 'G2temperature', 'G2salinity',
                     'G2salinityf', 'G2nitrate', 'G2salinityqc', 'G2c14', 'G2c14f', 'G2c14err', 'G2sigma0']]
    glodap['Origin'] = 'GLODAP'
    # First, I'll cut off loads of columns to simplify working with CCHDO dataset.
    cchdo = cchdo[['EXPOCODE', 'SECT_ID', 'STNNBR','DATE','LATITUDE',
                   'LONGITUDE', 'DEPTH', 'CTDPRS', 'CTDTMP',
                   'SALNTY','THETA',
                   'NITRAT', 'DELC14', 'TCARBN','PCO2']]
    cchdo['Origin'] = 'CCHDO'

    # then I'll change the column names to work with GLODAP above.
    cchdo = cchdo.rename(columns={"EXPOCODE": "G2expocode",
                                  "DATE": "G2year",
                                  "LATITUDE":"G2latitude",
                                  "LONGITUDE":"G2longitude",
                                  "CTDPRS":"G2pressure",
                                  "CTDTMP":"G2temperature",
                                  "SALNTY":"G2salinity",
                                  "NITRAT":"G2nitrate",
                                  "DELC14":"G2c14"})

    df = glodap.merge(cchdo, how='outer')

    # fix date formatting so each one has a simply year
    to_fix_date = df['G2year'].astype(str)
    to_fix_date = to_fix_date.str.slice(0,4)
    df['Date_sliced'] = to_fix_date

    # Use CSV file for future work
    df.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/cchdo_glodap_merged.csv')


def map_check():
    """
    # Reads merged data file from above. Look through each year, find where there are duplicate cruises

    Args:
        None

    Returns:
        merged dataset of GLODAP and CCHDO
    """
    df = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/cchdo_glodap_merged.csv')
    years = np.unique(df['Date_sliced'].astype(float))

    # Loop through the years and plot maps in each subplot
    for i in range(0, len(years)):
        plt.figure(figsize=(10, 10))
        ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))

        this_year_cchdo = df.loc[(df['Date_sliced'] == years[i].astype(float)) & (df['Origin'] == 'CCHDO')]
        c_c = np.unique(this_year_cchdo['G2expocode'])


        this_year_glodap = df.loc[(df['Date_sliced'] == years[i].astype(float)) & (df['Origin'] == 'GLODAP')]
        g_c = np.unique(this_year_glodap['G2expocode'])


        ax.add_feature(cf.OCEAN)
        ax.add_feature(cf.LAND, edgecolor='black')
        ax.gridlines()
        ax.set_title(f"Year: {years[i]}", fontsize=8)  # Add year as title to each subplot

        ax.scatter(this_year_cchdo['G2longitude'].values, this_year_cchdo['G2latitude'].values, transform=ccrs.PlateCarree(), label='CCHDO')  # Data is in lat/lon format))
        ax.scatter(this_year_glodap['G2longitude'].values, this_year_glodap['G2latitude'].values, transform=ccrs.PlateCarree(), label='GLODAP')  # Data is in lat/lon format))
        ax.set_global()
        ax.legend()
        print()
        print(f"Year is {years[i]}")
        print(f"This years CCHDO cruises: {c_c}")
        print(f"This years glodap cruises: {g_c}")
        # Adjust layout for better spacing
        plt.tight_layout()
        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2/output_V1/dataset_generation_v1/map_check/{years[i]}.png',
                    dpi=300, bbox_inches="tight")
        plt.close()











