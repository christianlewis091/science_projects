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

"""
I'm going to record my notes and thought process alongside the code in these triple apostrophe comments. 

First, I'm going to go back into CALAMS and look at LUC1, TW3536. 
Do I see any obvious problem? 
The first thong to note about TW3536 is that the primary standards don't look to hot. One has 0.996, another 0.997, and 1.002.
We've done better. 

But, the real problem was the "overcorrection" of small oxalics (cathy's secondary oxalics for RPO). 
In order for me to check this, and compare it (most easily) to all other smalls, I need to run the CALAMS eqn inside python
1. Has Kilho done this, and can I take an eqn from his excel sheet? 
1.1 I can't simply calculate RTS in python without dealing with the calibration curve. 
1.2 I don't know what to make of Kilho's sheet, there is no notes or documentation, just numbers everywhere. 
1.3 What IS potentially useful is simply the wheels he has analyzed. 

I must go back and correct all important small wheels in CALAMS Mode 5; then I can go back and anaylze them by mergeing their 
raw data (.out file) with their RTS data (from CALAMS)

Below is a list of the wheels I need to start with: 
TW3536 (LUC1)
TW3532 (RCM5)
TW3524 (RCM4)
TW3514 (RCM3)
TW3509 (RCM2)
TW3504 (RCM1)

I am manually dragging the .csv files (which get read into RLIMS) into a new folder for this analysis -> 
#'C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data'

Below, I am going to aggregate all these excel sheets (the out files) for easier viewing, 
I'm also going to aggregate the .csv files
"""

"""
The .out files
"""
# Define the path and file extension
directory_path = r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data\*.out"

files = glob.glob(directory_path, recursive=True)

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

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\output\dot_out_data.xlsx')

"""
the .csv files
!!! MANUALLY ADD COLUMN HEADERS FIRST!!!
"""
# Define the path and file extension
directory_path = r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis\selected_data\*.csv"

files = glob.glob(directory_path, recursive=True)

df = pd.DataFrame()
# Iterate through each file and open it
for file_path in files:
    with open(file_path, 'r') as file:
        data = pd.read_csv(file)

        # Add only the filename as a new column
        data['Filename'] = os.path.basename(file_path)

        # Append to the main DataFrame
        df = pd.concat([df, data], ignore_index=True)

        print(f"Total rows in the combined DataFrame: {len(df)}")

df.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\November_2024_fractionation_analysis\output\dot_csv_data.xlsx')


"""
TOMORROW...
A. Merge the data collated above with the "WHAT IS IT?" data. Which ones are oxalics, which ones are unks, blah blah
B. Plot them. What is the spread of oxalics in the small range? Do we have a gaussian distribution at the small range like XXU?
C. Go from there...
"""

































