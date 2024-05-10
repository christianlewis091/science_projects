"""
February 4, 2024

I want to be able to compare beam currents from Kapnui's, Oxalics, and secodary standards from RG20, to RCM10.
The first thing I want to do is write a short function/code-block to pull the data from the I: drive from old wheels.

For each wheel of interest, the ORIGINAL .out file is moved from the I: drive, to here:
(H:\Science\Current_Projects\06_small_14C_at_GNS\Data\historical_RG20_data), and converted to xlsx.

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
# #
# onlyfiles = [f for f in listdir(f'H:\Science\Datasets\RCM10_testing') if isfile(join(f'H:\Science\Datasets\RCM10_testing', f))]
#
#
# f = pd.read_fwf(r'I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3450-3499\TW3450\TW3452_p1.out', delimiter = "\t")
# print(f)


"""
TW3509_1 was another RCM10 test
"""
# open AMS data
df = pd.read_csv(r'H:\Science\Current_Projects\04_ams_data_quality\Small_samples\TW3509_1.csv', skiprows=3)

# Open Metadata. I HAD TO OPEN THE TXT FILE IN EXCEL TO DEAL WTH THE COMMA SEPERATOR
mass = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\Small_samples\TW3509.wheel.xlsx')

# Merge them together
df = df.merge(mass, how='outer')

# Check it worked.
# df.to_excel(r'H:\Science\Current_Projects\04_ams_data_quality\Small_samples\merge_out.xlsx')

pos = np.unique(df['position'])

for i in range(0, len(pos)):
    target = df.loc[df['position'] == pos[i]].reset_index(drop=True)
    target['Rotation'] = target.index # the run #'s are cumulative. I want to see data per rotation

    plt.scatter(target['C[mg]'], target['12CLEcurr'])
plt.show()
#
