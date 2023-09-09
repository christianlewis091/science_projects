import pandas as pd
import numpy as np
# import warnings
# import xlsxwriter
# from datetime import date
# warnings.simplefilter(action='ignore')

"""
We are working on an AMS data quality paper that was originally started by Albert Zondervan, who is not at uOttawa.
Jocelyn wants to rerun the scripts that created the plots, and numbers for the data quality paper; however, we
are concerned that many data in the record should have quality flags, and currently do not. This script's goal is to
help me identify and flag those data.

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
PHASE 1: FLAG BASED ON JOB NOTES

PHASE 2: FLAG BASED ON PLOTTING AND STATISTICS, FIND OUTLIERS!

"""
#
# # IMPORT THE DATA FILE
# df = pd.read_csv(r'H:\Science\Datasets\Alberts_dataquality\simplified RLIMS dataset.csv')
#
# """
# The following blocks of code add a "filtering flag" to the data based on what's written in the job notes.
# Later, I'll look at what's left (i.e., what hasn't been flagged as a "common" or unworrying job note, and go through
# those more closely
# """
#
# # INITIAlZE A COLUMN FOR ME TO ADD THINGS TO FILTER ON LATER
# df['CBL_Filtering_Category'] = -999
#
# # MY FILTRATION KEY
# # 1 == HAD NO DATA IN JOB NOTES
# # 2 == ONLY ONE CHARACTER
# # 3 == CONTAINS THE WORD TEST
# # 4 == ONLY CONTAINS NUMBERS
# # 5 == DESCRIBES X/Y (1 of 2, 3 of 6, etc)
# # 6 == DESCRIBES ANYTHING COMTAINING ONLY EA "XYZ"
# # 7 == DESCRIBES A "COMMON DEPEAT" (i.e., "skip acid etch", or "notify client")
#
# # HOW MANY ROWS HAVE NO JOB NOTES? ADD A LABEL. SECOND CLAUSE MAKES SURE I"M NOT OVERWRITING ALREADY FLAGGED DATA
# df.loc[(df['jobNOTES'] == 'Missing[]') & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 1
#
# # HOW MANY ROWS HVAE JOB NOTES WITH ONLY ONE CHARACTER?
# df.loc[(df['jobNOTES'].str.len() == 1) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 2
#
# # HOW MANY ROWS CONTAIN TEST?
# tests = ['TEST','test','Test']
# for i in range(len(tests)):
#     df.loc[(df['jobNOTES'].str.contains(tests[i], na=False)) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 3
#
# # HOW MANY ROWS HAVE FLAGS ALREADY? ALL FLAGS HAVE ALREADY BEEN REMOVED, OR NOT DOWNLOADED
# # print(np.unique(df['flag']))
#
# # HOW MANY ROWS ONLY CONTAIN NUMBERS?
# df.loc[(df['jobNOTES'].str.isdigit()) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 4
#
# # HOW MANY OF THE JOB NOTES ARE SUCH AS :1 OF2, 3 of 6
# for i in range(0, 10):
#     for k in range(0, 10):
#         df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'{i} of {k}'), 'CBL_Filtering_Category'] = 5
#         df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'Split {i} of {k}'), 'CBL_Filtering_Category'] = 5
#         df.loc[(df['CBL_Filtering_Category'] == -999) & (df['jobNOTES'] == f'split {i} of {k}'), 'CBL_Filtering_Category'] = 5
#
# # HOW MANY NOTES ARE ONLY EA NUMBERS? # TODO THIS LINE TAKES THE LONGEST! (UNCOMMENT WHEN CODE IS READY
# for x in range(0,10):
#     for y in range(0, 10):
#         for z in range(0, 10):
#             df.loc[(df['jobNOTES'].str.contains(f'EA {x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'EA # {x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'EA{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'EA #{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
#             df.loc[(df['jobNOTES'].str.contains(f'for EA{x}{y}{z}')) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 6
# #
# # MANY OF THE JOB NOTES ARE SOMETHING I CAN CALL "COMMON REPEATS", and are things I don't think we need to worry too much about
# common_repeats = pd.read_excel(r'H:\Science\Datasets\Alberts_dataquality\common_repeats.xlsx').astype(str)
# repeats = common_repeats['REPEAT']
# for i in range(0, len(repeats)):
#     x = str(repeats[i])
#     df.loc[(df['jobNOTES'] == x) & (df['CBL_Filtering_Category'] == -999), 'CBL_Filtering_Category'] = 7
#
#
# """
# WRITE THE OUTPUT
# """
# # ALIGN NUMBERED FLAGS WITH WHAT THEY MEAN
# numbers = [1,2,3,4,5,6,7]
# meaning = ['Empty Job Notes','1-Char','Contains TEST','Only Digits','X of Y','EA XYZ','Common Repeats']
# # 1 == HAD NO DATA IN JOB NOTES
# # 2 == ONLY ONE CHARACTER
# # 3 == CONTAINS THE WORD TEST
# # 4 == ONLY CONTAINS NUMBERS
# # 5 == DESCRIBES X/Y (1 of 2, 3 of 6, etc)
# # 6 == DESCRIBES ANYTHING COMTAINING ONLY EA "XYZ"
# # 7 == DESCRIBES A "COMMON DEPEAT" (i.e., "skip acid etch", or "notify client")
#
today = date.today()
# # writer = pd.ExcelWriter(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/testout.xlsx', engine='xlsxwriter')
#
# # PRINT OUT THE SORTED CATEGORIES THAT I"VE ASSIGNED
# df.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/ALL_DATA_{today}.csv')
#
# for i in range(0, len(numbers)):
#     toprint = df.loc[df['CBL_Filtering_Category'] == numbers[i]]
#     toprint.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/OutputCat_{meaning[i]}_{today}.csv')
#
# # WHAT DATA HASN"T BEEN CATEGORIZED YET AND NEEDS TO BE?
# to_export = df.loc[df['CBL_Filtering_Category'] == -999]
# to_export.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/Needs_Checking_{today}.csv')
#
# """
# PROGRESS REPORTS AND CHECKS
# """
# # WRITE A ONE LINE PROGRESS REPORT
# print(f'Categorization has downsized original list by {int(100*(1 - (len(to_export)/len(df))))}%, and currently length of data remaining is {len(to_export)}')
#
# # CHECK THAT MY FLAGS ARE BEING WRITTEN
# print(np.unique(df['CBL_Filtering_Category']))
#
# # HOW LONG IS A GIVEN SUBSET?
# check = df.loc[df['CBL_Filtering_Category'] == 7]
# print(f'Length of check data is {len(check)}')


"""
Once I've pre-filtered the jobNOTES according to 1) those that contain innocuous notes (we keep those measurements 1-2; 4-7) and have 
identified everything that is a "test" but not flagged, I'm going to go through the remaining 25% of the data and continue marking what is "innocuous". I think it will
be slightly more elegant from here to just record the TP#'s and add the 'Category' value to it later. 

September 9 2023
I've manually gone through and looked over what hasn't yet fallen into the categories described above. 
Wherenever something seemed worth further look, I put "Discuss" or "13C_soft_flag" (if for 13C reason) or "Remove" it seems like deserved removal, 
although this also probably should be "discussed".

These 'CBL_Filtering_Category'ies will be merged onto the df (the one written to "ALL DATA") and we'll take it from there. This needs to be done with 
a for loop at the moment, I think because the TP's all previously had a -999, so when you merge them, you get extra columns or removed columns
I'm reimporting the written files so I run easier from the python console. 
"""
# import pandas as pd
# import numpy as np
# import warnings
# import xlsxwriter
# from datetime import date
# warnings.simplefilter(action='ignore')
#
# # READ IN MANUAL CHECKS/ REREAD IN DF AND SETUP FOR A MERGE WITH THOSE MANUAL CHECLS
# df = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/ALL_DATA_2023-09-09.csv')
# manual_checks = pd.read_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/manual_checks.csv')
#
# # drop everything that was -999 cuz those would have had manual checks
# df_dropped = df.loc[df['CBL_Filtering_Category'] != -999]
# df_combined = pd.concat([df_dropped, manual_checks]).reset_index(drop=True)
#
# #LENGTH OF ORIGINAL DF SHOULD BE LENGHT OF DF COMBINED
# # print(len(df))
# # print(len(df_combined))
#
# df_combined['CBL_Filtering_Category'] = df_combined['CBL_Filtering_Category'].astype(str)
# print(df_combined['CBL_Filtering_Category'])
# print(np.unique(df_combined['CBL_Filtering_Category']))
#
# df_combined.to_csv(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/PHASE_1_COMPLETE_{today}.csv')














