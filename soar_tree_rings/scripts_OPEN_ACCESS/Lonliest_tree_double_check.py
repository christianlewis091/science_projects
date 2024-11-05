"""
January 10, 2024
Jocelyn wants to run more samples from Lonliest Tree, but wants to be double sure that both cores agree, seeing as
Tree 3 Core 3 doesn't go back past the bomb spike. So we're going to make sure that although roughly visually they agree,
that the measurements are actually the same within error.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned.xlsx')
df = df.loc[df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island"]
df = df[df.duplicated('DecimalDate', keep=False)]


newdesc = []
for i in range(0, len(df)):
    row = df.iloc[i]
    ringcode = row['Ring code']
    ringcode = ringcode[4:9]
    newdesc.append(ringcode)
df['TreeandCore'] = newdesc

years=np.unique(df['DecimalDate'])

for i in range(0, len(years)):
    this_year = df.loc[df['DecimalDate'] == years[i]]

    t2c2 = this_year.loc[this_year['TreeandCore'] =='T2-C2']
    t3c3 = this_year.loc[this_year['TreeandCore'] =='T3-C3']
    t3c2 = this_year.loc[this_year['TreeandCore'] =='T3-C2']

    fig = plt.figure()
    plt.errorbar(t2c2['DecimalDate'], t2c2['∆14C'], yerr=t2c2['∆14Cerr'], label='T2-C2', fmt='o', linestyle='', elinewidth=1, capsize=2)
    plt.errorbar(t3c2['DecimalDate'], t3c2['∆14C'], yerr=t3c2['∆14Cerr'], label='T3-C2', fmt='X', linestyle='', elinewidth=1, capsize=2)
    plt.errorbar(t3c3['DecimalDate'], t3c3['∆14C'], yerr=t3c3['∆14Cerr'], label='T3-C3', fmt='D', linestyle='', elinewidth=1, capsize=2)
    plt.legend()
    plt.xlabel('Date', fontsize=14)
    plt.title(f'{int(years[i])}')
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/lonliest_tree_double_check/{int(years[i])}.png',
                dpi=300, bbox_inches="tight")
    plt.close()












#
# print(np.unique(df['TreeandCore']))
#

# print(df)
# # quickly find wherever there are two measurements for the same year
# duplicates = df[df.duplicated('DecimalDate', keep=False)]
# print(duplicates)

