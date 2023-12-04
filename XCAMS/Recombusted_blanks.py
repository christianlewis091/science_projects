"""
Jocelyn requested that I take a look at some of the recombusted blank.
This refers to:
14047/1 and 14047/11, and how the blanks look during normal scenarious versus "recombustion" scenarios.

Margaret will tell me the job# of the ones that have been recombusted.
14047/11: 221623, 221624, 221625
14047/1: 221248, 221626, 221627

"""
# Import some stuff
import pandas as pd
import numpy as np
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.gridspec as gridspec


# Define the function I use to make date formatting easier
def long_date_to_decimal_date(x):
    array = []  # define an empty array in which the data will be stored
    for i in range(0, len(x)):  # initialize the for loop to run the length of our dataset (x)
        j = x[i]  # assign j: grab the i'th value from our dataset (x)
        decy = pyasl.decimalYear(j)  # The heavy lifting is done via this Py-astronomy package
        decy = float(decy)  # change to a float - this may be required for appending data to the array
        array.append(decy)  # append it all together into a useful column of data
    return array  # return the new data


# import the two datasets
bar_1 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\bar1.xlsx')
bar_11 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\xcams\bar11.xlsx')

# when exporting from RLIMS, asking for 14047/1 actually gave me 14047/1, /11, and /12, so I need to make sure I only have the field I want.
bar_1 = bar_1.loc[(bar_1['R'] == '14047/1')]


bar_1 = bar_1.dropna(subset='Ratio to standard').reset_index(drop=True)  # clean up the file by dropping all the empty rows that come from the importation of the prepocessing data.
bar_11 = bar_11.dropna(subset='Ratio to standard').reset_index(drop=True)  # clean up the file by dropping all the empty rows that come from the importation of the prepocessing data.

bar_1['Date Run'] = long_date_to_decimal_date(bar_1['Date Run'])  # convert dates to decimal dates by calling my function
bar_11['Date Run'] = long_date_to_decimal_date(bar_11['Date Run'])

"""
This is the quick and dirty way to exclude the test samples from the normal background dataset, this probably could be
done with a nice list and loop, or a really nice pandas indexing function but need the quick result for now. 
"""
max_filter = 0.01
bar_1 = bar_1.loc[(bar_1['Ratio to standard'] < max_filter)]  # This line and the one below filters for outliers that could skew the final analysis.
bar_11 = bar_11.loc[(bar_11['Ratio to standard'] < max_filter)]
bar_1 = bar_1.loc[(bar_1['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag
bar_11 = bar_11.loc[(bar_11['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag

bar_1_a = bar_1.loc[(bar_1['Job'] != 221248.0)]
bar_1_a = bar_1_a.loc[(bar_1['Job'] != 221626.0)]
bar_1_a = bar_1_a.loc[(bar_1['Job'] != 221627.0)]

bar_11_a = bar_11.loc[(bar_11['Job'] != 221623.0)]
bar_11_a = bar_11_a.loc[(bar_11['Job'] != 221624.0)]
bar_11_a = bar_11_a.loc[(bar_11['Job'] != 221625.0)]

x = pd.DataFrame({})
y = pd.DataFrame({})
list1 = [221248.0, 221626.0, 221627.0]
list2 = [221623.0, 221624.0, 221625.0]
for i in range(0, len(list1)):
    k = bar_1.loc[(bar_1['Job'] == list1[i])]
    x = pd.concat([x, k])

for i in range(0, len(list2)):
    k = bar_11.loc[(bar_11['Job'] == list2[i])]
    y = pd.concat([y, k])

"""
What's the average and 1-sigma of the standards when I only look at the non-Recombusted ones (the normal ones?)
"""

bar_1_average = np.average(bar_1_a['Ratio to standard'])
bar_11_average = np.average(bar_11_a['Ratio to standard'])

bar_1_std = np.std(bar_1_a['Ratio to standard'])
bar_11_std = np.std(bar_11_a['Ratio to standard'])

bar_1_recombusted_average = np.average(x['Ratio to standard'])
bar_11_recombusted_average = np.average(y['Ratio to standard'])

bar_1_recombusted_std = np.std(x['Ratio to standard'])
bar_11_recombusted_std = np.std(y['Ratio to standard'])

print("The average RTS of 14047/1, normally is: {} \u00B1 {} ".format(bar_1_average, bar_1_std))
print("The average RTS of 14047/1, recombusted is: {} \u00B1 {} ".format(bar_1_recombusted_average,
                                                                         bar_1_recombusted_std))
print()
print("The average RTS of 14047/11, normally is: {} \u00B1 {} ".format(bar_11_average, bar_11_std))
print("The average RTS of 14047/11, recombusted is: {} \u00B1 {} ".format(bar_11_recombusted_average,
                                                                          bar_11_recombusted_std))

# some items for plotting later
size1 = 5
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']

# plotting "x" the name for the recombusted's

fig = plt.figure(4, figsize=(16.1, 10))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=.5, hspace=.5)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.errorbar(x['Date Run'], x['Ratio to standard'], label='14047/1, recombusted', yerr=x['Ratio to standard error'], fmt='o', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.axhline(y=bar_1_recombusted_average, color=colors[3], linestyle='-')
plt.axhspan(bar_1_recombusted_average - bar_1_recombusted_std, bar_1_recombusted_average + bar_1_recombusted_std, alpha=0.1, color=colors[3])
plt.legend(fontsize=7.5)
plt.ylim(0.000, max_filter)
plt.xlim(2022, 2023)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.errorbar(bar_1_a['Date Run'], bar_1_a['Ratio to standard'], label='14047/1, "normal"',yerr=bar_1_a['Ratio to standard error'], fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.axhline(y=bar_1_average, color=colors2[3], linestyle='-')
plt.axhspan(bar_1_average - bar_1_std, bar_1_average + bar_1_std, alpha=0.1, color=colors2[3])
plt.legend(fontsize=7.5)
plt.ylim(0.000, max_filter)
plt.xlim(2013, 2023)
plt.ylabel('RTS', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.errorbar(y['Date Run'], y['Ratio to standard'], label='14047/11, recombusted', yerr=y['Ratio to standard error'],fmt='o', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.axhline(y=bar_11_recombusted_average, color=colors[3], linestyle='-')
plt.axhspan(bar_11_recombusted_average - bar_11_recombusted_std, bar_11_recombusted_average + bar_11_recombusted_std, alpha=0.1, color=colors[3])
plt.legend(fontsize=7.5)
plt.ylim(0.000, max_filter)
plt.xlim(2022, 2023)
plt.xlabel('Date', fontsize=14)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(bar_11_a['Date Run'], bar_11_a['Ratio to standard'], label='14047/11, "normal"', yerr=bar_11_a['Ratio to standard error'], fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1,capsize=2)
plt.axhline(y=bar_11_average, color=colors2[3], linestyle='-')
plt.axhspan(bar_11_average - bar_11_std, bar_11_average + bar_11_std, alpha=0.1, color=colors2[3])
plt.legend(fontsize=7.5)
plt.ylim(0.000, max_filter)
plt.xlim(2013, 2023)
plt.xlabel('Date', fontsize=14)
plt.ylabel('RTS', fontsize=14)  # label the y axis

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/XCAMS_data/Recombusted_blanks.png',
            dpi=300, bbox_inches="tight")