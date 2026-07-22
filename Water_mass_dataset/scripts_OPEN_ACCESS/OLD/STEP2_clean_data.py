"""
Concatonate all the data together and write it to a sheet
"""

# IMPORT MODULES
import gsw
import pandas.errors
from os import listdir
from os.path import isfile, join
import numpy as np
import seawater
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import time

# tracking how long it takes to run the script:
def time_function_execution(func):
    start_time = time.time()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{execution_time:.2f} (s)")

# Import water mass characterisitcs
wmc = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Emery' ,skiprows=2, comment='#')
wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley', skiprows=1, comment='#')

#
# A FUNCTION CREATED TO DEAL WITH SOME ISSUES IN GO-SHIP DATA: REMOVES SEPARATORS FROM A STRING
def remove_separators(value):
    if isinstance(value, str):
        stripped_value = value.strip()
        try:
            return int(stripped_value)
        except ValueError:
            try:
                return float(stripped_value)
            except ValueError:
                return stripped_value
    else:
        return value

"""
This section takes a bulk download of all the available GO-SHIP data and GLODAP data and merges it into one giant file
than can be used to run the for-loop to assign water masses.
"""

results_names = []
res_2 = []
filename = []
originname = []
onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\Bulk_Download') if isfile(join(r'H:\Science\Datasets\Hydrographic\Bulk_Download', f))]
goship_len = len(onlyfiles)

database = pd.DataFrame()
# for i in range(0,2):
for i in range(0, len(onlyfiles)):
    try:
        print(f'loop 1: {i/len(onlyfiles)}')
        # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
        data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\Bulk_Download\{onlyfiles[i]}', skiprows=2, comment='#')
        data['Project Name'] = 'GO-SHIP'
        data = data.applymap(remove_separators)
        if 'DELC14' in data.columns:
            data['Origin'] = f'{onlyfiles[i]}'
            database = pd.concat([database, data])
            results_names.append(str(onlyfiles[i]))

    except UnicodeDecodeError:
        x = 1
    except pandas.errors.ParserError:
        x = 1
#
"""
Now I'm adding on GLODAP data, see scrape_GLODAP.py
"""
# #
onlyfiles = [f for f in listdir(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2') if isfile(join(r'H:\Science\Datasets\Hydrographic\GLODAP_scrape2', f))]
glodap_len = len(onlyfiles)
for i in range(0, len(onlyfiles)):
    try:
        print(f'loop 2: {i/len(onlyfiles)}')
        # Read in the data in the file directory. Skip the first uncommented line (skiprows = 2). remove commented lines.
        data = pd.read_csv(f'H:\Science\Datasets\Hydrographic\GLODAP_scrape2\{onlyfiles[i]}', skiprows=2, comment='#')
        data['Project Name'] = 'GLODAP'
        data = data.applymap(remove_separators)
        if 'DELC14' in data.columns:
            data['Origin'] = f'{onlyfiles[i]}'
            database = pd.concat([database, data])
            results_names.append(str(onlyfiles[i]))

    except UnicodeDecodeError:
        x = 1
    except pandas.errors.ParserError:
        x = 1

database = database.dropna(subset='LONGITUDE')
database = database.dropna(subset='DELC14')
database = database.loc[database['DELC14'] != '/MILLE']
# remove missing data
database = database.loc[database['DELC14'].astype(int) > int(-998)]
print(database.head(5))
results = pd.DataFrame({"Filename": results_names})

with pd.ExcelWriter(r'C:\Users\clewis\IdeaProjects\GNS\Water_mass_dataset\output_OPEN_ACCESS\STEP2_clean_data\raw_data_watermassproject.xlsx') as writer:
    database.to_excel(writer, sheet_name='Database')
    results.to_excel(writer, sheet_name='FileErrors')


