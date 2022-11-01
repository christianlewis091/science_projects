import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyAstronomy import pyasl
import matplotlib.gridspec as gridspec

"""
Tuesday 1/11/2022 12:26

Here’s the C13 data – only those run on the dual inlet.
I’ve flagged bad data that can be ignored (in a separate tab).  I haven’t had a thorough look at the data, so there 
could be more bad data that should be flagged.  But good enough for now.
Some standards only have a single measurement, and many only have a couple of measurements (eg SIRI and GIRI samples).
I’d like to see how the 13C values scatter, as well as if there are any trends through time.  
Particularly we want to know if how we are doing in recent times – not sure if we want to look at just the last 1 year, 5 years, or something in between.

"""
"""Read in the data"""
df = pd.read_csv(r'H:\Science\Current_Projects\04_ams_data_quality\13C_standard_analysis_November2022\c13Standards2022_11_01.csv')
# for 1 year (begin 2022)
# df = df.loc[df['Job'] > 219966]
# # for 2 year (begin 2020)
# df = df.loc[df['Job'] > 214216]
# for 5 year (begin 2020)
df = df.loc[df['Job'] > 206292]

df = df.dropna(subset='SampleID')
df = df.dropna(subset='delta13C')
names = list((df['SampleID'].unique()))
#
"""Based on each unique sample ID, calculate summary information on each one"""
name = []
average = []
stddev = []
count = []

for i in range(0, len(names)):
    current_name = names[i]
    current_std = df.loc[df['SampleID'] == current_name]
    name.append(current_name)
    average.append(np.average(current_std['delta13C']))
    stddev.append(np.std(current_std['delta13C']))
    count.append(len(current_std))

    plt.scatter(current_std['Job'], current_std['delta13C'], label='{}'.format(current_name), color='black')
    plt.axhline((np.average(current_std['delta13C'])), color='black', alpha=0.15)
    plt.legend()
    plt.savefig('H:/Science/Current_Projects/04_ams_data_quality/13C_standard_analysis_November2022/plots/value{y}.png'.format(y=i), dpi=300, bbox_inches="tight")
    plt.close()
data = pd.DataFrame({"Sample ID": name, "Average": average, "1-sigma": stddev, "N": count}).sort_values("Sample ID",ascending=False).reset_index(drop=True)
"""Write that data to an excel sheet"""
data.to_excel('H:/Science/Current_Projects/04_ams_data_quality/C13_reduced.xlsx')

"""
PLOTS
"""

#
# """Index the data in some logical way and plot it up"""
# flag_list = []
# for i in range(0, len(df)):
#     row = df.iloc[i]
#     if 'TIRI' in row['SampleID']:
#         flag_list.append('TIRI')
#     elif 'FIRI' in row['SampleID']:
#         flag_list.append('FIRI')
#     elif 'GIRI' in row['SampleID']:
#         flag_list.append('GIRI')
#     elif 'SIRI' in row['SampleID']:
#         flag_list.append('SIRI')
#     elif 'OxI' in row['SampleID']:
#         flag_list.append('Oxalic')
#     elif 'Oxalic' in row['SampleID']:
#         flag_list.append('Oxalic')
#     elif 'BHD' in row['SampleID']:
#         flag_list.append('RRL')
#     elif 'Kauri' in row['SampleID']:
#         flag_list.append('RRL')
#     elif 'ANU' in row['SampleID']:
#         flag_list.append('RRL')
#     elif 'kapuni' in row['SampleID']:
#         flag_list.append('RRL')
#     elif 'air' in row['SampleID']:
#         flag_list.append('RRL')
#     elif 'LAC1' in row['SampleID']:
#         flag_list.append('RRL')
#     elif 'LAA1' in row['SampleID']:
#         flag_list.append('RRL')
#     else:
#         flag_list.append('Misc')
#
# df['IndexFlag'] = flag_list
#
#
# a1, a2, a3, a4, a5 = '#7fcdbb', '#a1dab4', '#41b6c4', '#2c7fb8', '#253494'
# colors = [a1, a2, a3, a4, a5, a1, a2, a3, a4, a5, a1, a2, a3, a4, a5, a1, a2, a3, a4, a5, a1, a2, a3, a4, a5]
# shapes = ['o', 'D', '^', 'X', 's', 'p', 'P', '+', 'o', 'D', '^', 'X', 's', 'p', 'P', '+', 'o', 'D', '^', 'X', 's', 'p',
#           'P', '+', 'o', 'D', '^', 'X', 's', 'p', 'P', '+']
#
# def plot_13Cdata(indexname, plotname):
#     data = df.loc[df['IndexFlag'] == indexname]  # isolate the category you're interested in
#     subdata = list((data['SampleID'].unique()))  # find the subcategories within
#     print(subdata)
#
#     for i in range(0, len(subdata)):
#         col = colors[i]
#         shape = shapes[i]
#
#         name = subdata[i]
#         slice = data.loc[data['SampleID'] == name]
#         slice_av = np.average(slice['delta13C'])
#         plt.scatter(slice['Job'], slice['delta13C'], label='{}'.format(name), color=col, marker=shape)
#         plt.axhline(slice_av, color='black', alpha=0.15)
#         plt.legend()
#         plt.xlabel('Job Number')
#         plt.ylabel('Delta 13C')
#     plt.savefig('H:/Science/Current_Projects/04_ams_data_quality/{}.png'.format(plotname), dpi=300, bbox_inches="tight")
#     plt.close()
#
# x = plot_13Cdata('TIRI', 'TIRI_redo')
# x = plot_13Cdata('SIRI', 'SIRI_redo')
# x = plot_13Cdata('FIRI', 'FIRI_redo')
# x = plot_13Cdata('GIRI', 'GIRI_redo')
# x = plot_13Cdata('Oxalic', 'Oxalic_redo')
# x = plot_13Cdata('RRL', 'RRL_redo')
# x = plot_13Cdata('Misc', 'Misc_redo')
#
#
#
#
#
#
#
#
#
# flag_list2 = []
# for i in range(0, len(df)):
#     row = df.iloc[i]
#     if row['IndexFlag'] == 'Misc':
#         if i <= 5:
#             flag_list2.append('Misc')
#         if 10 >= i >= 6:
#             flag_list2.append('Misc2')
#         if 15 >= i >= 11:
#             flag_list2.append('Misc3')
#         if 20 >= i >= 16:
#             flag_list2.append('Misc3')
#         if 25 >= i >= 21:
#             flag_list2.append('Misc5')
#         else:
#             flag_list2.append('Misc6')
#     else:
#         flag_list2.append(row['IndexFlag'])
#
# df['IndexFlag'] = flag_list2