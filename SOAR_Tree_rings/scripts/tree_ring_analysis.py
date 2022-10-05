

"""
Purpose:
Use the harmonized Southern Hemisphere dataset to see if we can find shifts in SOAR tree rings
to understand Southern ocean upwelling.
Outcome:
Currently in DEV mode.
"""
# TODO Index based on the flags in the dataset!
# Import all the basic libraries that I'll be using
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import seaborn as sns
from B_CGO_BHD_harmonization import harmonized
from X_miller_curve_algorithm import ccgFilter
from X_my_functions import monte_carlo_randomization_trend
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

"""
These next few lines appear often at the top of my codes. 
These next lines set some initial parameters that figures in the code will follow
and imports some nice colors that we'll use. 
"""
plt.close()
colors = sns.color_palette("rocket", 6)  # import sns color pallet rocket
colors2 = sns.color_palette("mako", 6)  # import sns color pallet mako.
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10

df = pd.read_excel(r'H:\Science\Datasets'
                   r'\SOARTreeRingData2022-02-01.xlsx')  # read in the Tree Ring data.
df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.
df = df.loc[(df['C14Flag']) != 'A..']

# importing harmonized southern hemisphere dataset from the previous python file.
harm_xs = harmonized['Decimal_date']  # see dataset_harmonization.py
harm_ys = harmonized['D14C']  # see dataset_harmonization.py
harm_y_errs = harmonized['weightedstderr_D14C']

"""
Before I do anything else, as advised, let's check to see which if any tree ring subsets
have bad counts. First, I'll just do this visually by overlaying the plots onto the
harmonized background record, and see if they do or do not overlap with the bomb spike.
In order to do this, I'll first index the dataset according to each site for easy sub-plotting.
"""

# # names = np.unique(df['StudySites::Site name'])
# # print(names)
CH_41_S = df.loc[(df['Site'] == 'Bahia San Pedro, Chile')]
CH_41_S_x = CH_41_S['DecimalDate']
CH_41_S_y = CH_41_S['∆14C']

CH_44_S = df.loc[(df['Site'] == 'Raul Marin Balmaceda')]
CH_44_S_x = CH_44_S['DecimalDate']
CH_44_S_y = CH_44_S['∆14C']

CH_48_S = df.loc[(df['Site'] == 'Tortel island')]
CH_48_S_x = CH_48_S['DecimalDate']
CH_48_S_y = CH_48_S['∆14C']

CH_48_S_2 = df.loc[(df['Site'] == 'Tortel river')]
CH_48_S_2_x = CH_48_S_2['DecimalDate']
CH_48_S_2_y = CH_48_S_2['∆14C']

CH_53_S = df.loc[(df['Site'] == 'Seno Skyring')]
CH_53_S_x = CH_53_S['DecimalDate']
CH_53_S_y = CH_53_S['∆14C']

CH_54_S = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
CH_54_S_x = CH_54_S['DecimalDate']
CH_54_S_y = CH_54_S['∆14C']

CH_55_S = df.loc[(df['Site'] == 'Baja Rosales, Isla Navarino')]
CH_55_S_x = CH_55_S['DecimalDate']
CH_55_S_y = CH_55_S['∆14C']

CH_55_S_2 = df.loc[(df['Site'] == 'Puerto Navarino, Isla Navarino')]
CH_55_S_2_x = CH_55_S_2['DecimalDate']
CH_55_S_2_y = CH_55_S_2['∆14C']

NZ_37_S = df.loc[(df['Site'] == 'Muriwai Beach Surf Club')]
NZ_37_S_x = NZ_37_S['DecimalDate']
NZ_37_S_y = NZ_37_S['∆14C']

NZ_39_S = df.loc[(df['Site'] == 'near Kapuni school field, NZ')]
NZ_39_S_x = NZ_39_S['DecimalDate']
NZ_39_S_y = NZ_39_S['∆14C']

NZ_41_S = df.loc[(df['Site'] == '19 Nikau St, Eastbourne, NZ')]
NZ_41_S_x = NZ_41_S['DecimalDate']
NZ_41_S_y = NZ_41_S['∆14C']

NZ_41_S_2 = df.loc[(df['Site'] == 'Baring Head, NZ')]
NZ_41_S_2_x = NZ_41_S_2['DecimalDate']
NZ_41_S_2_y = NZ_41_S_2['∆14C']

NZ_41_S_3 = df.loc[(df['Site'] == '23 Nikau St, Eastbourne, NZ')]
NZ_41_S_3_x = NZ_41_S_3['DecimalDate']
NZ_41_S_3_y = NZ_41_S_3['∆14C']

NZ_44_S = df.loc[(df['Site'] == 'Haast Beach, paddock near beach')]
NZ_44_S_x = NZ_44_S['DecimalDate']
NZ_44_S_y = NZ_44_S['∆14C']
# NZ_41_S_3.to_excel('eb.xlsx')

NZ_46_S = df.loc[(df['Site'] == 'Oreti Beach')]
NZ_46_S_x = NZ_46_S['DecimalDate']
NZ_46_S_y = NZ_46_S['∆14C']

NZ_47_S = df.loc[(df['Site'] == "Mason's Bay Homestead")]
NZ_47_S_x = NZ_47_S['DecimalDate']
NZ_47_S_y = NZ_47_S['∆14C']

NZ_53_S = df.loc[(df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island")]
NZ_53_S_x = NZ_53_S['DecimalDate']
NZ_53_S_y = NZ_53_S['∆14C']

fig, axs = plt.subplots(2, 4, sharex=True, sharey=True, figsize=(20, 8))

axs[0, 0].scatter(CH_41_S_x, CH_41_S_y, label='CH_41_S')
axs[0, 0].set_title("41\xb0S (Bahia, San Pedro)")
axs[0, 0].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 1].scatter(CH_44_S_x, CH_44_S_y, label='CH_41_S')
axs[0, 1].set_title("44\xb0S (Raul Marin Balcemeda)")
axs[0, 1].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 2].scatter(CH_48_S_x, CH_48_S_y, label='CH_41_S')
axs[0, 2].set_title("48\xb0S (Tortel Island)")
axs[0, 2].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 3].scatter(CH_48_S_2_x, CH_48_S_2_y, label='CH_41_S')
axs[0, 3].set_title("48\xb0S (Tortel River)")
axs[0, 3].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 0].scatter(CH_53_S_x, CH_53_S_y, label='CH_41_S')
axs[1, 0].set_title("53\xb0S (Seno Skyring)")
axs[1, 0].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 3].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)
axs[1, 3].scatter(CH_54_S_x, CH_54_S_y, label='CH_41_S')
axs[1, 3].set_title("54\xb0S (Monte Tarn, Punta Arenas)")

axs[1, 1].scatter(CH_55_S_x, CH_55_S_y, label='CH_41_S')
axs[1, 1].set_title("55\xb0S (Baja Rosales, Isla Navarino)")
axs[1, 1].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 2].scatter(CH_55_S_2_x, CH_55_S_2_y, label='CH_41_S')
axs[1, 2].set_title("55\xb0S (Puerto Navarino, Isla Navarino)")
axs[1, 2].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Tree_ring_validation1.png',
    dpi=300, bbox_inches="tight")
plt.close()

fig, axs = plt.subplots(2, 5, sharex=True, sharey=True, figsize=(20, 8))
axs[0, 0].scatter(NZ_37_S_x, NZ_37_S_y, label='CH_41_S')
axs[0, 0].set_title("37\xb0S (Muriwai Beach)")
axs[0, 0].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 1].scatter(NZ_39_S_x, NZ_39_S_y, label='CH_41_S')
axs[0, 1].set_title("39\xb0S (Kapuni Beach)")
axs[0, 1].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 3].scatter(NZ_41_S_x, NZ_41_S_y, label='CH_41_S')
axs[0, 3].set_title("41\xb0S (Eastbourne)")
axs[0, 3].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 2].scatter(NZ_41_S_2_x, NZ_41_S_2_y, label='CH_41_S')
axs[0, 2].set_title("41\xb0S (Baring Head)")
axs[0, 2].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 4].scatter(NZ_41_S_3_x, NZ_41_S_3_y, label='CH_41_S')
axs[0, 4].set_title("41\xb0S (Eastbourne)")
axs[0, 4].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 1].scatter(NZ_44_S_x, NZ_44_S_y, label='CH_41_S')
axs[1, 1].set_title("44\xb0S (Haast Beach)")
axs[1, 1].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 2].scatter(NZ_46_S_x, NZ_46_S_y, label='CH_41_S')
axs[1, 2].set_title("46\xb0S (Oreti Beach)")
axs[1, 2].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 3].scatter(NZ_47_S_x, NZ_47_S_y, label='CH_41_S')
axs[1, 3].set_title("47\xb0S (Mason's Bay)")
axs[1, 3].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 4].scatter(NZ_53_S_x, NZ_53_S_y, label='CH_41_S')
axs[1, 4].set_title("53\xb0S (World's Lonliest Tree)")
axs[1, 4].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Tree_ring_validation2.png',
    dpi=300, bbox_inches="tight")
plt.close()

fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(20, 8))

axs[0, 0].scatter(NZ_39_S_x, NZ_39_S_y, label='CH_41_S')
axs[0, 0].set_title("39\xb0S (Kapuni Beach)")
axs[0, 0].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[0, 1].scatter(NZ_41_S_3_x, NZ_41_S_3_y, label='CH_41_S')
axs[0, 1].set_title("41\xb0S (Eastbourne)")
axs[0, 1].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 0].scatter(CH_44_S_x, CH_44_S_y, label='CH_41_S')
axs[1, 0].set_title("44\xb0S (Raul Marin Balcemeda)")
axs[1, 0].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)

axs[1, 1].plot(harm_xs, harm_ys, label='CH_41_S', color='black', alpha=0.5)
axs[1, 1].scatter(CH_54_S_x, CH_54_S_y, label='CH_41_S')
axs[1, 1].set_title("54\xb0S (Monte Tarn, Punta Arenas)")

plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Tree_ring_validation_badrings.png',
    dpi=300, bbox_inches="tight")
plt.close()

"""
May 30, 2022: 
After meeting with Jocelyn, she noted that some of the bad ring counts may be from bad cores, while there are many
cores from the same site. 
Let's go through each of the cores and just verify that each one is good.
The following checks will go in order of the already indexed data by site.  
We shall follow the following checklist: 
1. If there is an obvious bad ring count (such as in Kapuni, Balcemeda, or Monte Tarn), check if there are multiple 
cores and if so, remove the bad ones. Check if there is a flag. If there is no flag, add a flag. 
2. If the core is too young to have the bomb-spike, there should be multiple cores. These double-cores are another
way of verifying the ring-counts (less likely that you have two side by side bad ring counts). 
So. 
I wrote a function(s) that is meant to aid with this specific process, because it became quite hard to index with 
the Ring Codes 'T1-C3-XXYY'. 
The following function "tree_ring_count_verification" indexes using data and and element that the user knows to 
tell the computer to look for. This data can then be put into the plotting function. I don't think its usually such a 
good idea to have a generic function for plotting but in this case, I think it will save me heaps of time. 
I'll define the arguments for each function below: 
data: a pandas dataframe of data 
element: a string ('xxxxx') element that you want the computer to look for. 'T1' for tree 1, or C3 for core 3. 
I'm going to just quickly list the types of elements that I'll need for each site here to save myself time for later. 
This can be found in my Data Science notebook. May 30, 2022, second page from this day. 
"""


def tree_ring_count_verification(data, element):
    data = data.reset_index(drop=True)  # reset the index or you get type-setting errors
    empty_array = []  # create an empty array. We will dump our sorted data in here
    for i in range(0, len(data)):  # initialize a for-loop the length of the site's dataset
        row = data.iloc[i]  # grab the i'th row
        cell = row['Ring code']  # grab the column of data from that row
        if element in cell:  # if what we're looking for is in there, append it to the array
            empty_array.append(row)
    data_new = pd.DataFrame(empty_array)  # take the array and put into a Pandas Dataframe.
    return data_new


CH_41_S_core1 = tree_ring_count_verification(CH_41_S, 'T1')
CH_41_S_core2 = tree_ring_count_verification(CH_41_S, 'T2')

CH_44_S_core1 = tree_ring_count_verification(CH_44_S, 'T7')
CH_44_S_core2 = tree_ring_count_verification(CH_44_S, 'T4')
CH_44_S_core3 = tree_ring_count_verification(CH_44_S, 'T3')

CH_48_S_core1 = tree_ring_count_verification(CH_48_S, 'T4')
CH_48_S_core2 = tree_ring_count_verification(CH_48_S_2,'T6')

CH_53_S_core1 = tree_ring_count_verification(CH_53_S, 'T3')
CH_53_S_core2 = tree_ring_count_verification(CH_53_S, 'T4')

CH_54_S_core1 = tree_ring_count_verification(CH_54_S, 'T6')
CH_54_S_core2 = tree_ring_count_verification(CH_54_S, 'T3')
CH_54_S_core3 = tree_ring_count_verification(CH_54_S, 'T5')

CH_55_S_core1 = tree_ring_count_verification(CH_55_S, 'T4')
CH_55_S_core2 = tree_ring_count_verification(CH_55_S, 'T1')
CH_55_S_core3 = tree_ring_count_verification(CH_55_S_2, 'T1')

NZ_37_S_core1 = tree_ring_count_verification(NZ_37_S, 'T2')  # ONLY ONE CORE HERE

NZ_39_S_core1 = tree_ring_count_verification(NZ_39_S, 'C1')
NZ_39_S_core2 = tree_ring_count_verification(NZ_39_S, 'C4')

NZ_41_S_core1 = tree_ring_count_verification(NZ_41_S, 'C2')
NZ_41_S_core2 = tree_ring_count_verification(NZ_41_S_2, 'C1')
NZ_41_S_core3 = tree_ring_count_verification(NZ_41_S_2, 'C3')
NZ_41_S_core4 = tree_ring_count_verification(NZ_41_S_3, 'C2')

NZ_44_S_core1 = tree_ring_count_verification(NZ_44_S, 'C1')
NZ_44_S_core2 = tree_ring_count_verification(NZ_44_S, 'C2')

NZ_46_S_core1 = tree_ring_count_verification(NZ_46_S, 'C1')
NZ_46_S_core2 = tree_ring_count_verification(NZ_46_S, 'C2')


NZ_47_S_core1 = tree_ring_count_verification(NZ_47_S, 'T1')  # ONLY ONE CORE HERE

NZ_53_S_core1 = tree_ring_count_verification(NZ_53_S, 'C2')
NZ_53_S_core2 = tree_ring_count_verification(NZ_53_S, 'C3')

"""
After splicing up the data based on the multi-tree and core information, the next block of code will be the plots. 
I'll use the plots to help visually decide which data the keep and which to remove. As a reminder: 
1. If data matches the bomb peak, this is one good validation. 
2. If data is too young for the bomb peak, there should be TWO records from the same tree and if they match, 
we call it valid. 
"""

size = 50
plt.errorbar(CH_41_S_core1['DecimalDate'], CH_41_S_core1['∆14C'], label='Tree 1, Core 2', yerr=CH_41_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_41_S_core2['DecimalDate'], CH_41_S_core2['∆14C'], label='Tree 2, Core 1', yerr=CH_41_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('41\u00b0S: Bahia San Pedro, Chile')
plt.xlim(min(CH_41_S['DecimalDate'] - 5), max(CH_41_S['DecimalDate'] + 5))
plt.ylim(min(CH_41_S['∆14C'] - 25), max(CH_41_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/BahiaSanPedro_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(CH_44_S_core1['DecimalDate'], CH_44_S_core1['∆14C'], label='Tree 7, Core 1', yerr=CH_44_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_44_S_core2['DecimalDate'], CH_44_S_core2['∆14C'], label='Tree 4, Core 1', yerr=CH_44_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(CH_44_S_core3['DecimalDate'], CH_44_S_core3['∆14C'], label='Tree 3, Core 2', yerr=CH_44_S_core3['∆14Cerr'], fmt='*', color=colors2[5], ecolor=colors2[5], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('44\u00b0S: Raul Marin Balmaceda, Chile')
plt.xlim(min(CH_44_S['DecimalDate'] - 5), max(CH_44_S['DecimalDate'] + 5))
plt.ylim(min(CH_44_S['∆14C'] - 25), max(CH_44_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/RaulMarin_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(CH_48_S_core1['DecimalDate'], CH_48_S_core1['∆14C'], label='Tree 4, Core 1 (Tortel Island)', yerr=CH_48_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_48_S_core2['DecimalDate'], CH_48_S_core2['∆14C'], label='Tree 6, Core 1 (Tortel River)', yerr=CH_48_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('48\u00b0S: Tortel Island and Tortel River, Chile')
plt.xlim(min(CH_48_S['DecimalDate'] - 5), max(CH_48_S['DecimalDate'] + 5))
plt.ylim(min(CH_48_S['∆14C'] - 25), max(CH_48_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Tortel_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(CH_53_S_core1['DecimalDate'], CH_53_S_core1['∆14C'], label='Tree 3, Core 1', yerr=CH_53_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_53_S_core2['DecimalDate'], CH_53_S_core2['∆14C'], label='Tree 4, Core 2', yerr=CH_53_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('53\u00b0S: Seno Skyring, Chile')
plt.xlim(min(CH_53_S['DecimalDate'] - 5), max(CH_53_S['DecimalDate'] + 5))
plt.ylim(min(CH_53_S['∆14C'] - 25), max(CH_53_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/SenoSky_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(CH_54_S_core1['DecimalDate'], CH_54_S_core1['∆14C'], label='Tree 6, Core 2', yerr=CH_54_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_54_S_core2['DecimalDate'], CH_54_S_core2['∆14C'], label='Tree 3, Core 1', yerr=CH_54_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(CH_54_S_core3['DecimalDate'], CH_54_S_core3['∆14C'], label='Tree 5, Core 1', yerr=CH_54_S_core3['∆14Cerr'], fmt='*', color=colors2[5], ecolor=colors2[5], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('54\u00b0S: Monte Tarn, Chile')
plt.xlim(min(CH_54_S['DecimalDate'] - 5), max(CH_54_S['DecimalDate'] + 5))
plt.ylim(min(CH_54_S['∆14C'] - 25), max(CH_54_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MonteTarn_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()
"""
Another thing to see is how Ricardo's Monte Tarn data matches with ours, so i'm going to briefly look at those as well. 
"""
df2 = pd.read_excel(r'H:\Science\Datasets\Jocelyn Chile tree data 1980-2016.xlsx')
df2_1 = df2.loc[(df2['Sheet']) == 1]
df2_2 = df2.loc[(df2['Sheet']) == 2]
df2_3 = df2.loc[(df2['Sheet']) == 3]
df2_4 = df2.loc[(df2['Sheet']) == 4]

size = 50
plt.errorbar(CH_54_S_core1['DecimalDate'], CH_54_S_core1['∆14C'], label='Tree 6, Core 2', yerr=CH_54_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_54_S_core2['DecimalDate'], CH_54_S_core2['∆14C'], label='Tree 3, Core 1', yerr=CH_54_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(CH_54_S_core3['DecimalDate'], CH_54_S_core3['∆14C'], label='Tree 5, Core 1', yerr=CH_54_S_core3['∆14Cerr'], fmt='*', color=colors2[5], ecolor=colors2[5], elinewidth=1, capsize=2)
plt.errorbar(df2_1['Year of Growth'], df2_1['D14C'], label='De Pol Holz: Polylepis tarapacana', yerr=df2_1['D14Cerr'], fmt='o', color=colors[1], ecolor=colors[1], elinewidth=1, capsize=2)
plt.errorbar(df2_2['Year of Growth'], df2_2['D14C'], label='De Pol Holz: Asutrocedrus chilensis', yerr=df2_2['D14Cerr'], fmt='D', color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2)
plt.errorbar(df2_3['Year of Growth'], df2_3['D14C'], label='De Pol Holz: Fitzroya cupressoides', yerr=df2_3['D14Cerr'], fmt='*', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.errorbar(df2_4['Year of Growth'], df2_4['D14C'], label='De Pol Holz: Pilgerodendron uviferum', yerr=df2_4['D14Cerr'], fmt='^', color=colors[4], ecolor=colors[4], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('54\u00b0S: Monte Tarn, Chile, de Pol Holz Dataset')
plt.xlim(min(df2['Year of Growth'] - 5), max(df2['Year of Growth'] + 5))
plt.ylim(min(df2['D14C'] - 25), max(df2['D14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MonteTarn_dePol Holz.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(CH_55_S_core1['DecimalDate'], CH_55_S_core1['∆14C'], label='Tree 4, Core 1 (Baja Rosales)', yerr=CH_55_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(CH_55_S_core2['DecimalDate'], CH_55_S_core2['∆14C'], label='Tree 1, Core 1 (Baja Rosales)', yerr=CH_55_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(CH_55_S_core3['DecimalDate'], CH_55_S_core3['∆14C'], label='Tree 1, Core 1 (Puerto Navarino)', yerr=CH_55_S_core3['∆14Cerr'], fmt='*', color=colors2[5], ecolor=colors2[5], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('55\u00b0S: Baja Rosales and Puerto Navarino, Chile')
plt.xlim(min(CH_55_S['DecimalDate'] - 5), max(CH_55_S['DecimalDate'] + 5))
plt.ylim(min(CH_55_S['∆14C'] - 25), max(CH_55_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Puerto Navarino_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_37_S_core1['DecimalDate'], NZ_37_S_core1['∆14C'], label='Tree 2, Core 2', yerr=NZ_37_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('37\u00b0S: Muriwai Beach, New Zealand')
plt.xlim(min(NZ_37_S['DecimalDate'] - 5), max(NZ_37_S['DecimalDate'] + 5))
plt.ylim(min(NZ_37_S['∆14C'] - 25), max(NZ_37_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MuriwaiBeach_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_39_S_core1['DecimalDate'], NZ_39_S_core1['∆14C'], label='Tree 1, Core 1', yerr=NZ_39_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(NZ_39_S_core2['DecimalDate'], NZ_39_S_core2['∆14C'], label='Tree 1, Core 4', yerr=NZ_39_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('39\u00b0S: Kapuni Beach, New Zealand')
plt.xlim(min(NZ_39_S['DecimalDate'] - 5), max(NZ_39_S['DecimalDate'] + 5))
plt.ylim(min(NZ_39_S['∆14C'] - 25), max(NZ_39_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Kapuni_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_41_S_core2['DecimalDate'], NZ_41_S_core2['∆14C'], label='Tree 1, Core 1, (Baring Head)', yerr=NZ_41_S_core2['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(NZ_41_S_core3['DecimalDate'], NZ_41_S_core3['∆14C'], label='Tree 1, Core 3 (Baring Head)', yerr=NZ_41_S_core3['∆14Cerr'], fmt='D', color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2)
plt.errorbar(NZ_41_S_core4['DecimalDate'], NZ_41_S_core4['∆14C'], label='Tree 1, Core 2 (Eastbourne 2)', yerr=NZ_41_S_core4['∆14Cerr'], fmt='*', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(NZ_41_S_core1['DecimalDate'], NZ_41_S_core1['∆14C'], label='Tree 1, Core 2, (Eastbourne 1)', yerr=NZ_41_S_core1['∆14Cerr'], fmt='^', color=colors[4], ecolor=colors[4], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('41\u00b0S: Eastbourne and Baring Head, New Zealand')
plt.xlim(min(NZ_41_S['DecimalDate'] - 5), max(NZ_41_S['DecimalDate'] + 5))
plt.ylim(min(NZ_41_S['∆14C'] - 25), max(NZ_41_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Eastborne_BHEAD_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_44_S_core1['DecimalDate'], NZ_44_S_core1['∆14C'], label='Tree 1, Core 1', yerr=NZ_44_S_core1['∆14Cerr'], fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(NZ_44_S_core2['DecimalDate'], NZ_44_S_core2['∆14C'], label='Tree 1, Core 2', yerr=NZ_44_S_core2['∆14Cerr'], fmt='D', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('44\u00b0S: Haast Beach, New Zealand')
plt.xlim(min(NZ_44_S['DecimalDate'] - 5), max(NZ_44_S['DecimalDate'] + 5))
plt.ylim(min(NZ_44_S['∆14C'] - 25), max(NZ_44_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Haast_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_46_S_core1['DecimalDate'], NZ_46_S_core1['∆14C'], label='Tree 2, Core 2', yerr=NZ_46_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(NZ_46_S_core2['DecimalDate'], NZ_46_S_core2['∆14C'], label='Tree 2, Core 1', yerr=NZ_46_S_core2['∆14Cerr'], fmt='D', color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('46\u00b0S: Oreti Beach, New Zealand')
plt.xlim(min(NZ_46_S['DecimalDate'] - 5), max(NZ_46_S['DecimalDate'] + 5))
plt.ylim(min(NZ_46_S['∆14C'] - 25), max(NZ_46_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Oreti_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_47_S_core1['DecimalDate'], NZ_47_S_core1['∆14C'], label='Tree 1, Core 1', yerr=NZ_47_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('47\u00b0S: Masons Bay, New Zealand')
plt.xlim(min(NZ_47_S['DecimalDate'] - 5), max(NZ_47_S['DecimalDate'] + 5))
plt.ylim(min(NZ_47_S['∆14C'] - 25), max(NZ_47_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MasonBay_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()

size = 50
plt.errorbar(NZ_53_S_core1['DecimalDate'], NZ_53_S_core1['∆14C'], label='Tree 2, Core 2', yerr=NZ_53_S_core1['∆14Cerr'], fmt='o', color=colors2[1], ecolor=colors2[1], elinewidth=1, capsize=2)
plt.errorbar(NZ_53_S_core2['DecimalDate'], NZ_53_S_core2['∆14C'], label='Tree 3, Core 3', yerr=NZ_53_S_core2['∆14Cerr'], fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.plot(harm_xs, harm_ys, label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
plt.legend()
plt.title('53\u00b0S: Lonliest Tree, New Zealand')
plt.xlim(min(NZ_53_S['DecimalDate'] - 5), max(NZ_53_S['DecimalDate'] + 5))
plt.ylim(min(NZ_53_S['∆14C'] - 25), max(NZ_53_S['∆14C'] + 25))
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/LonliestTree_validation.png',
    dpi=300, bbox_inches="tight")
plt.close()


"""
So here is the tentative list of the data that we will need to remove. Upon subject to change with my next meeting with
Jocelyn:
Chile:
Bahia San Pedro : All data before 2005.
Monte Tarn:       Remove Tree 5, Core 1.
Balmaceda:        Remove all besides Tree 7, Core 1.
New Zealand:
Kapuni:           Throw out Tree 1, Core 4.
Mason's Bay:      Only one record - cannot validate because too young. Remove.
Muriwai Beach:    Only one record - cannot validate because too young. Remove.
The next step is to remove the data that I have designated above. After I do this, I will re-set the dataframe as the
new one, and proceed as I was doing before with the offset calculations.
Next steps in order.
1. Flag the bad data with a unique flag and send updated excel file to Jocelyn.
2. Remove the bad data and re-concatenate into a DataFrame
3. Calculate the smooth fit using CCGCRV for the updated dataset's x-values and run monte carlo to get error estimates.
4. Calculate offsets and offset errors from the remaining tree ring data and the background dataset
5. Calculate initial rough latitudinal offset gradients
6. Re-assess plan before following long term goals (using Hysplit backtrajectories)
"""

"""
######################################################################################################################
Detailed as Step 1 above: my the block of code below will add new flags to the bad data and I will create a file to
send back to our group.
######################################################################################################################
"""
# LABEL flags to the Bahia San Pedro Set.
mt_array = []
for i in range(0, len(CH_41_S)):
    row = CH_41_S.iloc[i]
    # row = row.reset_index(drop = True)
    if row['DecimalDate'] < 2005:
        row[
            'CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 1 and Tree 2 deviate before 2005. Therefore I am removing all data < 2005'
    else:
        row['CBL_flag'] = '...'
    mt_array.append(row)
toconcat_CH_41_S = pd.DataFrame(mt_array)

# LABEL the outlying measurements from 23 Nikau St. Eastbourne NZ.
# This outlier will re-appear in the plots if you uncomment line 39 which excludes all original flags ("A..")
mt_array = []
for i in range(0, len(NZ_41_S_3)):  # initialize for loop to the length of the 23 Nikau Eastbourne Dataset
    row = NZ_41_S_3.iloc[i]
    if row['C14Flag'] == 'A..' and row['DecimalDate'] == 1995.00274:
        row['CBL_flag'] = 'REMOVED FROM ANALYSIS: Outlying low measurement. Also indicated by "A.." in C14 Flag column.'
    elif row['C14Flag'] == 'A..':
        row['CBL_flag'] = 'Removed due to original C14 Flag "A.."'
    else:
        row['CBL_flag'] = '...'
    mt_array.append(row)
toconcat_NZ_41_S_3 = pd.DataFrame(mt_array)

# LABEL Tree 1 Core 4 from Kapuni as BAD
mt_array = []  # create an empty array. We will dump our sorted data in here
for i in range(0, len(NZ_39_S)):  # initialize a for-loop the length of the site's dataset
    row = NZ_39_S.iloc[i]  # grab the i'th row
    cell = row['Ring code']  # grab the column of data from that row
    if 'C4' in cell:  # if what we're looking for is in there, append it to the array
        row['CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 1 Core 4 does not match bomb spike.'
    else:
        row['CBL_flag'] = '...'
    mt_array.append(row)
toconcat_NZ_39_S = pd.DataFrame(mt_array)

# LABEL Mason's Bay: Only 1 record - remove from Further analysis.
NZ_47_S[
    'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only one record exists, and is post-bomb spike - therefore cannot be validated.'
# NZ_47_S.to_excel('test.xlsx')

# LABEL Monte Tarn Tree 5 Core 1 as BAD
mt_array = []  # create an empty array. We will dump our sorted data in here
for i in range(0, len(CH_54_S)):  # initialize a for-loop the length of the site's dataset
    row = CH_54_S.iloc[i]  # grab the i'th row
    cell = row['Ring code']  # grab the column of data from that row
    if 'T5' in cell:  # if what we're looking for is in there, append it to the array
        row['CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 5 Core 1 does not match bomb spike.'
    else:
        row['CBL_flag'] = '...'
    mt_array.append(row)
toconcat_CH_54_S = pd.DataFrame(mt_array)

# LABEL Muriwai Beach: Only 1 record - remove from Further analysis.
NZ_37_S[
    'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only one record exists, and is post-bomb spike - therefore cannot be validated.'

# LABEL Balmaceda Tree 5 Core 1 as BAD
mt_array = []  # create an empty array. We will dump our sorted data in here
for i in range(0, len(CH_44_S)):  # initialize a for-loop the length of the site's dataset
    row = CH_44_S.iloc[i]  # grab the i'th row
    cell = row['Ring code']  # grab the column of data from that row
    if 'T7' not in cell:  # if what we're looking for is in there, append it to the array
        row[
            'CBL_flag'] = 'REMOVED FROM ANALYSIS: This tree core does not match bomb spike. Only keeping Tree 7 from this site.'
    else:
        row['CBL_flag'] = '...'
    mt_array.append(row)
toconcat_CH_44_S = pd.DataFrame(mt_array)
# toconcat_CH_44_S.to_excel('test.xlsx')

# LABEL the outlying measurements from Tortel Island
# This outlier will re-appear in the plots if you uncomment line 39 which excludes all original flags ("A..")
mt_array = []
for i in range(0, len(CH_48_S_2)):  # initialize for loop to the length of the 23 Nikau Eastbourne Dataset
    row = CH_48_S_2.iloc[i]
    if row['C14Flag'] == 'A..':
        row['CBL_flag'] = 'REMOVED FROM ANALYSIS: Outlying low measurement. Also indicated by "A.." in C14 Flag column.'
    else:
        row['CBL_flag'] = '...'
    mt_array.append(row)
toconcat_CH_48_S_2 = pd.DataFrame(mt_array)

"""
To complete Step 1 outlined on line 566, I'll concatonate all of the newly labeled data to later send to Jocelyn and
will be useful for future readers of the study.
It's getting a little bit complicated to keep straight with all of the indexing so I'm going to quickly summarize
the progress here before I re-concatenate the newly labeled data.
toconcat_CH_41_S -> newly labeled data from Bahia San Pedro, we labeled all data pre-2005
toconcat_CH_44_S -> newly labeled data from Raul Marin Balmaceda, we keep Tree 7, remove the rest
CH_48_S          -> UNALTERED data from Tortel Island
toconcat_CH_48_S_2 -> newly labeled data from Tortel River, labeled one outlier
CH_53_S          -> UNALTERED
toconcat_CH_54_S -> label that we're removing T5 C1 from Monte Tarn
CH_55_S          -> UNALTERED
CH_55_S_2        -> UNALTERED
NZ_37_S          -> Labeled to note that we cannot validate it so the whole dataset will not be used further
toconcat_NZ_39_S -> Labeling that we'll remove Tree 1 Core 4.
NZ_41_S          -> UNALTERED
NZ_41_S_2        -> UNALTERED
toconcat_NZ_41_S_3 -> Labeled one outlier from 23 Nikau St, Eastbourne
NZ_44_S          -> UNALTERED
NZ_46_S          -> UNALTERED
NZ_47_S          -> Labeled to note that we cannot validate it so the whole dataset will not be used further
NZ_53_S          -> UNALTERED
The first thing I'm going to do next is concatonate all of these into a new dataframe.
Then I am going to add '...' in ['CBL_flag'] to all data where it doesn't exist already.
Then, later, I can slice using the '...' to get a new cleaned dataframe which includes ONLY data that we are going
to use from here on out.
##
"""
combine = pd.concat([toconcat_CH_41_S,
                     toconcat_CH_44_S,
                     CH_48_S,
                     toconcat_CH_48_S_2,
                     CH_53_S,
                     toconcat_CH_54_S,
                     CH_55_S,
                     CH_55_S_2,
                     NZ_37_S,
                     toconcat_NZ_39_S,
                     NZ_41_S,
                     NZ_41_S_2,
                     toconcat_NZ_41_S_3,
                     NZ_44_S,
                     NZ_46_S,
                     NZ_47_S,
                     NZ_53_S])  # Keeps ALL Data
combine = combine.reset_index(drop=True)

# # where there is not already a CBL Flag, add '...'
mt_array = []
for i in range(0, len(combine)):
    combine = combine.reset_index(drop=True)
    row = combine.iloc[i]  # grab the i'th row
    x = row['CBL_flag']  # grab the CBL_flag column
    x = str(x)  # change the value to a string
    if x == 'nan':  # if there is no value there
        row['CBL_flag'] = '...'  # change it to '...'
    mt_array.append(row)
combined = pd.DataFrame(mt_array)

"""
Of course, now I need to check that I haven't lost any data. What is the lenght of the original dataframe after I
dropped the Nan's in the beginning, versus now?
They check out!
"""
# print(len(df)) == 648
# print(len(combined2)) == 648
combined.to_excel('SOARTreeRingData_CBL_flags.xlsx')

"""
Finally, I want to remove all the flagged data so I'm only left with things I HAVEN'T Flagged.
"""
df_cleaned = combined.loc[(combined['CBL_flag']) == '...']
# print(len(df_cleaned))
df_cleaned.to_excel('SOARTreeRingData_CBL_cleaned.xlsx')

# now, I've rebooted this code from a previous iteration, and to deal with renaming, I'm going to change from df_cleaned to df to be able to use the res of the code.

# """
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# INDEX ACCORDING TO INDIVIDUAL SITES AND TAKE A LOOK AT THAT:
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# """
#
# # names = np.unique(df['StudySites::Site name'])
# # print(names)
# CH_41_S = df.loc[(df['Site'] == 'Bahia San Pedro, Chile')]
# CH_41_S_x = CH_41_S['DecimalDate']
# CH_41_S_y = CH_41_S['∆14C']
# CH_41_S_off = CH_41_S['offset']
# CH_41_S_off_err = CH_41_S['offset_err_prop']
#
# CH_44_S = df.loc[(df['Site'] == 'Raul Marin Balmaceda')]
# CH_44_S_x = CH_44_S['DecimalDate']
# CH_44_S_y = CH_44_S['∆14C']
# CH_44_S_off = CH_44_S['offset']
# CH_44_S_off_err = CH_44_S['offset_err_prop']
#
# CH_48_S = df.loc[(df['Site'] == 'Tortel island')]
# CH_48_S_x = CH_48_S['DecimalDate']
# CH_48_S_y = CH_48_S['∆14C']
# CH_48_S_off = CH_48_S['offset']
# CH_48_S_off_err = CH_48_S['offset_err_prop']
#
# CH_48_S_2 = df.loc[(df['Site'] == 'Tortel river')]
# CH_48_S_2_x = CH_48_S_2['DecimalDate']
# CH_48_S_2_y = CH_48_S_2['∆14C']
# CH_48_S_2_off = CH_48_S_2['offset']
# CH_48_S_2_off_err = CH_48_S_2['offset_err_prop']
#
# CH_53_S = df.loc[(df['Site'] == 'Seno Skyring')]
# CH_53_S_x = CH_53_S['DecimalDate']
# CH_53_S_y = CH_53_S['∆14C']
# CH_53_S_off = CH_53_S['offset']
# CH_53_S_off_err = CH_53_S['offset_err_prop']
#
# CH_54_S = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
# CH_54_S_x = CH_54_S['DecimalDate']
# CH_54_S_y = CH_54_S['∆14C']
# CH_54_S_off = CH_54_S['offset']
# CH_54_S_off_err = CH_54_S['offset_err_prop']
#
# CH_55_S = df.loc[(df['Site'] == 'Baja Rosales, Isla Navarino')]
# CH_55_S_x = CH_55_S['DecimalDate']
# CH_55_S_y = CH_55_S['∆14C']
# CH_55_S_off = CH_55_S['offset']
# CH_55_S_off_err = CH_55_S['offset_err_prop']
#
# CH_55_S_2 = df.loc[(df['Site'] == 'Puerto Navarino, Isla Navarino')]
# CH_55_S_2_x = CH_55_S_2['DecimalDate']
# CH_55_S_2_y = CH_55_S_2['∆14C']
# CH_55_S_2_off = CH_55_S_2['offset']
# CH_55_S_2_off_err = CH_55_S_2['offset_err_prop']
#
# NZ_37_S = df.loc[(df['Site'] == 'Muriwai Beach Surf Club')]
# NZ_37_S_x = NZ_37_S['DecimalDate']
# NZ_37_S_y = NZ_37_S['∆14C']
# NZ_37_S_off = NZ_37_S['offset']
# NZ_37_S_off_err = NZ_37_S['offset_err_prop']
#
# NZ_39_S = df.loc[(df['Site'] == 'near Kapuni school field, NZ')]
# NZ_39_S_x =NZ_39_S['DecimalDate']
# NZ_39_S_y =NZ_39_S['∆14C']
# NZ_39_S_off =NZ_39_S['offset']
# NZ_39_S_off_err =NZ_39_S['offset_err_prop']
#
# NZ_41_S = df.loc[(df['Site'] == '19 Nikau St, Eastbourne, NZ')]
# NZ_41_S_x =NZ_41_S['DecimalDate']
# NZ_41_S_y =NZ_41_S['∆14C']
# NZ_41_S_off =NZ_41_S['offset']
# NZ_41_S_off_err =NZ_41_S['offset_err_prop']
#
# NZ_41_S_2 = df.loc[(df['Site'] == 'Baring Head, NZ')]
# NZ_41_S_2_x = NZ_41_S_2['DecimalDate']
# NZ_41_S_2_y = NZ_41_S_2['∆14C']
# NZ_41_S_2_off = NZ_41_S_2['offset']
# NZ_41_S_2_off_err = NZ_41_S_2['offset_err_prop']
#
# NZ_41_S_3 = df.loc[(df['Site'] == '23 Nikau St, Eastbourne, NZ')]
# NZ_41_S_3_x = NZ_41_S_3['DecimalDate']
# NZ_41_S_3_y = NZ_41_S_3['∆14C']
# NZ_41_S_3_off = NZ_41_S_3['offset']
# NZ_41_S_3_off_err = NZ_41_S_3['offset_err_prop']
#
# NZ_44_S = df.loc[(df['Site'] == 'Haast Beach, paddock near beach')]
# NZ_44_S_x = NZ_44_S['DecimalDate']
# NZ_44_S_y = NZ_44_S['∆14C']
# NZ_44_S_off = NZ_44_S['offset']
# NZ_44_S_off_err = NZ_44_S['offset_err_prop']
#
# NZ_46_S = df.loc[(df['Site'] == 'Oreti Beach')]
# NZ_46_S_x = NZ_46_S['DecimalDate']
# NZ_46_S_y = NZ_46_S['∆14C']
# NZ_46_S_off = NZ_46_S['offset']
# NZ_46_S_off_err = NZ_46_S['offset_err_prop']
#
# NZ_47_S = df.loc[(df['Site'] == "Mason's Bay Homestead")]
# NZ_47_S_x = NZ_47_S['DecimalDate']
# NZ_47_S_y = NZ_47_S['∆14C']
# NZ_47_S_off = NZ_47_S['offset']
# NZ_47_S_off_err = NZ_47_S['offset_err_prop']
#
# NZ_53_S = df.loc[(df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island")]
# NZ_53_S_x = NZ_53_S['DecimalDate']
# NZ_53_S_y = NZ_53_S['∆14C']
# NZ_53_S_off = NZ_53_S['offset']
# NZ_53_S_off_err = NZ_53_S['offset_err_prop']
#
# size1 = 30
# fig = plt.figure(2)
# plt.scatter(sample_xs2, harmonized_trend, label='harmonized', color='black')
# plt.plot(CH_41_S_x, CH_41_S_y, label='CH_41_S', color=colors[0])
# plt.plot(CH_44_S_x, CH_44_S_y, label='CH_44_S', color=colors[1])
# plt.plot(CH_48_S_x, CH_48_S_y, label='CH_48_S', color=colors[2])
# plt.plot(CH_48_S_2_x, CH_48_S_2_y, label='CH_48_S', color=colors[3])
# plt.plot(CH_53_S_x, CH_53_S_y, label='CH_53_S', color=colors[4])
# plt.plot(CH_54_S_x, CH_54_S_y, label='CH_54_S', color=colors[5])
# plt.plot(CH_55_S_x, CH_55_S_y, label='CH_55_S', color=colors[0])
# plt.plot(CH_55_S_2_x, CH_55_S_2_y, label='CH_55_S', color=colors[1])
#
# plt.plot(NZ_37_S_x, NZ_37_S_y, label='NZ_37_S', color=colors2[0])
# plt.plot(NZ_39_S_x, NZ_39_S_y, label='NZ_39_S', color=colors2[1])
# plt.plot(NZ_41_S_x, NZ_41_S_y, label='NZ_41_S', color=colors2[2])
# plt.plot(NZ_41_S_2_x, NZ_41_S_2_y, label='NZ_41_S', color=colors2[3])
# plt.plot(NZ_41_S_3_x, NZ_41_S_3_y, label='NZ_41_S', color=colors2[4])
# plt.plot(NZ_44_S_x, NZ_44_S_y, label='NZ_44_S', color=colors2[5])
# plt.plot(NZ_46_S_x, NZ_46_S_y, label='NZ_46_S', color=colors2[0])
# plt.plot(NZ_47_S_x, NZ_47_S_y, label='NZ_47_S', color=colors2[1])
# plt.plot(NZ_53_S_x, NZ_53_S_y, label='NZ_53_S', color=colors2[2])
#
# plt.legend(loc='upper right')
# plt.title('Plotting individual sites')
# plt.xlim([1980, 2015])
# plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure4.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# So now we can see how close the tree rings from each site are to the background harmonized dataset.
# At the bomb peak, you can clearly see a discrepancy between the tree rings and the bomb peak.
# But what does it mean at this exact point? And how do I identify meaningful differences between the datasets before
# and after the peak?
# I have pasted the comparison of Rachel's and mine up to this point in my notes.
# How do our offsets compare?
# """
# plt.errorbar(sample_xs, df['offset'], label='Tree Rings offset from background', yerr=df['offset_err_prop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
#
# fig, axs = plt.subplots(2, 4, sharex=True, sharey=True, figsize=(20, 8))
# axs[0, 0].errorbar(CH_41_S_x, CH_41_S_off, label='CH_41_S', yerr=CH_41_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 0].set_title("41\xb0S (Bahia, San Pedro)")
# axs[0, 0].axhline(y=0, color='black', linestyle='-')
# axs[0, 0].set_ylim(-20, 20)
#
# axs[0, 1].errorbar(CH_44_S_x, CH_44_S_off, label='CH_41_S', yerr=CH_44_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 1].set_title("44\xb0S (Raul Marin Balcemeda)")
# axs[0, 1].axhline(y=0, color='black', linestyle='-')
# axs[0, 1].set_ylim(-20, 20)
#
# axs[0, 2].errorbar(CH_48_S_x, CH_48_S_off, label='CH_41_S', yerr=CH_48_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 2].set_title("48\xb0S (Tortel Island)")
# axs[0, 2].axhline(y=0, color='black', linestyle='-')
# axs[0, 2].set_ylim(-20, 20)
#
# axs[0, 3].errorbar(CH_48_S_2_x, CH_48_S_2_off, label='CH_41_S', yerr=CH_48_S_2_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 3].set_title("48\xb0S (Tortel River)")
# axs[0, 3].axhline(y=0, color='black', linestyle='-')
# axs[0, 3].set_ylim(-20, 20)
#
# axs[1, 0].errorbar(CH_53_S_x, CH_53_S_off, label='CH_41_S', yerr=CH_53_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 0].set_title("53\xb0S (Seno Skyring)")
# axs[1, 0].axhline(y=0, color='black', linestyle='-')
# axs[1, 0].set_ylim(-20, 20)
#
# axs[1, 1].errorbar(CH_54_S_x, CH_54_S_off, label='CH_41_S', yerr=CH_54_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 1].set_title("54\xb0S (Monte Tarn, Punta Arenas)")
# axs[1, 1].axhline(y=0, color='black', linestyle='-')
# axs[1, 0].set_ylim(-20, 20)
#
# axs[1, 2].errorbar(CH_55_S_x, CH_55_S_off, label='CH_41_S', yerr=CH_55_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 2].set_title("55\xb0S (Baja Rosales, Isla Navarino)")
# axs[1, 2].axhline(y=0, color='black', linestyle='-')
# axs[1, 2].set_ylim(-20, 20)
#
# axs[1, 3].errorbar(CH_55_S_2_x, CH_55_S_2_off, label='CH_41_S', yerr=CH_55_S_2_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 3].set_title("55\xb0S (Puerto Navarino, Isla Navarino)")
# axs[1, 3].axhline(y=0, color='black', linestyle='-')
# axs[1, 3].set_ylim(-20, 20)
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure5.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
# fig, axs = plt.subplots(2, 5, sharex=True, sharey=True, figsize=(20, 8))
# axs[0, 0].errorbar(NZ_37_S_x, NZ_37_S_off, label='CH_41_S', yerr=NZ_37_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 0].set_title("37\xb0S (Muriwai Beach)")
# axs[0, 0].axhline(y=0, color='black', linestyle='-')
# axs[0, 0].set_ylim(-20, 20)
#
# axs[0, 1].errorbar(NZ_39_S_x, NZ_39_S_off, label='CH_41_S', yerr=NZ_39_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 1].set_title("39\xb0S (Kapuni Beach)")
# axs[0, 1].axhline(y=0, color='black', linestyle='-')
# axs[0, 1].set_ylim(-20, 20)
#
# axs[0, 3].errorbar(NZ_41_S_x, NZ_41_S_off, label='CH_41_S', yerr=NZ_41_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 3].set_title("41\xb0S (Eastbourne)")
# axs[0, 3].axhline(y=0, color='black', linestyle='-')
# axs[0, 3].set_ylim(-20, 20)
#
# axs[0, 2].errorbar(NZ_41_S_2_x, NZ_41_S_2_off, label='CH_41_S', yerr=NZ_41_S_2_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 2].set_title("41\xb0S (Baring Head)")
# axs[0, 2].axhline(y=0, color='black', linestyle='-')
# axs[0, 2].set_ylim(-20, 20)
#
# axs[0, 4].errorbar(NZ_41_S_3_x, NZ_41_S_3_off, label='CH_41_S', yerr=NZ_41_S_3_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[0, 4].set_title("41\xb0S (Eastbourne)")
# axs[0, 4].axhline(y=0, color='black', linestyle='-')
# axs[0, 4].set_ylim(-20, 20)
# # axs[1, 0].ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
#
# axs[1, 1].errorbar(NZ_44_S_x, NZ_44_S_off, label='CH_41_S', yerr=NZ_44_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 1].set_title("44\xb0S (Haast Beach)")
# axs[1, 1].axhline(y=0, color='black', linestyle='-')
# axs[1, 1].set_ylim(-20, 20)
#
# axs[1, 2].errorbar(NZ_46_S_x, NZ_46_S_off, label='CH_41_S', yerr=NZ_46_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 2].set_title("46\xb0S (Oreti Beach)")
# axs[1, 2].axhline(y=0, color='black', linestyle='-')
# axs[1, 0].set_ylim(-20, 20)
#
# axs[1, 3].errorbar(NZ_47_S_x, NZ_47_S_off, label='CH_41_S', yerr=NZ_47_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 3].set_title("47\xb0S (Mason's Bay)")
# axs[1, 3].axhline(y=0, color='black', linestyle='-')
# axs[1, 3].set_ylim(-20, 20)
#
# axs[1, 4].errorbar(NZ_53_S_x, NZ_53_S_off, label='CH_41_S', yerr=NZ_53_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
# axs[1, 4].set_title("53\xb0S (World's Lonliest Tree)")
# axs[1, 4].axhline(y=0, color='black', linestyle='-')
# axs[1, 4].set_ylim(-20, 20)
#
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure6.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# We can also index according to LATITUDE ONLY and see how the plots look
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# """
# # break up the data into two DataFrames based on their location, and remove all data before 1980.
# df = df.loc[(df['DecimalDate'] >= 1980)].reset_index(drop=True)  # TODO after analysis is finished, come back to time before 1980
# nz = df.loc[(df['Lon'] > 100)].reset_index(drop=True)
# chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)].reset_index(drop=True)
# chile['new_Lon'] = chile['Lon'] * -1
# # chile.to_excel('chile.xlsx')
# # chile['Lon_adjust'] = np.prod(chile['Lon'], -1)
# # Chile data still needs LONS to be changed to negative, but OK for now
#
# # index the NZ Data based on Latitude
# # I'm changing this from a previous version to bound the data at latitudes based on our data availability, rather
# # than arbitrarily at 5 degree increments.
# # nz_40 = nz.loc[(nz['Lat'] >= -40)]  # check it's working: print(np.unique(nz_40.Site))
# nz_40_45 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36)]
# nz_45_50 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43)]
# nz_50_55 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50)]  # > -998 keeps this portion from grabbing the Eastborne data.
# # check it works -> print(np.unique(nz_50_55.Site))
#
# # index the Chile Data based on latitude
# ch_40_45 = chile.loc[(chile['Lat'] > -45) & (chile['Lat'] <= -40)]
# ch_45_50 = chile.loc[(chile['Lat'] > -50) & (chile['Lat'] <= -45)]
# ch_50_56 = chile.loc[(chile['Lat'] > -56) & (chile['Lat'] <= -50)]
# # print(np.unique(ch_50_56.Site))
#
# """
# LINEAR REGRESSION OF NZ DATA
# """
# # A_40 = np.vstack([nz_40['DecimalDate'], np.ones(len(nz_40['DecimalDate']))]).T
# # m_40, c_40 = np.linalg.lstsq(A_40, nz_40['offset'], rcond=None)[0]
#
# A_40_45 = np.vstack([nz_40_45['DecimalDate'], np.ones(len(nz_40_45['DecimalDate']))]).T
# m_40_45, c_40_45 = np.linalg.lstsq(A_40_45, nz_40_45['offset'], rcond=None)[0]
#
# A_45_50 = np.vstack([nz_45_50['DecimalDate'], np.ones(len(nz_45_50['DecimalDate']))]).T
# m_45_50, c_45_50 = np.linalg.lstsq(A_45_50, nz_45_50['offset'], rcond=None)[0]
#
# A_50_55 = np.vstack([nz_50_55['DecimalDate'], np.ones(len(nz_50_55['DecimalDate']))]).T
# m_50_55, c_50_55 = np.linalg.lstsq(A_50_55, nz_50_55['offset'], rcond=None)[0]
#
#
# size1 = 30
# fig = plt.figure(7)
# # plt.scatter(nz_40['DecimalDate'], nz_40['offset'], marker='o', label='Southern Hemisphere Harmonized Dataset',
# #             color=colors2[5], s=size1, alpha=0.7)
# # plt.plot(nz_40['DecimalDate'], m_40 * nz_40['DecimalDate'] + c_40, label='40S', color=colors2[1], linestyle = "dotted")
# plt.plot(nz_40_45['DecimalDate'], m_40_45 * nz_40_45['DecimalDate'] + c_40_45, label='36-42S', color=colors2[2], linestyle = "dashdot")
# plt.plot(nz_45_50['DecimalDate'], m_45_50 * nz_45_50['DecimalDate'] + c_45_50, label='43-48S', color=colors2[3], linestyle = "dashed")
# plt.plot(nz_50_55['DecimalDate'], m_50_55 * nz_50_55['DecimalDate'] + c_50_55, label='53S', color=colors2[4])
# plt.title('New Zealand Tree Ring Offsets Linearly Regressed')
# plt.legend()
# # plt.xlim([1980, 2020])
# plt.ylim([-15, 10])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure7.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# LINEAR REGRESSION OF CHILE DATA
# """
# B_40_45 = np.vstack([ch_40_45['DecimalDate'], np.ones(len(ch_40_45['DecimalDate']))]).T
# n_40_45, d_40_45 = np.linalg.lstsq(B_40_45, ch_40_45['offset'], rcond=None)[0]
#
# B_45_50 = np.vstack([ch_45_50['DecimalDate'], np.ones(len(ch_45_50['DecimalDate']))]).T
# n_45_50, d_45_50 = np.linalg.lstsq(B_45_50, ch_45_50['offset'], rcond=None)[0]
#
# B_50_56 = np.vstack([ch_50_56['DecimalDate'], np.ones(len(ch_50_56['DecimalDate']))]).T
# n_50_56, d_50_56 = np.linalg.lstsq(B_50_56, ch_50_56['offset'], rcond=None)[0]
#
# size1 = 30
# fig = plt.figure(2)
# # plt.scatter(nz_40['DecimalDate'], nz_40['offset'], marker='o', label='Southern Hemisphere Harmonized Dataset',
# #             color=colors2[5], s=size1, alpha=0.7)plt.
# plt.plot(ch_40_45['DecimalDate'], n_40_45 * ch_40_45['DecimalDate'] + d_40_45, label='40-45S', color=colors2[2], linestyle = "dashdot")
# plt.plot(ch_45_50['DecimalDate'], n_45_50 * ch_45_50['DecimalDate'] + d_45_50, label='45-50S', color=colors2[3], linestyle = "dashed")
# plt.plot(ch_50_56['DecimalDate'], n_50_56 * ch_50_56['DecimalDate'] + d_50_56, label='50-56S', color=colors2[4])
# plt.title('Chilean Tree Ring Offsets Linearly Regressed')
# plt.legend()
# # plt.xlim([1980, 2020])
# # plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure8.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# AND THEN YOU CAN INDEX BASED ON LATITUDE AND TIME.
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# #######################################################################################################################
# """
#
# # indexing the data according to the matrix in my DataScience Notebook:
# # I'm changing this from a previous version to bound the data at latitudes based on our data availability, rather
# # than arbitrarily at 5 degree increments.
# # nz_a1 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]  # North of 40S, 1980 - 1990
# # nz_a2 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]  # North of 40S, 1990 - 2000
# # nz_a3 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]  # etc...
# # nz_a4 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]
#
# nz_b1 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]
# nz_b2 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
# nz_b3 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
# nz_b4 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]
#
# nz_c1 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]
# nz_c2 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
# nz_c3 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
# nz_c4 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]
#
# nz_d1 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]  # > -998 keeps this portion from grabbing the Eastborne data set at -999.
# nz_d2 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
# nz_d3 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
# nz_d4 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]
#
# """
# Perform the linear regression for each time period and latitude range:
#
# https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
# """
# # A_nz_a1 = np.vstack([nz_a1['DecimalDate'], np.ones(len(nz_a1['DecimalDate']))]).T
# # A_nz_a2 = np.vstack([nz_a2['DecimalDate'], np.ones(len(nz_a2['DecimalDate']))]).T
# # A_nz_a3 = np.vstack([nz_a3['DecimalDate'], np.ones(len(nz_a3['DecimalDate']))]).T
# # A_nz_a4 = np.vstack([nz_a4['DecimalDate'], np.ones(len(nz_a4['DecimalDate']))]).T
#
# A_nz_b1 = np.vstack([nz_b1['DecimalDate'], np.ones(len(nz_b1['DecimalDate']))]).T
# A_nz_b2 = np.vstack([nz_b2['DecimalDate'], np.ones(len(nz_b2['DecimalDate']))]).T
# A_nz_b3 = np.vstack([nz_b3['DecimalDate'], np.ones(len(nz_b3['DecimalDate']))]).T
# A_nz_b4 = np.vstack([nz_b4['DecimalDate'], np.ones(len(nz_b4['DecimalDate']))]).T
#
# A_nz_c1 = np.vstack([nz_c1['DecimalDate'], np.ones(len(nz_c1['DecimalDate']))]).T
# A_nz_c2 = np.vstack([nz_c2['DecimalDate'], np.ones(len(nz_c2['DecimalDate']))]).T
# A_nz_c3 = np.vstack([nz_c3['DecimalDate'], np.ones(len(nz_c3['DecimalDate']))]).T
# A_nz_c4 = np.vstack([nz_c4['DecimalDate'], np.ones(len(nz_c4['DecimalDate']))]).T
#
# A_nz_d1 = np.vstack([nz_d1['DecimalDate'], np.ones(len(nz_d1['DecimalDate']))]).T
# A_nz_d2 = np.vstack([nz_d2['DecimalDate'], np.ones(len(nz_d2['DecimalDate']))]).T
# A_nz_d3 = np.vstack([nz_d3['DecimalDate'], np.ones(len(nz_d3['DecimalDate']))]).T
# A_nz_d4 = np.vstack([nz_d4['DecimalDate'], np.ones(len(nz_d4['DecimalDate']))]).T
#
# # m_a1, c_a1 = np.linalg.lstsq(A_nz_a1, nz_a1['offset'], rcond=None)[0]
# # m_a2, c_a2 = np.linalg.lstsq(A_nz_a2, nz_a2['offset'], rcond=None)[0]
# # m_a3, c_a3 = np.linalg.lstsq(A_nz_a3, nz_a3['offset'], rcond=None)[0]
# # m_a4, c_a4 = np.linalg.lstsq(A_nz_a4, nz_a4['offset'], rcond=None)[0]
#
# m_b1, c_b1 = np.linalg.lstsq(A_nz_b1, nz_b1['offset'], rcond=None)[0]
# m_b2, c_b2 = np.linalg.lstsq(A_nz_b2, nz_b2['offset'], rcond=None)[0]
# m_b3, c_b3 = np.linalg.lstsq(A_nz_b3, nz_b3['offset'], rcond=None)[0]
# m_b4, c_b4 = np.linalg.lstsq(A_nz_b4, nz_b4['offset'], rcond=None)[0]
#
# m_c1, c_c1 = np.linalg.lstsq(A_nz_c1, nz_c1['offset'], rcond=None)[0]
# m_c2, c_c2 = np.linalg.lstsq(A_nz_c2, nz_c2['offset'], rcond=None)[0]
# m_c3, c_c3 = np.linalg.lstsq(A_nz_c3, nz_c3['offset'], rcond=None)[0]
# m_c4, c_c4 = np.linalg.lstsq(A_nz_c4, nz_c4['offset'], rcond=None)[0]
#
# m_d1, c_d1 = np.linalg.lstsq(A_nz_d1, nz_d1['offset'], rcond=None)[0]
# m_d2, c_d2 = np.linalg.lstsq(A_nz_d2, nz_d2['offset'], rcond=None)[0]
# m_d3, c_d3 = np.linalg.lstsq(A_nz_d3, nz_d3['offset'], rcond=None)[0]
# m_d4, c_d4 = np.linalg.lstsq(A_nz_d4, nz_d4['offset'], rcond=None)[0]
#
#
# """
# Testing the Figure
# """
# colors = sns.color_palette("rocket", 6)
# colors2 = sns.color_palette("mako", 6)
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['font.size'] = 10
# a = 0.15
# size1 = 15
# fig = plt.figure(2)
# # plt.plot(nz_a1['DecimalDate'], m_a1*nz_a1['DecimalDate'] + c_a1, label='North of 40S', color='black', linestyle = "dashdot")
# # plt.plot(nz_a2['DecimalDate'], m_a2*nz_a2['DecimalDate'] + c_a2, color='black', linestyle = "dashdot")
# # plt.plot(nz_a3['DecimalDate'], m_a3*nz_a3['DecimalDate'] + c_a3, color='black', linestyle = "dashdot")
# # plt.plot(nz_a4['DecimalDate'], m_a4*nz_a4['DecimalDate'] + c_a4, color='black', linestyle = "dashdot")
# #
# # plt.scatter(nz_a1['DecimalDate'], nz_a1['offset'], alpha = a, color='black', s = size1)
# # plt.scatter(nz_a2['DecimalDate'], nz_a2['offset'], alpha = a, color='black', s = size1)
# # plt.scatter(nz_a3['DecimalDate'], nz_a3['offset'], alpha = a, color='black', s = size1)
# # plt.scatter(nz_a4['DecimalDate'], nz_a4['offset'], alpha = a, color='black', s = size1)
#
# # TODO fix the B part of the matrix - doesn't seem to be indexing properly.
# plt.plot(nz_b1['DecimalDate'], m_b1*nz_b1['DecimalDate'] + c_b1, label='36-42S', color=colors2[2], linestyle = "dashdot")
# plt.plot(nz_b2['DecimalDate'], m_b2*nz_b2['DecimalDate'] + c_b2, color=colors2[2], linestyle = "dashdot")
# plt.plot(nz_b3['DecimalDate'], m_b3*nz_b3['DecimalDate'] + c_b3, color=colors2[2], linestyle = "dashdot")
# plt.plot(nz_b4['DecimalDate'], m_b4*nz_b4['DecimalDate'] + c_b4, color=colors2[2], linestyle = "dashdot")
#
# plt.scatter(nz_b1['DecimalDate'], nz_b1['offset'], alpha = a, color=colors2[2], s = size1)
# plt.scatter(nz_b2['DecimalDate'], nz_b2['offset'], alpha = a, color=colors2[2], s = size1)
# plt.scatter(nz_b3['DecimalDate'], nz_b3['offset'], alpha = a, color=colors2[2], s = size1)
# plt.scatter(nz_b4['DecimalDate'], nz_b4['offset'], alpha = a, color=colors2[2], s = size1)
#
#
# plt.plot(nz_c1['DecimalDate'], m_c1*nz_c1['DecimalDate'] + c_c1, label='43-48S', color=colors2[3], linestyle = "dashed")
# plt.plot(nz_c2['DecimalDate'], m_c2*nz_c2['DecimalDate'] + c_c2, color=colors2[3], linestyle = "dashed")
# plt.plot(nz_c3['DecimalDate'], m_c3*nz_c3['DecimalDate'] + c_c3, color=colors2[3], linestyle = "dashed")
# plt.plot(nz_c4['DecimalDate'], m_c4*nz_c4['DecimalDate'] + c_c4,  color=colors2[3], linestyle = "dashed")
#
# plt.scatter(nz_c1['DecimalDate'], nz_c1['offset'], alpha = a, color=colors2[3], s = size1)
# plt.scatter(nz_c2['DecimalDate'], nz_c2['offset'], alpha = a, color=colors2[3], s = size1)
# plt.scatter(nz_c3['DecimalDate'], nz_c3['offset'], alpha = a, color=colors2[3], s = size1)
# plt.scatter(nz_c4['DecimalDate'], nz_c4['offset'], alpha = a, color=colors2[3], s = size1)
#
# plt.plot(nz_d1['DecimalDate'], m_d1*nz_d1['DecimalDate'] + c_d1, label='53S', color=colors2[4], linestyle = "solid")
# plt.plot(nz_d2['DecimalDate'], m_d2*nz_d2['DecimalDate'] + c_d2, color=colors2[4], linestyle = "solid")
# plt.plot(nz_d3['DecimalDate'], m_d3*nz_d3['DecimalDate'] + c_d3, color=colors2[4], linestyle = "solid")
# plt.plot(nz_d4['DecimalDate'], m_d4*nz_d4['DecimalDate'] + c_d4, color=colors2[4], linestyle = "solid")
#
# plt.scatter(nz_d1['DecimalDate'], nz_d1['offset'], alpha = a, color=colors2[4], s = size1)
# plt.scatter(nz_d2['DecimalDate'], nz_d2['offset'], alpha = a, color=colors2[4], s = size1)
# plt.scatter(nz_d3['DecimalDate'], nz_d3['offset'], alpha = a, color=colors2[4], s = size1)
# plt.scatter(nz_d4['DecimalDate'], nz_d4['offset'], alpha = a, color=colors2[4], s = size1)
# plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
# plt.xlim([1980, 2020])
# plt.ylim([-15, 10])
# plt.legend()
# plt.title('New Zealand Tree Ring Offsets by Latitude and Year')
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure9.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
#
# """
# Trying to do the same as above for the Chile data
# """
#
# chile_a1 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]  # North of 40S, 1980 - 1990
# chile_a2 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]  # North of 40S, 1990 - 2000
# chile_a3 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]  # etc...
# chile_a4 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]
#
# chile_b1 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]
# chile_b2 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
# chile_b3 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
# chile_b4 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]
#
# chile_c1 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]
# chile_c2 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
# chile_c3 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
# chile_c4 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]
#
# chile_d1 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]  # > -998 keeps this portion from grabbing the Eastborne data set at -999.
# chile_d2 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
# chile_d3 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
# chile_d4 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]
#
# A_chile_a1 = np.vstack([chile_a1['DecimalDate'], np.ones(len(chile_a1['DecimalDate']))]).T
# A_chile_a2 = np.vstack([chile_a2['DecimalDate'], np.ones(len(chile_a2['DecimalDate']))]).T
# A_chile_a3 = np.vstack([chile_a3['DecimalDate'], np.ones(len(chile_a3['DecimalDate']))]).T
# A_chile_a4 = np.vstack([chile_a4['DecimalDate'], np.ones(len(chile_a4['DecimalDate']))]).T
#
# A_chile_b1 = np.vstack([chile_b1['DecimalDate'], np.ones(len(chile_b1['DecimalDate']))]).T
# A_chile_b2 = np.vstack([chile_b2['DecimalDate'], np.ones(len(chile_b2['DecimalDate']))]).T
# A_chile_b3 = np.vstack([chile_b3['DecimalDate'], np.ones(len(chile_b3['DecimalDate']))]).T
# A_chile_b4 = np.vstack([chile_b4['DecimalDate'], np.ones(len(chile_b4['DecimalDate']))]).T
#
# A_chile_c1 = np.vstack([chile_c1['DecimalDate'], np.ones(len(chile_c1['DecimalDate']))]).T
# A_chile_c2 = np.vstack([chile_c2['DecimalDate'], np.ones(len(chile_c2['DecimalDate']))]).T
# A_chile_c3 = np.vstack([chile_c3['DecimalDate'], np.ones(len(chile_c3['DecimalDate']))]).T
# A_chile_c4 = np.vstack([chile_c4['DecimalDate'], np.ones(len(chile_c4['DecimalDate']))]).T
#
# A_chile_d1 = np.vstack([chile_d1['DecimalDate'], np.ones(len(chile_d1['DecimalDate']))]).T
# A_chile_d2 = np.vstack([chile_d2['DecimalDate'], np.ones(len(chile_d2['DecimalDate']))]).T
# A_chile_d3 = np.vstack([chile_d3['DecimalDate'], np.ones(len(chile_d3['DecimalDate']))]).T
# A_chile_d4 = np.vstack([chile_d4['DecimalDate'], np.ones(len(chile_d4['DecimalDate']))]).T
#
# m_a1, c_a1 = np.linalg.lstsq(A_chile_a1, chile_a1['offset'], rcond=None)[0]
# m_a2, c_a2 = np.linalg.lstsq(A_chile_a2, chile_a2['offset'], rcond=None)[0]
# m_a3, c_a3 = np.linalg.lstsq(A_chile_a3, chile_a3['offset'], rcond=None)[0]
# m_a4, c_a4 = np.linalg.lstsq(A_chile_a4, chile_a4['offset'], rcond=None)[0]
#
# m_b1, c_b1 = np.linalg.lstsq(A_chile_b1, chile_b1['offset'], rcond=None)[0]
# m_b2, c_b2 = np.linalg.lstsq(A_chile_b2, chile_b2['offset'], rcond=None)[0]
# m_b3, c_b3 = np.linalg.lstsq(A_chile_b3, chile_b3['offset'], rcond=None)[0]
# m_b4, c_b4 = np.linalg.lstsq(A_chile_b4, chile_b4['offset'], rcond=None)[0]
#
# m_c1, c_c1 = np.linalg.lstsq(A_chile_c1, chile_c1['offset'], rcond=None)[0]
# m_c2, c_c2 = np.linalg.lstsq(A_chile_c2, chile_c2['offset'], rcond=None)[0]
# m_c3, c_c3 = np.linalg.lstsq(A_chile_c3, chile_c3['offset'], rcond=None)[0]
# m_c4, c_c4 = np.linalg.lstsq(A_chile_c4, chile_c4['offset'], rcond=None)[0]
#
# m_d1, c_d1 = np.linalg.lstsq(A_chile_d1, chile_d1['offset'], rcond=None)[0]
# m_d2, c_d2 = np.linalg.lstsq(A_chile_d2, chile_d2['offset'], rcond=None)[0]
# m_d3, c_d3 = np.linalg.lstsq(A_chile_d3, chile_d3['offset'], rcond=None)[0]
# m_d4, c_d4 = np.linalg.lstsq(A_chile_d4, chile_d4['offset'], rcond=None)[0]
#
# """
# Testing the Figure
# """
# colors = sns.color_palette("rocket", 6)
# colors2 = sns.color_palette("mako", 6)
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['font.size'] = 10
# a = 0.15
# size1 = 15
# fig = plt.figure(3)
# # plt.plot(chile_a1['DecimalDate'], m_a1*chile_a1['DecimalDate'] + c_a1, label='North of 40S', color='black', linestyle = "dashdot")
# # plt.plot(chile_a2['DecimalDate'], m_a2*chile_a2['DecimalDate'] + c_a2, color='black', linestyle = "dashdot")
# # plt.plot(chile_a3['DecimalDate'], m_a3*chile_a3['DecimalDate'] + c_a3, color='black', linestyle = "dashdot")
# # plt.plot(chile_a4['DecimalDate'], m_a4*chile_a4['DecimalDate'] + c_a4, color='black', linestyle = "dashdot")
# #
# # plt.scatter(chile_a1['DecimalDate'], chile_a1['offset'], alpha = a, color='black', s = size1)
# # plt.scatter(chile_a2['DecimalDate'], chile_a2['offset'], alpha = a, color='black', s = size1)
# # plt.scatter(chile_a3['DecimalDate'], chile_a3['offset'], alpha = a, color='black', s = size1)
# # plt.scatter(chile_a4['DecimalDate'], chile_a4['offset'], alpha = a, color='black', s = size1)
# # There is no data at higher than 40S for the Chilean sites#
#
# plt.plot(chile_b1['DecimalDate'], m_b1*chile_b1['DecimalDate'] + c_b1, label='40-45S', color=colors[1], linestyle = "dotted")
# plt.plot(chile_b2['DecimalDate'], m_b2*chile_b2['DecimalDate'] + c_b2, color=colors[1], linestyle = "dotted")
# plt.plot(chile_b3['DecimalDate'], m_b3*chile_b3['DecimalDate'] + c_b3, color=colors[1], linestyle = "dotted")
# plt.plot(chile_b4['DecimalDate'], m_b4*chile_b4['DecimalDate'] + c_b4, color=colors[1], linestyle = "dotted")
#
# plt.scatter(chile_b1['DecimalDate'], chile_b1['offset'], alpha = a, color=colors[1], s = size1)
# plt.scatter(chile_b2['DecimalDate'], chile_b2['offset'], alpha = a, color=colors[1], s = size1)
# plt.scatter(chile_b3['DecimalDate'], chile_b3['offset'], alpha = a, color=colors[1], s = size1)
# plt.scatter(chile_b4['DecimalDate'], chile_b4['offset'], alpha = a, color=colors[1], s = size1)
#
# plt.plot(chile_c1['DecimalDate'], m_c1*chile_c1['DecimalDate'] + c_c1, label='45-50S', color=colors2[1], linestyle = "dashed")
# plt.plot(chile_c2['DecimalDate'], m_c2*chile_c2['DecimalDate'] + c_c2, color=colors2[1], linestyle = "dashed")
# plt.plot(chile_c3['DecimalDate'], m_c3*chile_c3['DecimalDate'] + c_c3, color=colors2[1], linestyle = "dashed")
# plt.plot(chile_c4['DecimalDate'], m_c4*chile_c4['DecimalDate'] + c_c4,  color=colors2[1], linestyle = "dashed")
#
# plt.scatter(chile_c1['DecimalDate'], chile_c1['offset'], alpha = a, color=colors2[1], s = size1)
# plt.scatter(chile_c2['DecimalDate'], chile_c2['offset'], alpha = a, color=colors2[1], s = size1)
# plt.scatter(chile_c3['DecimalDate'], chile_c3['offset'], alpha = a, color=colors2[1], s = size1)
# plt.scatter(chile_c4['DecimalDate'], chile_c4['offset'], alpha = a, color=colors2[1], s = size1)
#
# plt.plot(chile_d1['DecimalDate'], m_d1*chile_d1['DecimalDate'] + c_d1, label='50-55S', color=colors[5], linestyle = "solid")
# plt.plot(chile_d2['DecimalDate'], m_d2*chile_d2['DecimalDate'] + c_d2, color=colors[5], linestyle = "solid")
# plt.plot(chile_d3['DecimalDate'], m_d3*chile_d3['DecimalDate'] + c_d3, color=colors[5], linestyle = "solid")
# plt.plot(chile_d4['DecimalDate'], m_d4*chile_d4['DecimalDate'] + c_d4, color=colors[5], linestyle = "solid")
#
# plt.scatter(chile_d1['DecimalDate'], chile_d1['offset'], alpha = a, color=colors[5], s = size1)
# plt.scatter(chile_d2['DecimalDate'], chile_d2['offset'], alpha = a, color=colors[5], s = size1)
# plt.scatter(chile_d3['DecimalDate'], chile_d3['offset'], alpha = a, color=colors[5], s = size1)
# plt.scatter(chile_d4['DecimalDate'], chile_d4['offset'], alpha = a, color=colors[5], s = size1)
# plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
# plt.title('Chilean Tree Ring Record Offsets Linearly Regressed')
# # plt.xlim([1980, 2020])
# # plt.ylim([-15, 10])
# plt.legend()
# plt.title('Chile Tree Ring Offsets by Latitude and Year')
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure10.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# The trends seen in the data above: Figures 9 and 10, aren't really that helpful. For example, one line can be drawn from
# 20 points while the other is 1 or 2 points. This is not represented at all in the Figure and will lead to unoptomized
# interpretations.
# I need to figure out some way to weigh the trend-lines based on how many data points are there.
#
# It also occurs to me now that a useful way to understand how to interpret my data is to actually understand
# visually where my data IS. ::: See Below
#
# """
#
# plt.close()  # some other figure kept popping up...
#
# """
# First, initialize the figure and prepare to draw the squares
# """
# # initialize where the boxes will go, and where my figures a and b will be drawn.
# maxlat = -30
# minlat = -60
# nz_max_lon = 180
# nz_min_lon = 160
# chile_max_lon = -60
# chile_min_lon = -80
#
# # initialize the figure and subplots.
# fig = plt.figure()
# plt.subplots_adjust(wspace=.2)
# res = 'i'  # todo switch to i for intermediate
# land = 'coral'
# # what do i want the size of the dots to be where the tree rings are from?
# size1 = 10
# """
# Add first subplot: the globe centered around antarctica
# """
#
# ax = fig.add_subplot(131)
# map = Basemap(lat_0=-90, lon_0=0, resolution=res, projection='ortho')
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.1)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries(linewidth=0.5)
#
# # plot where my new zealand subplot is on the globe
# x1, y1 = map(nz_min_lon, maxlat)
# x2, y2 = map(nz_max_lon, maxlat)
# x3, y3 = map(nz_max_lon, minlat)
# x4, y4 = map(nz_min_lon, minlat)
# poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor="none", edgecolor='black',linewidth=1, alpha=1)
# plt.gca().add_patch(poly)
#
# # plot where my chile subplot is on the globe
# x5, y5 = map(chile_min_lon, maxlat)
# x6, y6 = map(chile_max_lon, maxlat)
# x7, y7 = map(chile_max_lon, minlat)
# x8, y8 = map(chile_min_lon, minlat)
# poly2 = Polygon([(x5,y5),(x6,y6),(x7,y7),(x8,y8)], facecolor="none",edgecolor='black',linewidth=1,alpha=1)
# plt.gca().add_patch(poly2)
#
#
# """
# Add second subplot
# """
#
# ax = fig.add_subplot(132)
# plt.subplots_adjust(wspace=.25)
# # ax.set_title("Chilean Tree Ring Sites")
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=chile_min_lon, urcrnrlon=chile_max_lon, resolution=res)
# # parameters to make the plot more beautiful
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries(linewidth=0.5)
# map.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
# map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
# chile_lat = chile['Lat']
# chile_lon = chile['new_Lon']
#
# z, a = map(chile_lon, chile_lat)
#
# map.scatter(z, a, marker='D',color='m', s = size1)
# """
# Add third subplot
# """
# ax = fig.add_subplot(133)
# map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
# # parameters to make the plot more beautiful
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.5)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries()
# map.drawparallels(np.arange(-90, 90, 10), labels=[False, False, False, False], fontsize=7, linewidth=0.5)
# map.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
# nz_lat = nz['Lat']
# nz_lon = nz['Lon']
# x, y = map(nz_lon, nz_lat)
# map.scatter(x, y, marker='D',color='m', s= size1)
#
# # ax.set_title('New Zealand Tree Ring Sampling Sites')
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/maptest.png',
#









































































#
#
#
#
#
#
# CH_41_S = CH_41_S.reset_index(drop=True)  # reset the index or you get type-setting errors
# empty_array = []  # create an empty array. We will dump our sorted data in here
# for i in range(0, len(CH_41_S)):  # initialize a for-loop the length of the site's dataset
#     row = CH_41_S.iloc[i]  # grab the i'th row
#     cell = row['Ring code']  # grab the column of data from that row
#     element = 'T1'  # what is the element that we're looking for?
#     if element in cell:  # if what we're looking for is in there, append it to the array
#         empty_array.append(row)
# CH_41_S_core1 = pd.DataFrame(empty_array)  # take the array and put into a Pandas Dataframe.
#
# empty_array = []  # create an empty array. We will dump our sorted data in here
# for i in range(0, len(CH_41_S)):  # initialize a for-loop the length of the site's dataset
#     row = CH_41_S.iloc[i]  # grab the i'th row
#     cell = row['Ring code']  # grab the column of data from that row
#     element = 'T2'  # what is the element that we're looking for?
#     if element in cell:  # if what we're looking for is in there, append it to the array
#         empty_array.append(row)
# CH_41_S_core2 = pd.DataFrame(empty_array)  # take the array and put into a Pandas Dataframe.
# #
# x = CH_41_S_core1['DecimalDate']
# y = CH_41_S_core1['∆14C']
# z = CH_41_S_core1['∆14Cerr']
# x2 = CH_41_S_core2['DecimalDate']
# y2 = CH_41_S_core2['∆14C']
# z2 = CH_41_S_core2['∆14Cerr']

# size = 50
# plt.errorbar(x, y, label='Tree 1', yerr=z, fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
# plt.errorbar(x2, y2, label='Tree 2', yerr=z2, fmt='o', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
# plt.plot(harm_xs, harm_ys, label='Southern Hemisphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
# plt.legend()
# plt.title('Bahia San Pedro, Chile')
# plt.xlim(min(CH_41_S['DecimalDate'] - 5), max(CH_41_S['DecimalDate'] + 5))
# plt.ylim(min(CH_41_S['∆14C'] - 25), max(CH_41_S['∆14C'] + 25))
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig(
#     'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/SOAR_tree_rings/BahiaSanPedro_validation.png',
#     dpi=300, bbox_inches="tight")

# """
# Second one
# 'Raul Marin Balmaceda'
# T3 - Core 3, Core 2
# T4 - Core 1
# T7 - Core 1
#
# Elements will be:
# T3-C2
# T4-C1
# T7-C1
#
# """
#
#
# # CH_44_S.to_excel('test1.xlsx')
# # TODO.. i should be able to break up the following into a function for less copy pasting...
#
# def tree_ring_validation(df, element):
#     df = df.reset_index(drop=True)  # reset the index or you get type-setting errors
#     empty_array = []  # create an empty array. We will dump our sorted data in here
#     for i in range(0, len(df)):  # initialize a for-loop the length of the site's dataset
#         row = df.iloc[i]  # grab the i'th row
#         cell = row['Ring code']  # grab the column of data from that row
#         if element in cell:  # if what we're looking for is in there, append it to the array
#             empty_array.append(row)
#     df_new = pd.DataFrame(empty_array)  # take the array and put into a Pandas Dataframe.
#
#
# CH_44_S = CH_44_S.reset_index(drop=True)  # reset the index or you get type-setting errors
# empty_array = []  # create an empty array. We will dump our sorted data in here
# for i in range(0, len(CH_44_S)):  # initialize a for-loop the length of the site's dataset
#     row = CH_44_S.iloc[i]  # grab the i'th row
#     cell = row['Ring code']  # grab the column of data from that row
#     element = 'T1'  # what is the element that we're looking for?
#     if element in cell:  # if what we're looking for is in there, append it to the array
#         empty_array.append(row)
# CH_41_S_core1 = pd.DataFrame(empty_array)  # take the array and put into a Pandas Dataframe.
#
# empty_array = []  # create an empty array. We will dump our sorted data in here
# for i in range(0, len(CH_41_S)):  # initialize a for-loop the length of the site's dataset
#     row = CH_41_S.iloc[i]  # grab the i'th row
#     cell = row['Ring code']  # grab the column of data from that row
#     element = 'T2'  # what is the element that we're looking for?
#     if element in cell:  # if what we're looking for is in there, append it to the array
#         empty_array.append(row)
# CH_41_S_core2 = pd.DataFrame(empty_array)  # take the array and put into a Pandas Dataframe.
#
# x = CH_41_S_core1['DecimalDate']
# y = CH_41_S_core1['∆14C']
# z = CH_41_S_core1['∆14Cerr']
# x2 = CH_41_S_core2['DecimalDate']
# y2 = CH_41_S_core2['∆14C']
# z2 = CH_41_S_core2['∆14Cerr']
#
# size = 50
# plt.errorbar(x, y, label='Tree 1', yerr=z, fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
# plt.errorbar(x2, y2, label='Tree 2', yerr=z2, fmt='o', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
# plt.plot(harm_xs, harm_ys, label='Southern Hemisphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
# plt.legend()
# plt.title('Bahia San Pedro, Chile')
# plt.xlim(min(CH_41_S['DecimalDate'] - 5), max(CH_41_S['DecimalDate'] + 5))
# plt.ylim(min(CH_41_S['∆14C'] - 25), max(CH_41_S['∆14C'] + 25))
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig(
#     'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/SOAR_tree_rings/BahiaSanPedro_validation.png',
#     dpi=300, bbox_inches="tight")
#
# #
# #
# #


# CH_41_S = CH_41_S.reset_index(drop=True)  # reset the index or you get type-setting errors
# x = CH_41_S['Ring code']
# print(x)
# print(type(x[1]))

#
# # importing the tree-ring x-values from the file I've read in.
# sample_xs = (df['DecimalDate'])
# # I want the harmonized dataset to be smoothed using CCGCRV, and
# # I want it to OUTPUT the values at the specific x values that I have for tree-ring data.
# # the following lines of code slightly change the data format of the x-data to appease the Monte Carlo code.
# sample_xs2 = pd.DataFrame({'x': sample_xs})
#
# # Smooth the harmonized data using CCGCRV and have the output at the same time as tree ring x's
# # input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
# cutoff = 667
# harmonized_trend = ccgFilter(harm_xs, harm_ys, cutoff).getTrendValue(sample_xs2)
# harmonized_trend = pd.DataFrame({'harmonized_data_trended': np.concatenate(harmonized_trend)})  # put the output into a dataframe
#
# # error estimate on the harmonized data trended using CCGCRV
# n = 10  # TODO change back to 10,000
# errors = monte_carlo_randomization_Trend(harm_xs, sample_xs2, harm_ys, harm_y_errs, cutoff, n)
# errors_fin = errors[2]  # extract the summary dataframe
# errors_fin = errors_fin['stdevs']
#
# # add this new exciting data onto the original tree-ring dataframe
# df['harmonized_dataset_trended'] = harmonized_trend
# df['harmonized_dataset_errors'] = errors_fin
#
# """
# I think NOW I have to finally drop the NAN's because the math has trouble
# when there are missing values
# """
# df = df.dropna(subset = 'harmonized_dataset_trended')
# # re-extract the values from the cleaned dataframe to calculate offsets
# # between the harmonized dataset and the tree rings
# sample_xs = df['DecimalDate']
# sample_ys = df['∆14C']
# sample_y_err = df['∆14Cerr']
# harm_ys = df['harmonized_dataset_trended']
# harm_y_err = df['harmonized_dataset_errors']
#
# df['offset'] = sample_ys - harm_ys
# df['offset_err_prop'] = np.sqrt((sample_y_err**2) + (harm_y_err**2))
#
# plt.errorbar(sample_xs, df['offset'], label='Tree Rings offset from background', yerr=df['offset_err_prop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
# plt.title('Tree Ring Offsets From Background')
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure1.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Now I need to clean up the dataset, including removing bad ring counts, etc. But lets start with the bad ring counts.
# """
#
# baringhead = pd.read_excel(r'H:\The Science\Datasets'
#                            r'\BHD_14CO2_datasets_20211013.xlsx')
# xtot_bhd = baringhead['DEC_DECAY_CORR']
# ytot_bhd = baringhead['DELTA14C']
#
# """
# Figure 1. All the data together
# """
# size1 = 30
# fig = plt.figure(1)
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Southern Hemisphere Harmonized Dataset', color=colors2[5], s=size1, alpha=0.7)
# plt.scatter(sample_xs, sample_ys, marker='x', label='Tree Ring Records', color=colors2[2], s=size1, alpha = 0.7)
# plt.legend()
# plt.title('Harmonized Southern Hemisphere data versus Tree Ring record')
# # plt.xlim([1980, 2020])
# # plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure2.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
# """
# We can clearly see where bad ring counts exist - and the first thing I can do is remove wherever Jocelyn first flagged bad ring counts from the dataframe.
# """
# # testing the logic
# # df = df.drop(df[df['index'] < 50].index)  # works
# # drop all the data where Jocelyn noted that the ring counts are incorrect.
# df = df.drop(df[df['C14 comment'] == 'RING COUNT IS INCORRECT BASED ON 14C AMS measurement of this sample was performed at the Australian tiol University AMS facility.  All preparation (pretreatment, combustion, graphitisation, target packing) and data reduction was performed at the Rafter facility in our usual way.  The data quality meets our usual high standard, indicated by standard materials that agree with previous measurements of the same material made in our lab within one standard deviation.'].index)
# """
# The above line of code only removes three rows of data, so I'll add another filter based on how far off the offset is
# "if the tree ring data is X away from the harmonized record, we can be sure it's bad"
# """
# df['abs_offset'] = abs(df['offset'])
# # currently, if the offset is greater than 50, the data is removed.
# OFFSET_FILTER = 50
# df = df.drop(df[df['abs_offset'] > OFFSET_FILTER].index)  # works
# df = df.sort_values(by=['DecimalDate']).reset_index(drop=True)
# df['Lon'] = df['Lon'].fillna(174)  # all missing values are at Eastborne with this lon
# df['Lat'] = df['Lat'].fillna(-41)  # all missing values are at Eastborne with this latitude
#
# # re-write the file to an excel sheet
# # df.to_excel('tree_ring_analysis_py.xlsx')
# # so now I'm going to re-extract these variables before plotting...
# sample_xs = df['DecimalDate']
# sample_ys = df['∆14C']
# sample_y_err = df['∆14Cerr']
#
# size1 = 30
# fig = plt.figure(2)
# plt.scatter(xtot_bhd, ytot_bhd, label='Southern Hemisphere Harmonized Dataset', color=colors2[5], s = size1)
# plt.scatter(sample_xs, sample_ys, label='Tree Ring Records', color=colors2[2], s = size1, marker = 'x')
# plt.legend()
# plt.title('Harmonized Southern Hemisphere data versus Tree Ring record - Offsets > {} removed'.format(OFFSET_FILTER))
# # plt.xlim([1950, 1970])
# # plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure3.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#






