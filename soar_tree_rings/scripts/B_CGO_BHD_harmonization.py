"""
Status Update to this file on October 6, 2022.

The naming convention of this file (beginning with "B") was from a previous directory scheme, but I don't want to go around
changing file names, so I'm going to leave it as is.
This file was cleaned up today for a reboot of this project after GGMT.


----------------------------------------------
Purpose:
This file harmonizes two datasets, which will be ONE OF THREE background reference datasets for our SOAR paper #1.
In a previous work, I calculated time-variable difference between the Rafter/NIWA Baring Head D14CO2 dataset, and the
Heidelberg University Cape Grim D14CO2 dataset. This code can be found in the directory below this code block, analyzed in the form
of both FM, and D14C

Beacuse the analysis of these offsets are dependent on a Monte Carlo protocol which includes some randomization, the
literal results change each time the code is run (although it is the same within error). The absolute numbers used for
intercomparisons here are from a run on September 12, 2022, and can be found in the directory described after this code block.


Where BHD and CGO overlap before the gap in 1994, we will apply the following two offsets based on my previous calculation
1986 - 1991: Add 1.75 +- 0.10 to Heidelberg Data
1991 - 1994: Add 1.89 +- 0.20 to Heidelberg Data

In the gap period, no offset will be applied, and we will take the CGO data as it is. The reason we apply the offset
correction to CGO instead of BHD, is that the BHD record is longer and includes the whole bomb peak and would be more
challenging to offset correct.

After the gap, because the offset is within the GGMT goal of 0.5 per mil, and the sign changes, we link this up with the
gap, and apply no offset to the CGO dataset.

This file first applies the offset corrections to the CGO data, and then MERGES it with the BHD data to create
the "harmonized dataset".

"""
#C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\scripts\heidelberg_intercomparison_wD14C.py
#C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\scripts\heidelberg_intercomparison_wFM.py
# C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\output\FinalOutput_12September2022.txt

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date

""" LOAD UP AND TIDY THE DATA"""
# cape grim data
heidelberg = pd.read_excel(r'H:\Science\Datasets'
                           r'\heidelberg_cape_grim.xlsx', skiprows=40)
# Baring Head data excel file
baringhead = pd.read_excel(r'H:\Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')

# adding a key that can be useful later.
heidelberg['key'] = np.ones(len(heidelberg))
baringhead['key'] = np.zeros(len(baringhead))

# tidy up the data
# add decimal dates to DataFrame if not there already
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]
baringhead = baringhead.dropna(subset=['DELTA14C'])

# snip out the gaps: 1994 - 2006, and 2009 - 2012, and then merge back together
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < 1994)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] < 2009)]
snip3 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2012)]
snip = pd.merge(snip, snip2, how='outer')
snip = pd.merge(snip, snip3, how='outer')
baringhead = snip.reset_index(drop=True)

# drop some of the unnecessary columns that add clutter to the process
heidelberg = heidelberg.drop(columns=['#location', 'sampler_id', 'samplingheight', 'startdate', 'enddate',
                                      'Average pf Start-date and enddate', 'date_d_mm_yr', 'date_as_number',
                                      'samplingpattern',
                                      'wheightedanalyticalstdev_D14C', 'nbanalysis_D14C', 'd13C', 'flag_D14C',
                                      ], axis=1)
baringhead = baringhead.drop(columns=['SITE', 'NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                                      'DATE_COLL', 'date_as_number', 'DELTA13C_IRMS',
                                      'F14C', 'F14C_ERR', 'FLAG', 'METH_VESSEL',
                                      'METH_COLL'])

""" STEP 2: INDEX THE DATA ACCORDING TO TIMES LISTED ABOVE"""
# Baring head data does not need indexing because we will not apply corrections to it
# What are the current offsets (these are subject to change!)

# 1986 - 1991: Add 1.80 +- 0.18 to Heidelberg Data
# 1991 - 1994: Add 1.88 +- 0.16 to Heidelberg Data
# 1994 - 2006: No offset applied
# 2006 - 2009: Add 0.49 +- 0.07 to Heidelberg
# 2009 - 2012: Apply NO offset
# 2012 - 2016: Subtract 0.52 +- 0.06 to Heidelberg.

h1 = heidelberg.loc[(heidelberg['Decimal_date'] < 1991)].reset_index()
h2 = heidelberg.loc[(heidelberg['Decimal_date'] > 1991) & (heidelberg['Decimal_date'] < 1994)].reset_index()
h3 = heidelberg.loc[(heidelberg['Decimal_date'] > 1994) & (heidelberg['Decimal_date'] < 2006)].reset_index()
h4 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006) & (heidelberg['Decimal_date'] < 2009)].reset_index()
h5 = heidelberg.loc[(heidelberg['Decimal_date'] > 2009) & (heidelberg['Decimal_date'] < 2012)].reset_index()
h6 = heidelberg.loc[(heidelberg['Decimal_date'] > 2012) & (heidelberg['Decimal_date'] < 2016)].reset_index()

offset1 = 1.80
offset2 = 1.88
offset3 = 0
offset4 = 0
offset5 = 0
offset6 = 0
error1 = .18
error2 = .16
error3 = 0
error4 = 0
error5 = 0
error6 = 0

# apply the offsets to each of the slices.
h1['D14C'] = h1['D14C'] + offset1
h2['D14C'] = h2['D14C'] + offset2
h3['D14C'] = h3['D14C'] + offset3
h4['D14C'] = h4['D14C'] + offset4
h5['D14C'] = h5['D14C'] + offset5
h6['D14C'] = h6['D14C'] + offset6
h1['weightedstderr_D14C'] = np.sqrt(h1['weightedstderr_D14C']**2 + error1**2)  # propogate the error and REPLACE original
h2['weightedstderr_D14C'] = np.sqrt(h2['weightedstderr_D14C']**2 + error2**2)
h3['weightedstderr_D14C'] = np.sqrt(h3['weightedstderr_D14C']**2 + error3**2)
h4['weightedstderr_D14C'] = np.sqrt(h4['weightedstderr_D14C']**2 + error4**2)
h5['weightedstderr_D14C'] = np.sqrt(h5['weightedstderr_D14C']**2 + error5**2)
h6['weightedstderr_D14C'] = np.sqrt(h6['weightedstderr_D14C']**2 + error6**2)

""" STEP 4: MERGE ALL THE DATA! """
# for simplicity (and because I'm indexing the Heidelberg dataset much more than the Baring Head dataset right now, I'm going to change the
# baringhead column names to match those of the Heidelberg dataset
baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
baringhead = baringhead.rename(columns={"DELTA14C_ERR": "weightedstderr_D14C"})

# merge the data together
harmonized = pd.merge(baringhead, h1, how='outer')
harmonized = pd.merge(harmonized, h2, how='outer')
harmonized = pd.merge(harmonized, h3, how='outer')
harmonized = pd.merge(harmonized, h4, how='outer')
harmonized = pd.merge(harmonized, h5, how='outer')
harmonized = pd.merge(harmonized, h6, how='outer')

"""
A few of the data have errors of -1000 and this is throwing everything off
in later calculations...
I need to get rid of these...
"""
harmonized = harmonized.loc[(harmonized['weightedstderr_D14C'] > 0)]
harmonized = harmonized.drop(columns=['index'], axis=1)
harmonized = harmonized.dropna()

harmonized.sort_values(by=['Decimal_date'], inplace=True)
harmonized.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')

# make a plot.
harm1 = harmonized.loc[(harmonized['key'] == 0)]
harm2 = harmonized.loc[(harmonized['key'] == 1)]
x_bars = harm1['Decimal_date']
y_bars = harm1['D14C']
x_heids = harm2['Decimal_date']
y_heids = harm2['D14C']
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5
"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(x_bars, y_bars, marker='o', label='Data from Baring Head (RRL)', color=colors[3], s=size1, alpha = 0.5)
plt.scatter(x_heids, y_heids, marker='o', label='Data from CGO (Heidelberg)', color=colors2[3], s=size1, alpha = 0.5)
plt.legend()
# plt.title('All available data after 1980')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Harmonized_dataset.png', dpi=300, bbox_inches="tight")
plt.close()

"""
Figure 1 (again). All the data together
"""
farbe_bhd = '#4575b4'
farbe_bhd_bkgd = '#74add1'

farbe_sio = '#f46d43'
farbe_sio_bkgd ='#fdae61'

farbe_ansto = '#d73027'
farbe_maga = '#d73027'
farbe_heid = '#d73027'

fig = plt.figure(1)
plt.scatter(x_bars, y_bars, marker='o', label='Data from Baring Head (RRL)', color=farbe_bhd, s=size1, alpha = 0.5)
plt.scatter(x_heids, y_heids, marker='o', label='Data from CGO (Heidelberg)', color=farbe_heid, s=size1, alpha = 0.5)
plt.legend()
# plt.title('All available data after 1980')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/Harmonized_dataset2.png', dpi=300, bbox_inches="tight")
plt.close()
