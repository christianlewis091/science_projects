"""
December 4, 2024: Final check that the script still runs successfully before I submit the paper etc.
Still runs :)

October 6, 2022

This code looks at each of the SOAR Tree Ring sites from Chile and New Zealand that was analyzed here at the Rafter lab,
and tries to find where the bad ring counts are. At the end, two files are created, one that includes the flags,
and labels why they are flagged. The second removes all the flagged data, leaving only the "cleaned" data.

"""
import matplotlib as mpl
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import seaborn as sns
from reference1 import reference1
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

plt.close()
colors = sns.color_palette("rocket", 6)  # import sns color pallet rocket
colors2 = sns.color_palette("mako", 6)  # import sns color pallet mako.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10

df = pd.read_excel(r'H:\Science\Datasets\SOARTreeRingData2022-02-01_August_1_2024.xlsx', comment='#')  # read in the Tree Ring data. Pene's data from tree_rings_second_check was manually added to this file before read-in.
"""
August 5, 2024
One of the comments I am currently dealing with in the fine tuning stage is that the site names need to be changed. for instance, 17 Nikau St Eastbourne is someone's address, 
not appropriate for the paper.
"""

df = df.replace({'19 Nikau St, Eastbourne, NZ': "Eastbourne 1, NZ",
                 '23 Nikau St, Eastbourne, NZ': "Eastbourne 2, NZ",
                 'Bahia San Pedro, Chile': 'Bahia San Pedro, CH',
                 'Baja Rosales, Isla Navarino':'Baja Rosales, Isla Navarino, CH',
                 'Baring Head, NZ':'Baring Head, NZ',
                 'Haast Beach, paddock near beach':'Haast Beach, NZ',
                 "Mason's Bay Homestead":"Mason's Bay, NZ",
                 'Monte Tarn, Punta Arenas':'Monte Tarn, Punta Arenas, CH',
                 'Muriwai Beach Surf Club':'Muriwai Beach, NZ',
                 'Oreti Beach': 'Oreti Beach, NZ',
                 'Puerto Navarino, Isla Navarino':'Puerto Navarino, Isla Navarino, CH',
                 'Raul Marin Balmaceda': 'Raul Marin Balmaceda, CH',
                 'Seno Skyring': 'Seno Skyring, CH',
                 'Tortel island': 'Tortel Island, CH',
                 'Tortel river': 'Tortel River, CH',
                 "World's Loneliest Tree, Camp Cove, Campbell island": "Campbell Island, NZ",
                 'near Kapuni school field, NZ': 'Taranaki, NZ'})

# On January 2, 2025, I noticed that the line below was commented out. I don't know why this was the case, and
# Obviously it was an error. Currnetly the duplicates are removed near line 141.
# df = df.drop_duplicates(subset='Ring code')
df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.

# importing Reference 1 from the previous python file.
harm_xs = reference1['Decimal_date']  # see dataset_harmonization.py
harm_ys = reference1['D14C']  # see dataset_harmonization.py
harm_y_errs = reference1['weightedstderr_D14C']

"""
Before I do anything else, as advised, let's check to see which if any tree ring subsets
have bad counts. First, I'll just do this visually by overlaying the plots onto the
harmonized background record, and see if they do or do not overlap with the bomb spike.
In order to do this, I'll first index the dataset according to each site for easy sub-plotting.

Jan 11, 2024. Redoing this section via loops. I've leveled up in codeing and realized the preivous way can lead to errors
"""

# add a new descriptor which is the ring code (T2-C3, etc)
newdesc = []
for i in range(0, len(df)):
    row = df.iloc[i]

    if row['Site'] == "19 Nikau St, Eastbourne, NZ":
        ringcode = row['Ring code']
        ringcode = ringcode[6:11]
    elif row['Site'] == "23 Nikau St, Eastbourne, NZ":
        ringcode = row['Ring code']
        ringcode = ringcode[6:11]
    elif row['Site'] == "near Kapuni school field, NZ":
        ringcode = row['Ring code']
        ringcode = ringcode[8:13]
    else:
        ringcode = row['Ring code']
        ringcode = ringcode[4:9]

    newdesc.append(ringcode)

df['TreeandCore'] = newdesc

sites = np.unique(df['Site'])

for i in range(0, len(sites)):

    # loop into the first site
    this_site = df.loc[df['Site'] == sites[i]]

    # how many unique tree cores are in this site?
    cores = np.unique(this_site['TreeandCore'])
    fig = plt.figure()
    for j in range(0, len(cores)):
        this_core = this_site.loc[this_site['TreeandCore'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.scatter(this_core['DecimalDate'], this_core['∆14C'], label=f'{cores[j]}')
    plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
    plt.legend()
    plt.xlabel('Date', fontsize=14)
    plt.title(f'{sites[i]}')
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/Fixing_in_Jan2024/unfiltered_plots/{sites[i]}.png', dpi=300, bbox_inches="tight")
    # changing output location for final checks
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/tree_ring_analysis/unfiltered_plots/{sites[i]}.png', dpi=300, bbox_inches="tight")
    plt.close()

# add flags to those samples that look bad.

df['CBL_flag'] = '...'
df.loc[(df['C14Flag'] != '...'), 'CBL_flag'] = 'Already flagged by JCT in original database.'
df.loc[(df['Site'] == "Bahia San Pedro, CH") & (df['DecimalDate'] <= 2005), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 1 and Tree 2 deviate before 2005. Therefore I am removing all data < 2005'
df.loc[(df['Site'] == "Mason's Bay, NZ"), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only one record exists, and is post-bomb spike - therefore cannot be validated.'
df.loc[(df['Site'] == "Monte Tarn, Punta Arenas, CH") & (df['TreeandCore'] == 'T5-C1'), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 5 Core 1 does not match bomb spike.'
df.loc[(df['Site'] == "Muriwai Beach, NZ"), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only one record exists, and is post-bomb spike - therefore cannot be validated.'
# df.loc[(df['Site'] == "Raul Marin Balmaceda") & (df['TreeandCore'] != 'T7-C1'), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only Tree 7 Core 1 matches bomb spike, all others from this site are wrong.'
# the line below was added to simply remove all data from Raul Marin since we found in 2024 from Pene's work that there was a ring count error in the ones we thought were OK.
df.loc[(df['Site'] == "Raul Marin Balmaceda, CH"), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only Tree 7 Core 1 matches bomb spike, all others from this site are wrong.'
df.loc[(df['Site'] == "Oreti Beach, NZ") & (df['C14Flag'] == '.X.'), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: This was flagged by JCT as potentially bad count.'
df.loc[(df['Site'] == "Taranaki, NZ"), 'CBL_flag'] = 'Not included further. Not close enough to coastline and weird winds around taranaki,Tree 1 Core 4 does not match bomb spike.'

# changing output location for final checks
# df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_flags_aug_1_2024.xlsx')
df.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/SOARTreeRingData_CBL_flags_aug_1_2024.xlsx')

df_cleaned = df.loc[(df['CBL_flag']) == '...']
# changing output location for final checks
# df_cleaned.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
print(f'I discovered an issue during reviews (2/2/25), that duplicates and triplicates exist in the tree ring records due to a bug in RLIMS. How long was it before? {len(df_cleaned)}')
df_cleaned = df_cleaned.drop_duplicates(subset='Ring code')
df_cleaned.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
print(f'I discovered an issue during reviews(2/2/25), that duplicates and triplicates exist in the tree ring records due to a bug in RLIMS. How long is it after? {len(df_cleaned)}')

# re-write the plots with only the cleaned data
sites = np.unique(df_cleaned['Site'])

for i in range(0, len(sites)):

    # loop into the first site
    this_site = df_cleaned.loc[df_cleaned['Site'] == sites[i]]

    # how many unique tree cores are in this site?
    cores = np.unique(this_site['TreeandCore'])
    fig = plt.figure()
    for j in range(0, len(cores)):
        this_core = this_site.loc[this_site['TreeandCore'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.scatter(this_core['DecimalDate'], this_core['∆14C'], label=f'{cores[j]}')
    plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
    plt.legend()
    plt.xlabel('Date', fontsize=14)
    plt.title(f'{sites[i]}')
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/Fixing_in_Jan2024/cleaned_plots/{sites[i]}.png',
        dpi=300, bbox_inches="tight")
    # changing output location for final checks
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/tree_ring_analysis/cleaned_plots/{sites[i]}.png', dpi=300, bbox_inches="tight")
    plt.close()

"""
August 5, 2024 JCT wants a side by side plot of Bahia San Pedro "Rachel had a nice figure that showed the difference between the two cores.  You could add that as a second panel below the figure you currently have.
Say something about not being able to determine where the ring count error occurred, so both cores are discarded for >2005 ages.
"
"""

bsp = df.loc[(df['Site']) == 'Bahia San Pedro, CH']
bsp.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/bsp.xlsx')

# I've elected to export this and manually do the differences quick in excel to save time. I've learned to balance excel and python more these days.
# Dec 4, I did not re-do this manual analysis, and leave the read_in location. The rest of this is left as it was.
bsp_in = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/bsp_in.xlsx', sheet_name='Sheet2')
bsp_in = bsp_in.loc[bsp_in['difference'] != -999]
"""
2 plots horizontal
"""
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(1, 2)
gs.update(wspace=0.2, hspace=0.35)

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])

# how many unique tree cores are in this site?
cores = np.unique(bsp['TreeandCore'])
for j in range(0, len(cores)):
    this_core = bsp.loc[bsp['TreeandCore'] == cores[j]]
    # used to do errorbar but they're too small to se anyway compared to the data
    plt.scatter(this_core['DecimalDate'], this_core['∆14C'], label=f'{cores[j]}')
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.xlim(1980,2020)
plt.ylim(0,300)
plt.xlabel('Date', fontsize=14)
plt.title('Bahia San Pedro, Chile')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plt.title('Difference between cores: (T1-C2)-(T2-C1)')
plt.errorbar(bsp_in['Year'], bsp_in['difference'], yerr=bsp_in['properr'], linestyle='', marker='o', color='black')
plt.ylabel('Difference between cores: (T1-C2)-(T2-C1) (\u2030)', fontsize=14)  # label the y axis
plt.xlim(1980,2020)
plt.axhline(y=0, color='black')
plt.savefig(
    f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/Fixing_in_Jan2024/cleaned_plots/Bahia_sidebar.png',
    dpi=300, bbox_inches="tight")
plt.savefig(
    f'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Images_and_Figures/tree_ring_analysis\cleaned_plots/Bahia_sidebar.png',
    dpi=300, bbox_inches="tight")
plt.close()


