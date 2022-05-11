"""
Purpose:

Use the harmonized Southern Hemisphere dataset to see if we can find shifts in SOAR tree rings
to understand Southern ocean upwelling.

Outcome:

FILE STILL IN PROGRESS.

"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from dataset_harmonization import harmonized
from miller_curve_algorithm import ccgFilter
from heidelberg_intercomparison import monte_carlo_randomization_Trend
from heidelberg_intercomparison import monte_carlo_randomization_Smooth

"""
In the previous iteration of this file, I tried indexing and cleaning the 
tree ring file BEFORE doing the math. 
This led to many errors and NaN outputs due to problems with the actual indexing
rather than any errors or bad data. 

For example, all Chilean values need to be changed to NEGATIVE longitude, right now 
its in the same hemisphere as new zealand values. 
And there are a lot of missing data. 

In this iteration, I'm going to do all the math FIRST, and then index the data
after. 
"""
df = pd.read_excel(r'H:\The Science\Datasets'
                   r'\SOARTreeRingData2022-02-01.xlsx')
df = df.dropna(subset = '∆14C').reset_index()

harm_xs = harmonized['Decimal_date']  # see dataset_harmonization.py
harm_ys = harmonized['D14C']  # see dataset_harmonization.py
harm_y_errs = harmonized['weightedstderr_D14C']
sample_xs = (df['DecimalDate'])
sample_ys = (df['∆14C'])
sample_y_err = (df['∆14Cerr'])
# to appease the code, I have to adjust the format of the sample x's.
# the original monte carlo code had to extract a column ['x'] from a dataframe
# and its bugging because it doesn't see that here. So I'll just create one versus
# changing the function and risking ruining the other code.
sample_xs2 = pd.DataFrame({'x': sample_xs})
cutoff = 667

# Smooth the harmonized data using CCGCRV and have the output at the same time as tree ring x's
# input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
harmonized_trend = ccgFilter(harm_xs, harm_ys, cutoff).getTrendValue(sample_xs2)
# put the output into a dataframe
harmonized_trend = pd.DataFrame({'harmonized_data_trended': np.concatenate(harmonized_trend)})

# error estimate on the harmonized data trended using CCGCRV
n = 10  # TODO change back to 10,000
errors = monte_carlo_randomization_Trend(harm_xs, sample_xs2, harm_ys, harm_y_errs, cutoff, n)
errors_fin = errors[2]  # extract the summary dataframe
errors_fin = errors_fin['stdevs']

# add this new exciting data onto the original dataframe
df['harmonized_dataset_trended'] = harmonized_trend
df['harmonized_dataset_errors'] = errors_fin
print(np.shape(df))
""" 
I think NOW I have to finally drop the NAN's beacause the math has trouble
When there are missing values
"""
df = df.dropna(subset = 'harmonized_dataset_trended')
# re-extract the values from the cleaned dataframe to calculate offsets
# between the harmonized dataset and the tree rings
sample_xs = df['DecimalDate']
sample_ys = df['∆14C']
sample_y_err = df['∆14Cerr']
harm_ys = df['harmonized_dataset_trended']
harm_y_err = df['harmonized_dataset_errors']

df['offset'] = sample_ys - harm_ys
df['offset_err_prop'] = np.sqrt((sample_y_err**2) + (harm_y_err**2))
print(df)
plt.errorbar(sample_xs, df['offset'], label='Tree Rings offset from background', yerr=df['offset_err_prop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_offsets.png',
#             dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
"""
Coming back to this file on 11/5/22 after doing a lot of learning about AMS with albert, have to re-orient 
myself to the code. 
Up to this point in the code, I've smoothed the harmonized dataset using CCGCRV and got the output at the exact 
x-points that I have tree ring data. I've calculated the offsets between the tree ring data and the harmonized dataset, 
and I have the propagated errors for the CCGCRV smoothing process, and the offset calculation. 

Now I need to clean up the dataset, including removing bad ring counts, etc. But lets start with the bad ring counts. 

"""
baringhead = pd.read_excel(r'H:\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
xtot_bhd = baringhead['DEC_DECAY_CORR']
ytot_bhd = baringhead['DELTA14C']

colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5
"""
Figure 1. All the data together
"""
size1 = 30
fig = plt.figure(1)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Southern Hemisphere Harmonized Dataset', color=colors2[5], s=size1, alpha=0.7)
plt.scatter(sample_xs, sample_ys, marker='x', label='Tree Ring Records', color=colors2[2], s=size1, alpha = 0.7)
plt.legend()
plt.title('Harmonized Southern Hemisphere data versus Tree Ring record')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Bad_ring_counts.png',
            dpi=300, bbox_inches="tight")
plt.close()
"""
We can clearly see where bad ring counts exist - and the first thing I can do is remove wherever Jocelyn first flagged bad ring counts from the dataframe. 
"""
print(np.shape(df))
# testing the logic
# df = df.drop(df[df['index'] < 50].index)  # works
df = df.drop(df[df['C14 comment'] == 'RING COUNT IS INCORRECT BASED ON 14C AMS measurement of this sample was performed at the Australian tiol University AMS facility.  All preparation (pretreatment, combustion, graphitisation, target packing) and data reduction was performed at the Rafter facility in our usual way.  The data quality meets our usual high standard, indicated by standard materials that agree with previous measurements of the same material made in our lab within one standard deviation.'].index)
"""
The above line of code only removes three rows of data, so I'll add another filter based on how far off the offset is 
"if the tree ring data is X away from the harmonized record, we can be sure it's bad" 
"""

df['abs_offset'] = abs(df['offset'])
df = df.drop(df[df['abs_offset'] > 150].index)  # works
print(np.shape(df))
print(df)
df = df.sort_values(by=['DecimalDate'])
# df.to_excel('df.xlsx')
# so now I'm going to re-extract these variables before plotting...
sample_xs = df['DecimalDate']
sample_ys = df['∆14C']
sample_y_err = df['∆14Cerr']

size1 = 30
fig = plt.figure(2)
plt.plot(xtot_bhd, ytot_bhd, label='Southern Hemisphere Harmonized Dataset', color=colors2[5])
plt.plot(sample_xs, sample_ys, label='Tree Ring Records', color=colors2[2])
plt.legend()
plt.title('Harmonized Southern Hemisphere data versus Tree Ring record - Bad Ring Counts Removed')
# plt.xlim([1950, 1970])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Bad_ring_counts_removed_line.png',
            dpi=300, bbox_inches="tight")
plt.close()
"""
So now we can see that there are certain dates in which we have multiple values. These are also from different sites. 
This is kind of exactly what we want beacuse these different sites, perhaps different regions / latitudes, can tell us
about the differing SOce signal that we're interested in. 

How did Rachel approach this problem? 

First, I need to split up the data into different sites. I'll keep her original notation: 
"""
# # names = np.unique(df['StudySites::Site name'])
# # print(names)
CH_41_S = df.loc[(df['Site'] == 'Bahia San Pedro, Chile')]
CH_41_S_x = CH_41_S['DecimalDate']
CH_41_S_y = CH_41_S['∆14C']
CH_41_S_off = CH_41_S['offset']
CH_41_S_off_err = CH_41_S['offset_err_prop']

CH_44_S = df.loc[(df['Site'] == 'Raul Marin Balmaceda')]
CH_44_S_x = CH_44_S['DecimalDate']
CH_44_S_y = CH_44_S['∆14C']
CH_44_S_off = CH_44_S['offset']
CH_44_S_off_err = CH_44_S['offset_err_prop']

CH_48_S = df.loc[(df['Site'] == 'Tortel island')]
CH_48_S_x = CH_48_S['DecimalDate']
CH_48_S_y = CH_48_S['∆14C']
CH_48_S_off = CH_48_S['offset']
CH_48_S_off_err = CH_48_S['offset_err_prop']

CH_48_S_2 = df.loc[(df['Site'] == 'Tortel river')]
CH_48_S_2_x = CH_48_S_2['DecimalDate']
CH_48_S_2_y = CH_48_S_2['∆14C']
CH_48_S_2_off = CH_48_S_2['offset']
CH_48_S_2_off_err = CH_48_S_2['offset_err_prop']

CH_53_S = df.loc[(df['Site'] == 'Seno Skyring')]
CH_53_S_x = CH_53_S['DecimalDate']
CH_53_S_y = CH_53_S['∆14C']
CH_53_S_off = CH_53_S['offset']
CH_53_S_off_err = CH_53_S['offset_err_prop']

CH_54_S = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
CH_54_S_x = CH_54_S['DecimalDate']
CH_54_S_y = CH_54_S['∆14C']
CH_54_S_off = CH_54_S['offset']
CH_54_S_off_err = CH_54_S['offset_err_prop']

CH_55_S = df.loc[(df['Site'] == 'Baja Rosales, Isla Navarino')]
CH_55_S_x = CH_55_S['DecimalDate']
CH_55_S_y = CH_55_S['∆14C']
CH_55_S_off = CH_55_S['offset']
CH_55_S_off_err = CH_55_S['offset_err_prop']

CH_55_S_2 = df.loc[(df['Site'] == 'Puerto Navarino, Isla Navarino')]
CH_55_S_2_x = CH_55_S_2['DecimalDate']
CH_55_S_2_y = CH_55_S_2['∆14C']
CH_55_S_2_off = CH_55_S_2['offset']
CH_55_S_2_off_err = CH_55_S_2['offset_err_prop']

NZ_37_S = df.loc[(df['Site'] == 'Muriwai Beach Surf Club')]
NZ_37_S_x = NZ_37_S['DecimalDate']
NZ_37_S_y = NZ_37_S['∆14C']
NZ_37_S_off = NZ_37_S['offset']
NZ_37_S_off_err = NZ_37_S['offset_err_prop']

NZ_39_S = df.loc[(df['Site'] == 'near Kapuni school field, NZ')]
NZ_39_S_x =NZ_39_S['DecimalDate']
NZ_39_S_y =NZ_39_S['∆14C']
NZ_39_S_off =NZ_39_S['offset']
NZ_39_S_off_err =NZ_39_S['offset_err_prop']

NZ_41_S = df.loc[(df['Site'] == '19 Nikau St, Eastbourne, NZ')]
NZ_41_S_x =NZ_41_S['DecimalDate']
NZ_41_S_y =NZ_41_S['∆14C']
NZ_41_S_off =NZ_41_S['offset']
NZ_41_S_off_err =NZ_41_S['offset_err_prop']

NZ_41_S_2 = df.loc[(df['Site'] == 'Baring Head, NZ')]
NZ_41_S_2_x = NZ_41_S_2['DecimalDate']
NZ_41_S_2_y = NZ_41_S_2['∆14C']
NZ_41_S_2_off = NZ_41_S_2['offset']
NZ_41_S_2_off_err = NZ_41_S_2['offset_err_prop']

NZ_41_S_3 = df.loc[(df['Site'] == '23 Nikau St, Eastbourne, NZ')]
NZ_41_S_3_x = NZ_41_S_3['DecimalDate']
NZ_41_S_3_y = NZ_41_S_3['∆14C']
NZ_41_S_3_off = NZ_41_S_3['offset']
NZ_41_S_3_off_err = NZ_41_S_3['offset_err_prop']

NZ_44_S = df.loc[(df['Site'] == 'Haast Beach, paddock near beach')]
NZ_44_S_x = NZ_44_S['DecimalDate']
NZ_44_S_y = NZ_44_S['∆14C']
NZ_44_S_off = NZ_44_S['offset']
NZ_44_S_off_err = NZ_44_S['offset_err_prop']

NZ_46_S = df.loc[(df['Site'] == 'Oreti Beach')]
NZ_46_S_x = NZ_46_S['DecimalDate']
NZ_46_S_y = NZ_46_S['∆14C']
NZ_46_S_off = NZ_46_S['offset']
NZ_46_S_off_err = NZ_46_S['offset_err_prop']

NZ_47_S = df.loc[(df['Site'] == "Mason's Bay Homestead")]
NZ_47_S_x = NZ_47_S['DecimalDate']
NZ_47_S_y = NZ_47_S['∆14C']
NZ_47_S_off = NZ_47_S['offset']
NZ_47_S_off_err = NZ_47_S['offset_err_prop']

NZ_53_S = df.loc[(df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island")]
NZ_53_S_x = NZ_53_S['DecimalDate']
NZ_53_S_y = NZ_53_S['∆14C']
NZ_53_S_off = NZ_53_S['offset']
NZ_53_S_off_err = NZ_53_S['offset_err_prop']

size1 = 30
fig = plt.figure(2)
plt.scatter(sample_xs2, harmonized_trend, label='harmonized', color='black')
plt.plot(CH_41_S_x, CH_41_S_y, label='CH_41_S', color=colors[0])
plt.plot(CH_44_S_x, CH_44_S_y, label='CH_44_S', color=colors[1])
plt.plot(CH_48_S_x, CH_48_S_y, label='CH_48_S', color=colors[2])
plt.plot(CH_48_S_2_x, CH_48_S_2_y, label='CH_48_S', color=colors[3])
plt.plot(CH_53_S_x, CH_53_S_y, label='CH_53_S', color=colors[4])
plt.plot(CH_54_S_x, CH_54_S_y, label='CH_54_S', color=colors[5])
plt.plot(CH_55_S_x, CH_55_S_y, label='CH_55_S', color=colors[0])
plt.plot(CH_55_S_2_x, CH_55_S_2_y, label='CH_55_S', color=colors[1])

plt.plot(NZ_37_S_x, NZ_37_S_y, label='NZ_37_S', color=colors2[0])
plt.plot(NZ_39_S_x, NZ_39_S_y, label='NZ_39_S', color=colors2[1])
plt.plot(NZ_41_S_x, NZ_41_S_y, label='NZ_41_S', color=colors2[2])
plt.plot(NZ_41_S_2_x, NZ_41_S_2_y, label='NZ_41_S', color=colors2[3])
plt.plot(NZ_41_S_3_x, NZ_41_S_3_y, label='NZ_41_S', color=colors2[4])
plt.plot(NZ_44_S_x, NZ_44_S_y, label='NZ_44_S', color=colors2[5])
plt.plot(NZ_46_S_x, NZ_46_S_y, label='NZ_46_S', color=colors2[0])
plt.plot(NZ_47_S_x, NZ_47_S_y, label='NZ_47_S', color=colors2[1])
plt.plot(NZ_53_S_x, NZ_53_S_y, label='NZ_53_S', color=colors2[2])

plt.legend(loc='upper right')
plt.title('Plotting individual sites')
plt.xlim([1980, 2015])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Individual_Sites.png',
            dpi=300, bbox_inches="tight")
plt.close()
"""
So now we can see how close the tree rings from each site are to the background harmonized dataset. 
At the bomb peak, you can clearly see a discrepancy between the tree rings and the bomb peak. 
But what does it mean at this exact point? And how do I identify meaningful differences between the datasets before
and after the peak? 

I have pasted the comparison of Rachel's and mine up to this point in my notes. 

How do our offsets compare? 

"""

fig, axs = plt.subplots(2, 4, sharex=True, sharey=True, figsize=(20, 8))
axs[0, 0].plot(CH_41_S_x, CH_41_S_off, label='CH_41_S', color=colors[0])
axs[0, 0].set_title("41\xb0S (Bahia, San Pedro)")
axs[0, 0].axhline(y=0, color='black', linestyle='-')
# axs[0, 0].xlim([1980, 2015])

axs[0, 1].plot(CH_44_S_x, CH_44_S_off, label='CH_44_S',color=colors[1])
axs[0, 1].set_title("44\xb0S (Raul Marin Balcemeda)")
axs[0, 1].axhline(y=0, color='black', linestyle='-')

axs[0, 2].plot(CH_48_S_x, CH_48_S_off, label='CH_48_S',color=colors[2])
axs[0, 2].set_title("48\xb0S (Tortel Island)")
axs[0, 2].axhline(y=0, color='black', linestyle='-')

axs[0, 3].plot(CH_48_S_2_x, CH_48_S_2_off, label='CH_48_S_2',color=colors[3])
axs[0, 3].set_title("48\xb0S (Tortel River)")
axs[0, 3].axhline(y=0, color='black', linestyle='-')

axs[1, 0].plot(CH_53_S_x, CH_53_S_off, label='CH_53_S',color=colors[4])
axs[1, 0].set_title("53\xb0S (Seno Skyring)")
axs[1, 0].axhline(y=0, color='black', linestyle='-')
# axs[1, 0].ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis

axs[1, 1].plot(CH_54_S_x, CH_54_S_off, label='CH_54_S',color=colors[5])
axs[1, 1].set_title("54\xb0S (Monte Tarn, Punta Arenas)")
axs[1, 1].axhline(y=0, color='black', linestyle='-')

axs[1, 2].plot(CH_55_S_x, CH_55_S_off, label='CH_55_S',color=colors[0])
axs[1, 2].set_title("55\xb0S (Baja Rosales, Isla Navarino)")
axs[1, 2].axhline(y=0, color='black', linestyle='-')

axs[1, 3].plot(CH_55_S_2_x, CH_55_S_2_off, label='CH_55_S_2' ,color=colors[1])
axs[1, 3].set_title("55\xb0S (Puerto Navarino, Isla Navarino)")
axs[1, 3].axhline(y=0, color='black', linestyle='-')

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Chile_offsets.png',
            dpi=300, bbox_inches="tight")
plt.close()


fig, axs = plt.subplots(2, 5, sharex=True, sharey=True, figsize=(20, 8))
axs[0, 0].plot(NZ_37_S_x, NZ_37_S_off, label='NZ_39_S', color=colors[0])
axs[0, 0].set_title("37\xb0S (Muriwai Beach)")
axs[0, 0].axhline(y=0, color='black', linestyle='-')
# axs[0, 0].xlim([1980, 2015])

axs[0, 1].plot(NZ_39_S_x, NZ_39_S_off, label='NZ_39_S',color=colors[1])
axs[0, 1].set_title("39\xb0S (Kapuni Beach)")
axs[0, 1].axhline(y=0, color='black', linestyle='-')

axs[0, 3].plot(NZ_41_S_x, NZ_41_S_off, label='NZ_41_S',color=colors[2])
axs[0, 3].set_title("41\xb0S (Eastbourne)")
axs[0, 3].axhline(y=0, color='black', linestyle='-')

axs[0, 2].plot(NZ_41_S_2_x, NZ_41_S_2_off, label='NZ_41_S_2',color=colors[3])
axs[0, 2].set_title("41\xb0S (Baring Head)")
axs[0, 2].axhline(y=0, color='black', linestyle='-')

axs[0, 4].plot(NZ_41_S_3_x, NZ_41_S_3_off, label='NZ_41_S_3',color=colors[4])
axs[0, 4].set_title("41\xb0S (Eastbourne)")
axs[0, 4].axhline(y=0, color='black', linestyle='-')
# axs[1, 0].ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis

axs[1, 1].plot(NZ_44_S_x, NZ_44_S_off, label='NZ_44_S',color=colors[5])
axs[1, 1].set_title("44\xb0S (Haast Beach)")
axs[1, 1].axhline(y=0, color='black', linestyle='-')

axs[1, 2].plot(NZ_46_S_x, NZ_46_S_off, label='NZ_46_S',color=colors[0])
axs[1, 2].set_title("46\xb0S (Oreti Beach)")
axs[1, 2].axhline(y=0, color='black', linestyle='-')

axs[1, 3].plot(NZ_47_S_x, NZ_47_S_off, label='NZ_47_S' ,color=colors[1])
axs[1, 3].set_title("47\xb0S (Mason's Bay)")
axs[1, 3].axhline(y=0, color='black', linestyle='-')

axs[1, 4].plot(NZ_53_S_x, NZ_53_S_off, label='NZ_53_S' ,color=colors[1])
axs[1, 4].set_title("53\xb0S (World's Lonliest Tree)")
axs[1, 4].axhline(y=0, color='black', linestyle='-')

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/NZ_offsets.png',
            dpi=300, bbox_inches="tight")
plt.close()












#
# size1 = 30
# fig = plt.figure(3)
# # plt.scatter(sample_xs2, harmonized_trend, label='harmonized', color='black')
# plt.plot(CH_41_S_x, CH_41_S_off, label='CH_41_S', color=colors[0])
# plt.plot(CH_44_S_x, CH_44_S_off, label='CH_44_S',color=colors[1])
# plt.plot(CH_48_S_x, CH_48_S_off, label='CH_48_S',color=colors[2])
# plt.plot(CH_48_S_2_x, CH_48_S_2_off, label='CH_48_S_2',color=colors[3])
# # plt.plot(CH_53_S_x, CH_53_S_off, label='CH_53_S',color=colors[4])
# # plt.plot(CH_54_S_x, CH_54_S_off, label='CH_54_S',color=colors[5])
# # plt.plot(CH_55_S_x, CH_55_S_off, label='CH_55_S',color=colors[0])
# # plt.plot(CH_55_S_2_x, CH_55_S_2_off, label='CH_55_S_2' ,color=colors[1])
# plt.legend()
# plt.title('Pacific Sector Offsets')
# plt.xlim([1980, 2015])
# plt.ylim([-15, 10])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Pacific_Sector_offsets_lines.png',
# #             dpi=300, bbox_inches="tight")
# # plt.close()
# plt.show()

# size1 = 30
# fig = plt.figure(3)
# # plt.scatter(sample_xs2, harmonized_trend, label='harmonized', color='black')
# plt.errorbar(CH_41_S_x, CH_41_S_off, label='CH_41_S', yerr= CH_41_S_off_err, fmt='o', color=colors[0], ecolor='black', elinewidth=1, capsize=2)
# plt.errorbar(CH_44_S_x, CH_44_S_off, label='CH_44_S', yerr= CH_44_S_off_err, fmt='o', color=colors[1], ecolor='black', elinewidth=1, capsize=2)
# # plt.errorbar(CH_48_S_x, CH_48_S_off, label='CH_48_S', yerr= CH_48_S_off_err, fmt='o', color=colors[2], ecolor='black', elinewidth=1, capsize=2)
# # plt.errorbar(CH_48_S_2_x, CH_48_S_2_off, label='CH_48_S_2', yerr= CH_48_S_2_off_err, fmt='o', color=colors[3], ecolor='black', elinewidth=1, capsize=2)
# # plt.errorbar(CH_53_S_x, CH_53_S_off, label='CH_53_S', yerr= CH_53_S_off_err, fmt='o', color=colors[4], ecolor='black', elinewidth=1, capsize=2)
# # plt.errorbar(CH_54_S_x, CH_54_S_off, label='CH_54_S', yerr= CH_54_S_off_err, fmt='o', color=colors[5], ecolor='black', elinewidth=1, capsize=2)
# # plt.errorbar(CH_55_S_x, CH_55_S_off, label='CH_55_S', yerr= CH_55_S_off_err, fmt='o', color=colors[0], ecolor='black', elinewidth=1, capsize=2)
# # plt.errorbar(CH_55_S_2_x, CH_55_S_2_off, label='CH_55_S_2', yerr= CH_55_S_2_off_err, fmt='o', color=colors[1], ecolor='black', elinewidth=1, capsize=2)
# plt.legend()
# plt.title('Pacific Sector Offsets')
# plt.xlim([1980, 2015])
# plt.ylim([-15, 10])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Pacific_Sector_offsets_1980.png',
# #             dpi=300, bbox_inches="tight")
# plt.close()

































""" Later, when I need to adjust the Chilean values to negative lon, here is the code"""
# df['Lon'] = df['Lon'].fillna(-999)  # fill all missing values with -999
# df['Lat'] = df['Lat'].fillna(-999)  # fill all missing values with -999
# df.drop(df[df['C14Flag'] == -999].index, inplace=True)
#
# # baringhead = baringhead.iloc[::5, :]  # if I want to downsample the data
# xtot_bhd = baringhead['DEC_DECAY_CORR']             # entire dataset x-values
# ytot_bhd = baringhead['DELTA14C']                   # entire dataset y-values
#
# """ First order of tidying, adjust the Western Hemisphere longitude values (should be negative) """
# # From POKEMON.PY file
# # df.loc[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Poison')] # filtering based on two types of data OR
# nz = df.loc[(df['Lon'] > 100) | (df['Lon'] == -999)].reset_index()  # split up the data
# chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)].reset_index()  # split up the data
# chile['new_lon'] = np.multiply(chile['Lon'], -1)  # address the bad longitude
# nz['new_lon'] = nz['Lon']  # need this new column to be the same for concatenation
#
# frames = [chile, nz]  # TODO: figure out: why I need to put these two DataFrames into an array before concat
# df = pd.concat(frames)  # put the data back together
# # df.to_excel('adjusted_SOAR2.xlsx')

""" And later, when i want to index by location, see this block of code: """
# # names = np.unique(df['StudySites::Site name'])
# # print(names)
# eastbourne1 = df.loc[(df['Site'] == '19 Nikau St, Eastbourne, NZ')]
# eastbourne2 = df.loc[(df['Site'] == '23 Nikau St, Eastbourne, NZ')]
# san_pedro = df.loc[(df['Site'] == 'Bahia San Pedro, Chile')]
# navarino1 = df.loc[(df['Site'] == 'Baja Rosales, Isla Navarino')]
# bhd = df.loc[(df['Site'] == 'Baring Head, NZ')]
# haast_paddock = df.loc[(df['Site'] == 'Haast Beach, paddock near beach')]
# mason_bay = df.loc[(df['Site'] == "Mason's Bay Homestead")]
# monte_tarn = df.loc[(df['Site'] == 'Monte Tarn, Punta Arenas')]
# muriwai_beach = df.loc[(df['Site'] == 'Muriwai Beach Surf Club')]
# oreti_beach = df.loc[(df['Site'] == 'Oreti Beach')]
# navarino2 = df.loc[(df['Site'] == 'Puerto Navarino, Isla Navarino')]
# balmaceda = df.loc[(df['Site'] == 'Raul Marin Balmaceda')]
# seno = df.loc[(df['Site'] == 'Seno Skyring')]
# tortel_island = df.loc[(df['Site'] == 'Tortel island')]
# tortel_river = df.loc[(df['Site'] == 'Tortel river')]
# lonely_tree = df.loc[(df['Site'] == "World's Loneliest Tree, Camp Cove, Campbell island")]
# kapuni_field = df.loc[(df['Site'] == 'near Kapuni school field, NZ')]
#