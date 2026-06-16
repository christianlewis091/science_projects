import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
today = date.today()

"""
We are working on an AMS data quality paper that was originally started by Albert Zondervan, who is not at uOttawa.
Jocelyn wants to rerun the scripts that created the plots, and numbers for the data quality paper; however, we
are concerned that many data in the record should have quality flags, and currently do not. This script's goal is to
help me identify and flag those data.

January 8, 2024
Re-exporting the full RLIMS dataset to run the script and will keep updating here. 



September 12, 2023
I'm splitting the document into different "steps" that I can use as the flags to help identify where flags came in. 


September 8, 2023:
Initialization of this file. Creating the folders where the data will be stored:

Location of Original Data
H:\Science\Datasets\Alberts_dataquality

Location of Output
# C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output

Flags we will enter are as follows:
in general, where X can be any flag in that column:
A column 1 flag "X.." indicates the measurement is BAD and should not be used anymore, a "hard" flag
A column 2 flag ".X." is a soft flag. The measurement needs some looking at before further use
A column 3 flag "..X" is informational

# X can be any of the following, the following are previously used flags:
# "..T" = Test sample
# "A.." = Analytical problem
# "N.." = Sampling problem for Airs
# ".F." = Contains fossil fuel pollution
# "..D" = Data has been updated since publication
# "..P" = Data is preliminary and needs to be checked

PHASES OF THIS FILE: 
><>><>><>><>><>><>><>><>
PHASE 1: IDENTIFY INNOCUOUS JOB NOTES
><>><>><>><>><>><>><>><>
Label all jobNOTES that are NOT BAD, by filtering and labeling things that are clearly innocuous, such 
as, things that are only digits, or, the things listed below.  
Phase 1 adds "filtering flags" to the data based on what's written in the job notes
# 1 == HAD NO DATA IN JOB NOTES
# 2 == ONLY ONE CHARACTER
# 3 == CONTAINS THE WORD TEST
# 4 == ONLY CONTAINS NUMBERS
# 5 == DESCRIBES X/Y (1 of 2, 3 of 6, etc)
# 6 == DESCRIBES ANYTHING COMTAINING ONLY EA "XYZ"
# 7 == DESCRIBES A "COMMON DEPEAT" (i.e., "skip acid etch", or "notify client

Adding a soft flag to anything that contains test. 

><>><>><>><>><>><>><>><>
PHASE 2: MANUALLY CHECK REST OF JOB NOTES
><>><>><>><>><>><>><>><>
There are of course heaps of job notes that don't fit into the strict labeling categories I've made in phase 1, 
although phase 1 did capture 75% of the notes, 25% remain and need manual checking. I went through these and added 
some labels that I thought were appropriate at the time. This can be found on this sheet: 

'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/manual_checks.csv'

By mergeing it back to the data from phase 1 and re-labeling for cleaner data, we can have a full, better dataset
I am flagging anything that says "Discuss" with a soft flag, and anything with "Remove" with a hard flag

><>><>><>><>><>><>><>><>
PHASE 3: Plot the data to look for outliers (THE ROUGH IN) 
><>><>><>><>><>><>><>><>

><>><>><>><>><>><>><>><>
PHASE 4: Plot the data to look for outliers (zooming into each "known") 
><>><>><>><>><>><>><>><>
Phase 4 outliers/labels overwrite those from phase 3.
400 flags added to the data

"""

# IMPORT THE DATA FILE
# this file contains all of RLIMS as downloaded from one of our most recent wheels (today is 21/12/2023; Dec 21),
# but the file was moved to my C: drive
df = pd.read_csv(r'H:\Science\Datasets\data_quality1.csv')
# df = pd.read_csv(r'H:\Science\Papers\In Prep Work\2023_Zondervan_DataQuality\simplified RLIMS dataset.csv')
# I initially wrote the following 4 scripts using a downloaded file from Albert. His export script has since gone
# Missing, and some of the variable names have changed. I can either 1) change all the variable names in the following
# 4 scripts, or simply rename the values here, to match the old ones. I choose the latter.
# df = df[['R_number','TW','TP','Quality Flag','AMS Category ID XCAMS','Ratio to standard','Ratio to standard error','Date Run','JOB Notes','sample']]
df = df.rename(columns={"JOB Notes": "jobNOTES", "AMS Category ID XCAMS": "AMScategID", "Ratio to standard": "RTS", "Ratio to standard error": "RTSerr"})
# TODO upon return in January:
# TODO 1) Re-export the file above, but this time make sure to include the field EArun. This allows me to filter for Ea vs Sealed tube later on
# TODO 2) Re-run all the scripts, without removing any data yet!
# TODO 3) after re-running, decide where data should be removed, and then import those NEW FLAGS back into RLIMS


length_check = df
# INITIAlZE A COLUMN FOR ME TO ADD THINGS TO FILTER ON LATER
df['CBL_Filtering_Category'] = -999

"""
><>><>><>><>><>><>><>><>
PHASE 1: IDENTIFY INNOCUOUS JOB NOTES
><>><>><>><>><>><>><>><>
"""
# See documentation above for details on 1-7 labeling scheme
# Checking for "must contain -999" because if it doesn't it's already been labeled

test = df.loc[df['jobNOTES'].isnull()]

print(len(test))