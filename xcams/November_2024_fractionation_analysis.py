"""
Jocelyn would like the answers to the following questions

Is there a pattern in recent dropoffs in currents and isotope ratios, leading to fractionation, and issues forcing us to use Mode 1 vs Mode 5.
How do we deal with small samples with respect to new concerns such as describes above?
See Jacob's data/recent wheels, and cathy's recent wheels.

Is there actual overcorrection in the data, or is within the error, and it's actually no problem?
If we "pretend" correct Kauri and Firi-D from recent wheels, do they look OK?

How will the foram test wheel look? This wheel is designed to understand if we're able to run some small samples for a student with small foram samples.

This will start by the handover between KS and CBL, started with the Excel sheet in the following file directory:
I:\C14Data\Graphite\RCM10\XCAMS\TW3532 analysis.xlsx

The first thing I'd like to do is forge a pathway to import XCAMS runlogs into python, without having to copy and paste manually. This will make things easier, and simpler to reconstruct later on.
"""

import glob
import pandas as pd
import os

# Define the path and file extension
directory_path = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3450-3499\**\*.out"
directory_path2 = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3500-3549\**\*.out"
# Get all .dat files in the specified directory and its subdirectories

files = glob.glob(directory_path, recursive=True)
files2 = glob.glob(directory_path2, recursive=True)

df = pd.DataFrame()
# df = pd.DataFrame(columns=['timestamp','run','(block)','position','TP#','(stnd)','14Ccnts','(cnts)','Tdetect','BeacGen','BeacROI','LTF','(%DT)','13Ccurr','(13Ccurr_stdev)','(13Ctime)','12Ccurr','(12Ctime)','12CLEcurr','(12CLEtime)','(CathCurr)','(MPAtime)','(MPAcnts)','(MPAtime)','(MPAcnts)','(MPAtime)','(MPAcnts)'])
# Iterate through each file and open it
for file_path in files:
    with open(file_path, 'r') as file:
        # Skip the first three lines
        for _ in range(3):
            next(file)

        # Read the rest of the file
        data = pd.read_csv(file, sep='\t', engine='python')

        # Add only the filename as a new column
        data['Filename'] = os.path.basename(file_path)

        # Append to the main DataFrame
        df = pd.concat([df, data], ignore_index=True)

        print(f"Total rows in the combined DataFrame: {len(df)}")

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\output\data.xlsx')












