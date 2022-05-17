"""
Purpose:

Use the harmonized Southern Hemisphere dataset to see if we can find shifts in SOAR tree rings
to understand Southern ocean upwelling.

Outcome:

Cleans up the data and outputs a new dataframe into excel sheet used for Tree_ring_analysis2.
Creates a nice plot that gives an overview of the data-offsets relative to the harmonized dataset.
Propagated errors are currently run at 10 iterations of Monte Carlo.
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
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

df = pd.read_excel(r'H:\The Science\Datasets'
                   r'\SOARTreeRingData2022-02-01.xlsx')
df = df.dropna(subset = '∆14C').reset_index()

# importing harmonized southern hemisphere dataset from the previous python file.
harm_xs = harmonized['Decimal_date']  # see dataset_harmonization.py
harm_ys = harmonized['D14C']  # see dataset_harmonization.py
harm_y_errs = harmonized['weightedstderr_D14C']

# importing the tree-ring x-values from the file I've read in.
sample_xs = (df['DecimalDate'])
# I want the harmonized dataset to be smoothed using CCGCRV, and
# I want it to OUTPUT the values at the specific x values that I have for tree-ring data.
# the following lines of code slightly change the data format of the x-data to appease the Monte Carlo code.
sample_xs2 = pd.DataFrame({'x': sample_xs})

# Smooth the harmonized data using CCGCRV and have the output at the same time as tree ring x's
# input is: 1) x data, 2) y data that you want smoothed, then, 3) x-values at which you want y's output
cutoff = 667
harmonized_trend = ccgFilter(harm_xs, harm_ys, cutoff).getTrendValue(sample_xs2)
harmonized_trend = pd.DataFrame({'harmonized_data_trended': np.concatenate(harmonized_trend)})  # put the output into a dataframe

# error estimate on the harmonized data trended using CCGCRV
n = 10  # TODO change back to 10,000
errors = monte_carlo_randomization_Trend(harm_xs, sample_xs2, harm_ys, harm_y_errs, cutoff, n)
errors_fin = errors[2]  # extract the summary dataframe
errors_fin = errors_fin['stdevs']

# add this new exciting data onto the original tree-ring dataframe
df['harmonized_dataset_trended'] = harmonized_trend
df['harmonized_dataset_errors'] = errors_fin

""" 
I think NOW I have to finally drop the NAN's because the math has trouble
when there are missing values
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

plt.errorbar(sample_xs, df['offset'], label='Tree Rings offset from background', yerr=df['offset_err_prop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.title('Tree Ring Offsets From Background')
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure1.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Now I need to clean up the dataset, including removing bad ring counts, etc. But lets start with the bad ring counts. 
"""

baringhead = pd.read_excel(r'H:\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
xtot_bhd = baringhead['DEC_DECAY_CORR']
ytot_bhd = baringhead['DELTA14C']

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
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure2.png',
            dpi=300, bbox_inches="tight")
plt.close()
"""
We can clearly see where bad ring counts exist - and the first thing I can do is remove wherever Jocelyn first flagged bad ring counts from the dataframe. 
"""
# testing the logic
# df = df.drop(df[df['index'] < 50].index)  # works
# drop all the data where Jocelyn noted that the ring counts are incorrect.
df = df.drop(df[df['C14 comment'] == 'RING COUNT IS INCORRECT BASED ON 14C AMS measurement of this sample was performed at the Australian tiol University AMS facility.  All preparation (pretreatment, combustion, graphitisation, target packing) and data reduction was performed at the Rafter facility in our usual way.  The data quality meets our usual high standard, indicated by standard materials that agree with previous measurements of the same material made in our lab within one standard deviation.'].index)
"""
The above line of code only removes three rows of data, so I'll add another filter based on how far off the offset is 
"if the tree ring data is X away from the harmonized record, we can be sure it's bad" 
"""
df['abs_offset'] = abs(df['offset'])
# currently, if the offset is greater than 50, the data is removed.
OFFSET_FILTER = 50
df = df.drop(df[df['abs_offset'] > OFFSET_FILTER].index)  # works
df = df.sort_values(by=['DecimalDate']).reset_index()
df['Lon'] = df['Lon'].fillna(174)  # all missing values are at Eastborne with this lon
df['Lat'] = df['Lat'].fillna(-41)  # all missing values are at Eastborne with this latitude

# re-write the file to an excel sheet
df.to_excel('tree_ring_analysis_py.xlsx')
# so now I'm going to re-extract these variables before plotting...
sample_xs = df['DecimalDate']
sample_ys = df['∆14C']
sample_y_err = df['∆14Cerr']

size1 = 30
fig = plt.figure(2)
plt.scatter(xtot_bhd, ytot_bhd, label='Southern Hemisphere Harmonized Dataset', color=colors2[5], s = size1)
plt.scatter(sample_xs, sample_ys, label='Tree Ring Records', color=colors2[2], s = size1, marker = 'x')
plt.legend()
plt.title('Harmonized Southern Hemisphere data versus Tree Ring record - Offsets > {} removed'.format(OFFSET_FILTER))
# plt.xlim([1950, 1970])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure3.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
INDEX ACCORDING TO INDIVIDUAL SITES AND TAKE A LOOK AT THAT:
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
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
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure4.png',
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
plt.errorbar(sample_xs, df['offset'], label='Tree Rings offset from background', yerr=df['offset_err_prop'], fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)

fig, axs = plt.subplots(2, 4, sharex=True, sharey=True, figsize=(20, 8))
axs[0, 0].errorbar(CH_41_S_x, CH_41_S_off, label='CH_41_S', yerr=CH_41_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 0].set_title("41\xb0S (Bahia, San Pedro)")
axs[0, 0].axhline(y=0, color='black', linestyle='-')
axs[0, 0].set_ylim(-20, 20)

axs[0, 1].errorbar(CH_44_S_x, CH_44_S_off, label='CH_41_S', yerr=CH_44_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 1].set_title("44\xb0S (Raul Marin Balcemeda)")
axs[0, 1].axhline(y=0, color='black', linestyle='-')
axs[0, 1].set_ylim(-20, 20)

axs[0, 2].errorbar(CH_48_S_x, CH_48_S_off, label='CH_41_S', yerr=CH_48_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 2].set_title("48\xb0S (Tortel Island)")
axs[0, 2].axhline(y=0, color='black', linestyle='-')
axs[0, 2].set_ylim(-20, 20)

axs[0, 3].errorbar(CH_48_S_2_x, CH_48_S_2_off, label='CH_41_S', yerr=CH_48_S_2_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 3].set_title("48\xb0S (Tortel River)")
axs[0, 3].axhline(y=0, color='black', linestyle='-')
axs[0, 3].set_ylim(-20, 20)

axs[1, 0].errorbar(CH_53_S_x, CH_53_S_off, label='CH_41_S', yerr=CH_53_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 0].set_title("53\xb0S (Seno Skyring)")
axs[1, 0].axhline(y=0, color='black', linestyle='-')
axs[1, 0].set_ylim(-20, 20)

axs[1, 1].errorbar(CH_54_S_x, CH_54_S_off, label='CH_41_S', yerr=CH_54_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 1].set_title("54\xb0S (Monte Tarn, Punta Arenas)")
axs[1, 1].axhline(y=0, color='black', linestyle='-')
axs[1, 0].set_ylim(-20, 20)

axs[1, 2].errorbar(CH_55_S_x, CH_55_S_off, label='CH_41_S', yerr=CH_55_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 2].set_title("55\xb0S (Baja Rosales, Isla Navarino)")
axs[1, 2].axhline(y=0, color='black', linestyle='-')
axs[1, 2].set_ylim(-20, 20)

axs[1, 3].errorbar(CH_55_S_2_x, CH_55_S_2_off, label='CH_41_S', yerr=CH_55_S_2_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 3].set_title("55\xb0S (Puerto Navarino, Isla Navarino)")
axs[1, 3].axhline(y=0, color='black', linestyle='-')
axs[1, 3].set_ylim(-20, 20)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure5.png',
            dpi=300, bbox_inches="tight")
plt.close()


fig, axs = plt.subplots(2, 5, sharex=True, sharey=True, figsize=(20, 8))
axs[0, 0].errorbar(NZ_37_S_x, NZ_37_S_off, label='CH_41_S', yerr=NZ_37_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 0].set_title("37\xb0S (Muriwai Beach)")
axs[0, 0].axhline(y=0, color='black', linestyle='-')
axs[0, 0].set_ylim(-20, 20)

axs[0, 1].errorbar(NZ_39_S_x, NZ_39_S_off, label='CH_41_S', yerr=NZ_39_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 1].set_title("39\xb0S (Kapuni Beach)")
axs[0, 1].axhline(y=0, color='black', linestyle='-')
axs[0, 1].set_ylim(-20, 20)

axs[0, 3].errorbar(NZ_41_S_x, NZ_41_S_off, label='CH_41_S', yerr=NZ_41_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 3].set_title("41\xb0S (Eastbourne)")
axs[0, 3].axhline(y=0, color='black', linestyle='-')
axs[0, 3].set_ylim(-20, 20)

axs[0, 2].errorbar(NZ_41_S_2_x, NZ_41_S_2_off, label='CH_41_S', yerr=NZ_41_S_2_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 2].set_title("41\xb0S (Baring Head)")
axs[0, 2].axhline(y=0, color='black', linestyle='-')
axs[0, 2].set_ylim(-20, 20)

axs[0, 4].errorbar(NZ_41_S_3_x, NZ_41_S_3_off, label='CH_41_S', yerr=NZ_41_S_3_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[0, 4].set_title("41\xb0S (Eastbourne)")
axs[0, 4].axhline(y=0, color='black', linestyle='-')
axs[0, 4].set_ylim(-20, 20)
# axs[1, 0].ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis

axs[1, 1].errorbar(NZ_44_S_x, NZ_44_S_off, label='CH_41_S', yerr=NZ_44_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 1].set_title("44\xb0S (Haast Beach)")
axs[1, 1].axhline(y=0, color='black', linestyle='-')
axs[1, 1].set_ylim(-20, 20)

axs[1, 2].errorbar(NZ_46_S_x, NZ_46_S_off, label='CH_41_S', yerr=NZ_46_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 2].set_title("46\xb0S (Oreti Beach)")
axs[1, 2].axhline(y=0, color='black', linestyle='-')
axs[1, 0].set_ylim(-20, 20)

axs[1, 3].errorbar(NZ_47_S_x, NZ_47_S_off, label='CH_41_S', yerr=NZ_47_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 3].set_title("47\xb0S (Mason's Bay)")
axs[1, 3].axhline(y=0, color='black', linestyle='-')
axs[1, 3].set_ylim(-20, 20)

axs[1, 4].errorbar(NZ_53_S_x, NZ_53_S_off, label='CH_41_S', yerr=NZ_53_S_off_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.5)
axs[1, 4].set_title("53\xb0S (World's Lonliest Tree)")
axs[1, 4].axhline(y=0, color='black', linestyle='-')
axs[1, 4].set_ylim(-20, 20)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure6.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
We can also index according to LATITUDE ONLY and see how the plots look
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
"""
# break up the data into two DataFrames based on their location, and remove all data before 1980.
df = df.loc[(df['DecimalDate'] >= 1980)]  # TODO after analysis is finished, come back to time before 1980
nz = df.loc[(df['Lon'] > 100)]
chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)]
# Chile data still needs LONS to be changed to negative, but OK for now

# index the NZ Data based on Latitude
# I'm changing this from a previous version to bound the data at latitudes based on our data availability, rather
# than arbitrarily at 5 degree increments.
# nz_40 = nz.loc[(nz['Lat'] >= -40)]  # check it's working: print(np.unique(nz_40.Site))
nz_40_45 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36)]
nz_45_50 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43)]
nz_50_55 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50)]  # > -998 keeps this portion from grabbing the Eastborne data.
# check it works -> print(np.unique(nz_50_55.Site))

# index the Chile Data based on latitude
ch_40_45 = chile.loc[(chile['Lat'] > -45) & (chile['Lat'] <= -40)]
ch_45_50 = chile.loc[(chile['Lat'] > -50) & (chile['Lat'] <= -45)]
ch_50_56 = chile.loc[(chile['Lat'] > -56) & (chile['Lat'] <= -50)]
# print(np.unique(ch_50_56.Site))

"""
LINEAR REGRESSION OF NZ DATA
"""
# A_40 = np.vstack([nz_40['DecimalDate'], np.ones(len(nz_40['DecimalDate']))]).T
# m_40, c_40 = np.linalg.lstsq(A_40, nz_40['offset'], rcond=None)[0]

A_40_45 = np.vstack([nz_40_45['DecimalDate'], np.ones(len(nz_40_45['DecimalDate']))]).T
m_40_45, c_40_45 = np.linalg.lstsq(A_40_45, nz_40_45['offset'], rcond=None)[0]

A_45_50 = np.vstack([nz_45_50['DecimalDate'], np.ones(len(nz_45_50['DecimalDate']))]).T
m_45_50, c_45_50 = np.linalg.lstsq(A_45_50, nz_45_50['offset'], rcond=None)[0]

A_50_55 = np.vstack([nz_50_55['DecimalDate'], np.ones(len(nz_50_55['DecimalDate']))]).T
m_50_55, c_50_55 = np.linalg.lstsq(A_50_55, nz_50_55['offset'], rcond=None)[0]


size1 = 30
fig = plt.figure(7)
# plt.scatter(nz_40['DecimalDate'], nz_40['offset'], marker='o', label='Southern Hemisphere Harmonized Dataset',
#             color=colors2[5], s=size1, alpha=0.7)
# plt.plot(nz_40['DecimalDate'], m_40 * nz_40['DecimalDate'] + c_40, label='40S', color=colors2[1], linestyle = "dotted")
plt.plot(nz_40_45['DecimalDate'], m_40_45 * nz_40_45['DecimalDate'] + c_40_45, label='36-42S', color=colors2[2], linestyle = "dashdot")
plt.plot(nz_45_50['DecimalDate'], m_45_50 * nz_45_50['DecimalDate'] + c_45_50, label='43-48S', color=colors2[3], linestyle = "dashed")
plt.plot(nz_50_55['DecimalDate'], m_50_55 * nz_50_55['DecimalDate'] + c_50_55, label='53S', color=colors2[4])
plt.title('New Zealand Tree Ring Offsets Linearly Regressed')
plt.legend()
# plt.xlim([1980, 2020])
plt.ylim([-15, 10])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure7.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
LINEAR REGRESSION OF CHILE DATA
"""
B_40_45 = np.vstack([ch_40_45['DecimalDate'], np.ones(len(ch_40_45['DecimalDate']))]).T
n_40_45, d_40_45 = np.linalg.lstsq(B_40_45, ch_40_45['offset'], rcond=None)[0]

B_45_50 = np.vstack([ch_45_50['DecimalDate'], np.ones(len(ch_45_50['DecimalDate']))]).T
n_45_50, d_45_50 = np.linalg.lstsq(B_45_50, ch_45_50['offset'], rcond=None)[0]

B_50_56 = np.vstack([ch_50_56['DecimalDate'], np.ones(len(ch_50_56['DecimalDate']))]).T
n_50_56, d_50_56 = np.linalg.lstsq(B_50_56, ch_50_56['offset'], rcond=None)[0]

size1 = 30
fig = plt.figure(2)
# plt.scatter(nz_40['DecimalDate'], nz_40['offset'], marker='o', label='Southern Hemisphere Harmonized Dataset',
#             color=colors2[5], s=size1, alpha=0.7)plt.
plt.plot(ch_40_45['DecimalDate'], n_40_45 * ch_40_45['DecimalDate'] + d_40_45, label='40-45S', color=colors2[2], linestyle = "dashdot")
plt.plot(ch_45_50['DecimalDate'], n_45_50 * ch_45_50['DecimalDate'] + d_45_50, label='45-50S', color=colors2[3], linestyle = "dashed")
plt.plot(ch_50_56['DecimalDate'], n_50_56 * ch_50_56['DecimalDate'] + d_50_56, label='50-56S', color=colors2[4])
plt.title('Chilean Tree Ring Offsets Linearly Regressed')
plt.legend()
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure8.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
AND THEN YOU CAN INDEX BASED ON LATITUDE AND TIME. 
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
"""

# indexing the data according to the matrix in my DataScience Notebook:
# I'm changing this from a previous version to bound the data at latitudes based on our data availability, rather
# than arbitrarily at 5 degree increments.
# nz_a1 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]  # North of 40S, 1980 - 1990
# nz_a2 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]  # North of 40S, 1990 - 2000
# nz_a3 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]  # etc...
# nz_a4 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

nz_b1 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]
nz_b2 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
nz_b3 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
nz_b4 = nz.loc[(nz['Lat'] >= -42) & (nz['Lat'] < -36) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

nz_c1 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]
nz_c2 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
nz_c3 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
nz_c4 = nz.loc[(nz['Lat'] >= -48) & (nz['Lat'] < -43) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

nz_d1 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]  # > -998 keeps this portion from grabbing the Eastborne data set at -999.
nz_d2 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
nz_d3 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
nz_d4 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

"""
Perform the linear regression for each time period and latitude range: 

https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
"""
# A_nz_a1 = np.vstack([nz_a1['DecimalDate'], np.ones(len(nz_a1['DecimalDate']))]).T
# A_nz_a2 = np.vstack([nz_a2['DecimalDate'], np.ones(len(nz_a2['DecimalDate']))]).T
# A_nz_a3 = np.vstack([nz_a3['DecimalDate'], np.ones(len(nz_a3['DecimalDate']))]).T
# A_nz_a4 = np.vstack([nz_a4['DecimalDate'], np.ones(len(nz_a4['DecimalDate']))]).T

A_nz_b1 = np.vstack([nz_b1['DecimalDate'], np.ones(len(nz_b1['DecimalDate']))]).T
A_nz_b2 = np.vstack([nz_b2['DecimalDate'], np.ones(len(nz_b2['DecimalDate']))]).T
A_nz_b3 = np.vstack([nz_b3['DecimalDate'], np.ones(len(nz_b3['DecimalDate']))]).T
A_nz_b4 = np.vstack([nz_b4['DecimalDate'], np.ones(len(nz_b4['DecimalDate']))]).T

A_nz_c1 = np.vstack([nz_c1['DecimalDate'], np.ones(len(nz_c1['DecimalDate']))]).T
A_nz_c2 = np.vstack([nz_c2['DecimalDate'], np.ones(len(nz_c2['DecimalDate']))]).T
A_nz_c3 = np.vstack([nz_c3['DecimalDate'], np.ones(len(nz_c3['DecimalDate']))]).T
A_nz_c4 = np.vstack([nz_c4['DecimalDate'], np.ones(len(nz_c4['DecimalDate']))]).T

A_nz_d1 = np.vstack([nz_d1['DecimalDate'], np.ones(len(nz_d1['DecimalDate']))]).T
A_nz_d2 = np.vstack([nz_d2['DecimalDate'], np.ones(len(nz_d2['DecimalDate']))]).T
A_nz_d3 = np.vstack([nz_d3['DecimalDate'], np.ones(len(nz_d3['DecimalDate']))]).T
A_nz_d4 = np.vstack([nz_d4['DecimalDate'], np.ones(len(nz_d4['DecimalDate']))]).T

# m_a1, c_a1 = np.linalg.lstsq(A_nz_a1, nz_a1['offset'], rcond=None)[0]
# m_a2, c_a2 = np.linalg.lstsq(A_nz_a2, nz_a2['offset'], rcond=None)[0]
# m_a3, c_a3 = np.linalg.lstsq(A_nz_a3, nz_a3['offset'], rcond=None)[0]
# m_a4, c_a4 = np.linalg.lstsq(A_nz_a4, nz_a4['offset'], rcond=None)[0]

m_b1, c_b1 = np.linalg.lstsq(A_nz_b1, nz_b1['offset'], rcond=None)[0]
m_b2, c_b2 = np.linalg.lstsq(A_nz_b2, nz_b2['offset'], rcond=None)[0]
m_b3, c_b3 = np.linalg.lstsq(A_nz_b3, nz_b3['offset'], rcond=None)[0]
m_b4, c_b4 = np.linalg.lstsq(A_nz_b4, nz_b4['offset'], rcond=None)[0]

m_c1, c_c1 = np.linalg.lstsq(A_nz_c1, nz_c1['offset'], rcond=None)[0]
m_c2, c_c2 = np.linalg.lstsq(A_nz_c2, nz_c2['offset'], rcond=None)[0]
m_c3, c_c3 = np.linalg.lstsq(A_nz_c3, nz_c3['offset'], rcond=None)[0]
m_c4, c_c4 = np.linalg.lstsq(A_nz_c4, nz_c4['offset'], rcond=None)[0]

m_d1, c_d1 = np.linalg.lstsq(A_nz_d1, nz_d1['offset'], rcond=None)[0]
m_d2, c_d2 = np.linalg.lstsq(A_nz_d2, nz_d2['offset'], rcond=None)[0]
m_d3, c_d3 = np.linalg.lstsq(A_nz_d3, nz_d3['offset'], rcond=None)[0]
m_d4, c_d4 = np.linalg.lstsq(A_nz_d4, nz_d4['offset'], rcond=None)[0]


"""
Testing the Figure
"""
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
a = 0.15
size1 = 15
fig = plt.figure(2)
# plt.plot(nz_a1['DecimalDate'], m_a1*nz_a1['DecimalDate'] + c_a1, label='North of 40S', color='black', linestyle = "dashdot")
# plt.plot(nz_a2['DecimalDate'], m_a2*nz_a2['DecimalDate'] + c_a2, color='black', linestyle = "dashdot")
# plt.plot(nz_a3['DecimalDate'], m_a3*nz_a3['DecimalDate'] + c_a3, color='black', linestyle = "dashdot")
# plt.plot(nz_a4['DecimalDate'], m_a4*nz_a4['DecimalDate'] + c_a4, color='black', linestyle = "dashdot")
#
# plt.scatter(nz_a1['DecimalDate'], nz_a1['offset'], alpha = a, color='black', s = size1)
# plt.scatter(nz_a2['DecimalDate'], nz_a2['offset'], alpha = a, color='black', s = size1)
# plt.scatter(nz_a3['DecimalDate'], nz_a3['offset'], alpha = a, color='black', s = size1)
# plt.scatter(nz_a4['DecimalDate'], nz_a4['offset'], alpha = a, color='black', s = size1)

# TODO fix the B part of the matrix - doesn't seem to be indexing properly.
plt.plot(nz_b1['DecimalDate'], m_b1*nz_b1['DecimalDate'] + c_b1, label='36-42S', color=colors2[2], linestyle = "dashdot")
plt.plot(nz_b2['DecimalDate'], m_b2*nz_b2['DecimalDate'] + c_b2, color=colors2[2], linestyle = "dashdot")
plt.plot(nz_b3['DecimalDate'], m_b3*nz_b3['DecimalDate'] + c_b3, color=colors2[2], linestyle = "dashdot")
plt.plot(nz_b4['DecimalDate'], m_b4*nz_b4['DecimalDate'] + c_b4, color=colors2[2], linestyle = "dashdot")

plt.scatter(nz_b1['DecimalDate'], nz_b1['offset'], alpha = a, color=colors2[2], s = size1)
plt.scatter(nz_b2['DecimalDate'], nz_b2['offset'], alpha = a, color=colors2[2], s = size1)
plt.scatter(nz_b3['DecimalDate'], nz_b3['offset'], alpha = a, color=colors2[2], s = size1)
plt.scatter(nz_b4['DecimalDate'], nz_b4['offset'], alpha = a, color=colors2[2], s = size1)


plt.plot(nz_c1['DecimalDate'], m_c1*nz_c1['DecimalDate'] + c_c1, label='43-48S', color=colors2[3], linestyle = "dashed")
plt.plot(nz_c2['DecimalDate'], m_c2*nz_c2['DecimalDate'] + c_c2, color=colors2[3], linestyle = "dashed")
plt.plot(nz_c3['DecimalDate'], m_c3*nz_c3['DecimalDate'] + c_c3, color=colors2[3], linestyle = "dashed")
plt.plot(nz_c4['DecimalDate'], m_c4*nz_c4['DecimalDate'] + c_c4,  color=colors2[3], linestyle = "dashed")

plt.scatter(nz_c1['DecimalDate'], nz_c1['offset'], alpha = a, color=colors2[3], s = size1)
plt.scatter(nz_c2['DecimalDate'], nz_c2['offset'], alpha = a, color=colors2[3], s = size1)
plt.scatter(nz_c3['DecimalDate'], nz_c3['offset'], alpha = a, color=colors2[3], s = size1)
plt.scatter(nz_c4['DecimalDate'], nz_c4['offset'], alpha = a, color=colors2[3], s = size1)

plt.plot(nz_d1['DecimalDate'], m_d1*nz_d1['DecimalDate'] + c_d1, label='53S', color=colors2[4], linestyle = "solid")
plt.plot(nz_d2['DecimalDate'], m_d2*nz_d2['DecimalDate'] + c_d2, color=colors2[4], linestyle = "solid")
plt.plot(nz_d3['DecimalDate'], m_d3*nz_d3['DecimalDate'] + c_d3, color=colors2[4], linestyle = "solid")
plt.plot(nz_d4['DecimalDate'], m_d4*nz_d4['DecimalDate'] + c_d4, color=colors2[4], linestyle = "solid")

plt.scatter(nz_d1['DecimalDate'], nz_d1['offset'], alpha = a, color=colors2[4], s = size1)
plt.scatter(nz_d2['DecimalDate'], nz_d2['offset'], alpha = a, color=colors2[4], s = size1)
plt.scatter(nz_d3['DecimalDate'], nz_d3['offset'], alpha = a, color=colors2[4], s = size1)
plt.scatter(nz_d4['DecimalDate'], nz_d4['offset'], alpha = a, color=colors2[4], s = size1)
plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
plt.xlim([1980, 2020])
plt.ylim([-15, 10])
plt.legend()
plt.title('New Zealand Tree Ring Offsets by Latitude and Year')
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure9.png',
            dpi=300, bbox_inches="tight")
plt.close()



"""
Trying to do the same as above for the Chile data
"""

chile_a1 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]  # North of 40S, 1980 - 1990
chile_a2 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]  # North of 40S, 1990 - 2000
chile_a3 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]  # etc...
chile_a4 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

chile_b1 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]
chile_b2 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
chile_b3 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
chile_b4 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

chile_c1 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]
chile_c2 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
chile_c3 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
chile_c4 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

chile_d1 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]  # > -998 keeps this portion from grabbing the Eastborne data set at -999.
chile_d2 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
chile_d3 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
chile_d4 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

A_chile_a1 = np.vstack([chile_a1['DecimalDate'], np.ones(len(chile_a1['DecimalDate']))]).T
A_chile_a2 = np.vstack([chile_a2['DecimalDate'], np.ones(len(chile_a2['DecimalDate']))]).T
A_chile_a3 = np.vstack([chile_a3['DecimalDate'], np.ones(len(chile_a3['DecimalDate']))]).T
A_chile_a4 = np.vstack([chile_a4['DecimalDate'], np.ones(len(chile_a4['DecimalDate']))]).T

A_chile_b1 = np.vstack([chile_b1['DecimalDate'], np.ones(len(chile_b1['DecimalDate']))]).T
A_chile_b2 = np.vstack([chile_b2['DecimalDate'], np.ones(len(chile_b2['DecimalDate']))]).T
A_chile_b3 = np.vstack([chile_b3['DecimalDate'], np.ones(len(chile_b3['DecimalDate']))]).T
A_chile_b4 = np.vstack([chile_b4['DecimalDate'], np.ones(len(chile_b4['DecimalDate']))]).T

A_chile_c1 = np.vstack([chile_c1['DecimalDate'], np.ones(len(chile_c1['DecimalDate']))]).T
A_chile_c2 = np.vstack([chile_c2['DecimalDate'], np.ones(len(chile_c2['DecimalDate']))]).T
A_chile_c3 = np.vstack([chile_c3['DecimalDate'], np.ones(len(chile_c3['DecimalDate']))]).T
A_chile_c4 = np.vstack([chile_c4['DecimalDate'], np.ones(len(chile_c4['DecimalDate']))]).T

A_chile_d1 = np.vstack([chile_d1['DecimalDate'], np.ones(len(chile_d1['DecimalDate']))]).T
A_chile_d2 = np.vstack([chile_d2['DecimalDate'], np.ones(len(chile_d2['DecimalDate']))]).T
A_chile_d3 = np.vstack([chile_d3['DecimalDate'], np.ones(len(chile_d3['DecimalDate']))]).T
A_chile_d4 = np.vstack([chile_d4['DecimalDate'], np.ones(len(chile_d4['DecimalDate']))]).T

m_a1, c_a1 = np.linalg.lstsq(A_chile_a1, chile_a1['offset'], rcond=None)[0]
m_a2, c_a2 = np.linalg.lstsq(A_chile_a2, chile_a2['offset'], rcond=None)[0]
m_a3, c_a3 = np.linalg.lstsq(A_chile_a3, chile_a3['offset'], rcond=None)[0]
m_a4, c_a4 = np.linalg.lstsq(A_chile_a4, chile_a4['offset'], rcond=None)[0]

m_b1, c_b1 = np.linalg.lstsq(A_chile_b1, chile_b1['offset'], rcond=None)[0]
m_b2, c_b2 = np.linalg.lstsq(A_chile_b2, chile_b2['offset'], rcond=None)[0]
m_b3, c_b3 = np.linalg.lstsq(A_chile_b3, chile_b3['offset'], rcond=None)[0]
m_b4, c_b4 = np.linalg.lstsq(A_chile_b4, chile_b4['offset'], rcond=None)[0]

m_c1, c_c1 = np.linalg.lstsq(A_chile_c1, chile_c1['offset'], rcond=None)[0]
m_c2, c_c2 = np.linalg.lstsq(A_chile_c2, chile_c2['offset'], rcond=None)[0]
m_c3, c_c3 = np.linalg.lstsq(A_chile_c3, chile_c3['offset'], rcond=None)[0]
m_c4, c_c4 = np.linalg.lstsq(A_chile_c4, chile_c4['offset'], rcond=None)[0]

m_d1, c_d1 = np.linalg.lstsq(A_chile_d1, chile_d1['offset'], rcond=None)[0]
m_d2, c_d2 = np.linalg.lstsq(A_chile_d2, chile_d2['offset'], rcond=None)[0]
m_d3, c_d3 = np.linalg.lstsq(A_chile_d3, chile_d3['offset'], rcond=None)[0]
m_d4, c_d4 = np.linalg.lstsq(A_chile_d4, chile_d4['offset'], rcond=None)[0]

"""
Testing the Figure
"""
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
a = 0.15
size1 = 15
fig = plt.figure(3)
# plt.plot(chile_a1['DecimalDate'], m_a1*chile_a1['DecimalDate'] + c_a1, label='North of 40S', color='black', linestyle = "dashdot")
# plt.plot(chile_a2['DecimalDate'], m_a2*chile_a2['DecimalDate'] + c_a2, color='black', linestyle = "dashdot")
# plt.plot(chile_a3['DecimalDate'], m_a3*chile_a3['DecimalDate'] + c_a3, color='black', linestyle = "dashdot")
# plt.plot(chile_a4['DecimalDate'], m_a4*chile_a4['DecimalDate'] + c_a4, color='black', linestyle = "dashdot")
#
# plt.scatter(chile_a1['DecimalDate'], chile_a1['offset'], alpha = a, color='black', s = size1)
# plt.scatter(chile_a2['DecimalDate'], chile_a2['offset'], alpha = a, color='black', s = size1)
# plt.scatter(chile_a3['DecimalDate'], chile_a3['offset'], alpha = a, color='black', s = size1)
# plt.scatter(chile_a4['DecimalDate'], chile_a4['offset'], alpha = a, color='black', s = size1)
# There is no data at higher than 40S for the Chilean sites#

plt.plot(chile_b1['DecimalDate'], m_b1*chile_b1['DecimalDate'] + c_b1, label='40-45S', color=colors[1], linestyle = "dotted")
plt.plot(chile_b2['DecimalDate'], m_b2*chile_b2['DecimalDate'] + c_b2, color=colors[1], linestyle = "dotted")
plt.plot(chile_b3['DecimalDate'], m_b3*chile_b3['DecimalDate'] + c_b3, color=colors[1], linestyle = "dotted")
plt.plot(chile_b4['DecimalDate'], m_b4*chile_b4['DecimalDate'] + c_b4, color=colors[1], linestyle = "dotted")

plt.scatter(chile_b1['DecimalDate'], chile_b1['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(chile_b2['DecimalDate'], chile_b2['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(chile_b3['DecimalDate'], chile_b3['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(chile_b4['DecimalDate'], chile_b4['offset'], alpha = a, color=colors[1], s = size1)

plt.plot(chile_c1['DecimalDate'], m_c1*chile_c1['DecimalDate'] + c_c1, label='45-50S', color=colors2[1], linestyle = "dashed")
plt.plot(chile_c2['DecimalDate'], m_c2*chile_c2['DecimalDate'] + c_c2, color=colors2[1], linestyle = "dashed")
plt.plot(chile_c3['DecimalDate'], m_c3*chile_c3['DecimalDate'] + c_c3, color=colors2[1], linestyle = "dashed")
plt.plot(chile_c4['DecimalDate'], m_c4*chile_c4['DecimalDate'] + c_c4,  color=colors2[1], linestyle = "dashed")

plt.scatter(chile_c1['DecimalDate'], chile_c1['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(chile_c2['DecimalDate'], chile_c2['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(chile_c3['DecimalDate'], chile_c3['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(chile_c4['DecimalDate'], chile_c4['offset'], alpha = a, color=colors2[1], s = size1)

plt.plot(chile_d1['DecimalDate'], m_d1*chile_d1['DecimalDate'] + c_d1, label='50-55S', color=colors[5], linestyle = "solid")
plt.plot(chile_d2['DecimalDate'], m_d2*chile_d2['DecimalDate'] + c_d2, color=colors[5], linestyle = "solid")
plt.plot(chile_d3['DecimalDate'], m_d3*chile_d3['DecimalDate'] + c_d3, color=colors[5], linestyle = "solid")
plt.plot(chile_d4['DecimalDate'], m_d4*chile_d4['DecimalDate'] + c_d4, color=colors[5], linestyle = "solid")

plt.scatter(chile_d1['DecimalDate'], chile_d1['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(chile_d2['DecimalDate'], chile_d2['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(chile_d3['DecimalDate'], chile_d3['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(chile_d4['DecimalDate'], chile_d4['offset'], alpha = a, color=colors[5], s = size1)
plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
plt.title('Chilean Tree Ring Record Offsets Linearly Regressed')
# plt.xlim([1980, 2020])
# plt.ylim([-15, 10])
plt.legend()
plt.title('Chile Tree Ring Offsets by Latitude and Year')
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_Figure10.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
The trends seen in the data above: Figures 9 and 10, aren't really that helpful. For example, one line can be drawn from 
20 points while the other is 1 or 2 points. This is not represented at all in the Figure and will lead to unoptomized
interpretations. 
I need to figure out some way to weigh the trend-lines based on how many data points are there. 
"""
