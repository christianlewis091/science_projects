"""
The excel sheet read in below was created by findnig the NZA's in Rachel's Thesis Table 4.2
Initial .loc functions are added to recreate the metadata from this table. 
"""

import pandas as pd
import warnings 
warnings.filterwarnings(
    "ignore",
    message="Workbook contains no default style, apply openpyxl's default")

df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\Corran_Table4_2.xlsx")


"""
BOMB PERIOD LABELLING 
"""
group1 = [56840,56843,56179,56842,56181,56178,56841,56180]
group2 = [57793,57795,57794,57792,57791]
group3 = [62645,62647,62646,62648]
group4 = [57788,57790,57789,57787,57786]
group5 = [62643,62644]
group6 = [62329,62330]
group7 = [62327, 62328]

# set empty columns
df['Type'] = 'So Far Empty'
df['Year'] = -999

# fill in the columnmjs we set
df.loc[df['Job::NZA'].isin(group1), 'Type'] = 'Bomb Period Oak Tree Ring'
df.loc[df['Job::NZA'].isin(group1), 'Year'] = 1950

df.loc[df['Job::NZA'].isin(group2), 'Type'] = 'Bomb Period Oak Tree Ring'
df.loc[df['Job::NZA'].isin(group2), 'Year'] = 1956

df.loc[df['Job::NZA'].isin(group3), 'Type'] = 'Bomb Period Kauri Tree Ring'
df.loc[df['Job::NZA'].isin(group3), 'Year'] = 1957

df.loc[df['Job::NZA'].isin(group4), 'Type'] = 'Bomb Period Oak Tree Ring'
df.loc[df['Job::NZA'].isin(group4), 'Year'] = 1958

df.loc[df['Job::NZA'].isin(group5), 'Type'] = 'Bomb Period Kauri Tree Ring'
df.loc[df['Job::NZA'].isin(group5), 'Year'] = 1961

df.loc[df['Job::NZA'].isin(group6), 'Type'] = 'Bomb Period Kauri Tree Ring'
df.loc[df['Job::NZA'].isin(group6), 'Year'] = 1966

df.loc[df['Job::NZA'].isin(group7), 'Type'] = 'Bomb Period Kauri Tree Ring'
df.loc[df['Job::NZA'].isin(group7), 'Year'] = 1968

"""
POSTBOMB PERIOD LABELLING 
"""
group8=[56187,56189, 56186,56188]
group9=[62641,62642]
group10=[56191,56193,56190,56192]
group11=[62325,62326]
group11_1 =[62323,62324]
group12=[62639,62640]
group13=[56183,56185,56182,56184]
group14=[62638,62637]

df.loc[df['Job::NZA'].isin(group8), 'Type'] = 'Post Bomb Pine Tree Ring'
df.loc[df['Job::NZA'].isin(group8), 'Year'] = 1986

df.loc[df['Job::NZA'].isin(group9), 'Type'] = 'Post Bomb Pine Tree Ring'
df.loc[df['Job::NZA'].isin(group9), 'Year'] = 1988

df.loc[df['Job::NZA'].isin(group10), 'Type'] = 'Post Bomb Chestnut Tree Ring'
df.loc[df['Job::NZA'].isin(group10), 'Year'] = 1990

df.loc[df['Job::NZA'].isin(group11), 'Type'] = 'Post Bomb Chestnut Tree Ring'
df.loc[df['Job::NZA'].isin(group11), 'Year'] = 1991

df.loc[df['Job::NZA'].isin(group11_1), 'Type'] = 'Post Bomb Chestnut Tree Ring'
df.loc[df['Job::NZA'].isin(group11_1), 'Year'] = 1994

df.loc[df['Job::NZA'].isin(group12), 'Type'] = 'Post Bomb Chestnut Tree Ring'
df.loc[df['Job::NZA'].isin(group12), 'Year'] = 1995

df.loc[df['Job::NZA'].isin(group13), 'Type'] = 'Post Bomb Pine Tree Ring'
df.loc[df['Job::NZA'].isin(group13), 'Year'] = 1999

df.loc[df['Job::NZA'].isin(group14), 'Type'] = 'Post Bomb Pine Tree Ring'
df.loc[df['Job::NZA'].isin(group14), 'Year'] = 2000

"""
Ancient Wood Labelling
"""
group15 = [62313,62625,62311,62626]
group16 = [56174,56176,56173,56175]
group17 = [56167,56169,56166,56168,62322,62635,62321,62636]

df.loc[df['Job::NZA'].isin(group15), 'Type'] = 'Known-age wood (FIRI-D)'
df.loc[df['Job::NZA'].isin(group16), 'Type'] = 'Known-age wood (SIRI-F)'
df.loc[df['Job::NZA'].isin(group17), 'Type'] = 'Blank wood Kauri'

"""
Other Organic Materials
"""
group18 = [12357,12358,64289,64290]
group19 = [12340,12341,64291,64292]
group20 = [12954,12955,12956,12957,64293,64294]

df.loc[df['Job::NZA'].isin(group18), 'Type'] = 'Known-age leather (FIRI-Q)'
df.loc[df['Job::NZA'].isin(group19), 'Type'] = 'Parchment (FIRI optional)'
df.loc[df['Job::NZA'].isin(group20), 'Type'] = 'Textile (FIRI optional)'

"""
Now we'll need to do the tedious job of adding the "methods" from her table.

ww = untreated whole wood

As = ANSTO soxhlet wash only (no cellulose extraction)
Rs = RRL Soxhlet wash only, (no cellulose)

As-A = ANSTO soxhlet, ANSTO cellulose
As-R = ANSTO soxhlet, RRL cellulose
Rs-R = RRL Soxlet, RRL cellulose
Rs-A = RRL soxlet, ANSTO cellulose

# chekcing the Soxlet vs ASE
 Rs-A; RRL Soxhlet solvent wash, ANSTO cellulose extraction
 Ra-A : RRL ASE, ANSTO cellulose
"""

unlabelled = [56842, 56841,62647,62648,62625,62626,62635,62636,12358,64290,12341,64292,12955,12956,12957,64294]
ww = [56840,57793,57788]
Rs = [56843]
As_A = [56179,57792,57787,56187,56191,56183,56174,56167]
As_R = [56181,56189,56193,56185,56176,56169]
Rs_A = [56178, 56180,57791,62645,57786,62643,62329,62327,56188,62641,56192,62325,62323,62639,56184,62638,62313,56175,56168,62322,12357,12340,64291,12954]
As = [57795,57790]
Rs = [57794,57789]
Ra_A = [62646,62644,62330,62328,62642,62326,62324,62640,62637,62311,62321,64289,64293]
Rs_R = [56186,56190,56182,56173,56166]

df['Method_fromTable'] = 'Not Yet Filled' 

df.loc[df['Job::NZA'].isin(unlabelled), 'Method_fromTable'] = 'Unlabelled'
df.loc[df['Job::NZA'].isin(ww), 'Method_fromTable'] = 'Whole wood, untreated'

df.loc[df['Job::NZA'].isin(Rs), 'Method_fromTable'] = 'RRL Soxhlet wash only, (no cellulose)'
df.loc[df['Job::NZA'].isin(As), 'Method_fromTable'] = 'ANSTO soxhlet wash only (no cellulose extraction)'

df.loc[df['Job::NZA'].isin(As_A), 'Method_fromTable'] = 'ANSTO soxhlet, ANSTO cellulose'
df.loc[df['Job::NZA'].isin(As_R), 'Method_fromTable'] = 'ANSTO soxhlet, RRL cellulose'
df.loc[df['Job::NZA'].isin(Rs_A), 'Method_fromTable'] = 'RRL soxlet, ANSTO cellulose'
df.loc[df['Job::NZA'].isin(Rs_R), 'Method_fromTable'] = 'RRL Soxlet, RRL cellulose'

df.loc[df['Job::NZA'].isin(Ra_A), 'Method_fromTable'] = 'RRL Soxhlet solvent wash, ANSTO cellulose extraction'

df.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\data\Corran_Table4_2_OUTPUT_FOR_CHECK.xlsx")




