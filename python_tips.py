import numpy as np
import pandas as pd
# """
# It's hard to write code from scratch, an empty Python page.
# Usually I'm referencing one or many of my old python files to find
#     some syntax or bit of code to perform some function.
# This isn't so useful because they are all spread out over heaps of
#     different codes.
# This code resolves that by putting all of the important code I need,
#     and the hacks that I have learned, in one place.
#
# Some areas of this code will use real examples using a Pokemon code I grabbed
# from Youtube (see "pokemon.py")
#
# Helpful Youtuber and their Github Pages
# https://github.com/sp8rks/MSE2001python/tree/main/module_examples
# https://www.youtube.com/watch?v=fwZahTYfyxA&t=2280s&ab_channel=TaylorSparks
# https://www.youtube.com/watch?v=tRKeLrwfUgU&ab_channel=NicholasRenotte
#
# """
#
# ################################################################
# """
# # COMMONLY IMPORTED LIBRARIES
# """
# import pandas as pd
# import openpyxl
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# import numpy as np
# from numpy.fft import fft, ifft
# import seaborn as sns
#
# import datetime
# from astropy.time import Time
#
# ################################################################
# """ IMPORTING DATA FROM EXCEL, CSV, TXT File """
#
# # READ AN EXCEL FILE
# df = pd.read_excel(r'INSERT FILE PATH\'SHEET TITLE'', sheet_name='X')
#   can ignore sheet name if there is no specific sheet name
#
# # READ A CSV FILE
# df = pd.read_csv(
#
# # examples
# df = pd.read_csv(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
#                  r'\The Science\Stats and Data Analysis'
#                  r'\Matlab and Python Files'
#                  r'\pokemon_data.csv')
# df2 = pd.read_csv(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
#                  r'\The Science\Stats and Data Analysis'
#                  r'\Matlab and Python Files'
#                  r'\output.csv')
#
# ################################################################
# """ Clean up the file """
#
# # Check where are empty cells
# emptycells = df.isnull().sum()
# print(emptycells)
#
# # Drop ALL NaN rows from the datasheet
# df.dropna(inplace=True)
#
# # Drop NaNs from SPECIFIC COLUMNS
# llnl = llnl.dropna(subset=['D14C'])
#
# # Import a variable from the sheet, and drop the NaN's.
# x = df['x'].dropna()
#
# # If you want to drop a column, leave it here on this list.
# df = df.drop(columns=['Column Names that I want to drop'], axis = 1)
#
# # Do you need to change the name of a column in the dataframe?
# df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
# df.rename(columns={"A": "a", "B": "c"})
#
# """
# MERGING DATASETS!
# """
# # add a key to data before merging...
# # https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
# # result = pd.concat(frames, keys=["x", "y", "z"])
#
# # Merge two datasets along a column, (At least one column names must align from each sheet)
# # combine = pd.merge(df1,df2) Gets rid of some data, like empty parts
# # combine = pd.merge(df1,df2, how='outer') Keeps ALL Data
# """
# How to merge two sets of data that are different in space/time
# For example
#     one dataset has 10,000 C02 measurements with 1) times and 2) measurements
#     a second dataset has 100 measurements with 1) times and 2) wind direction
#
# This block of code can add the wind direction to the associated co2 measurements!
#
# If you leave out the condition, how= outer, the result prints the data
# only containing that with the lesser variable (ex. I only have 5 wind measurements,
# it creates a dataframe with only 5 lines). Adding this condition keeps the whole dataset.
#
# """
#
#
# import numpy as np
# import pandas as pd
# #
# df1 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
#                     r'\The Science\Stats and Data Analysis'
#                     r'\Matlab and Python Files\testing.xlsx')
# df2 = pd.read_excel(r'G:\My Drive\Work\GNS Radiocarbon Scientist'
#                     r'\The Science\Stats and Data Analysis'
#                     r'\Matlab and Python Files\testing2.xlsx')
# # print(df1.columns)
# # print(df2.columns)
# combine = pd.merge(df1, df2, how='outer')
# print()
#
#
#
# ###############################################################
# """
# CHECK THE FILE SEEMS CORRECTLY IMPORTED
# """
#
# # print(df.head(10))  # print the top X amount of lines
# # print(df.tail(10))  # print the bottom X amount of lines
# # print(df.columns) # show me all the column names!
#
# ################################################################
# """
# INDEX / FILTER THE DATA YOU NEED
# """
#
# # Grab ONE column
# Type1 = df['Type 1']
#
# # Grab TWO Columns, etc...
# Types = df[['Type 1','Type 2']]
# #print(Types)
#
# # What unique vales are there?
# #Unique = df.'Type 2'.unique # not working...
#
#
# # Say I want to see only data with value X in column Y
# # For example, I want all data for Pokemon with "Type 1" = "Fire"
# Fire = df.loc[df['Type 1'] == "Fire" ]
# #print(Fire)
#
# # Filter or INDEX based on TWO types of data
# grass_poison = df.loc[(df['Type 1'] == 'Grass') & (df['Type 2'] == 'Poison')] # filtering based on two types of data AND
# #print(grass_poison)
#
# # Another example of filtering based on other real data I have (from BarrowCO2Data.py)
# # df = df.loc[(df['year'].between(2000, 2011))]  # filter values from 2000-2011
# # df = df.loc[(df['value'] > 0)]  # filter out all flag values (-1000)
#
# # Index with iloc: Grab the 15th row of the dataset
# filter_w_iloc = df.iloc[1]
# #print(filter_w_iloc)
# filter_w_iloc2 = df.iloc[1, 1]  # [X, y] , [Row, Column]
# #print(filter_w_iloc2)
#
#
# # slice with iloc
# #slice = df.iloc[22:33]
# #print(slice)
#
# #downsample data to every 10th data point
# #df_downsampled = df.iloc[::100, :]
# #print(df_downsampled)
#
# ##############################################
# """
# PERFORM MATH ON THE DATA / STORE IN NEW COLUMNS
# """
# # numpy mathematical functions
# # https://numpy.org/doc/stable/reference/routines.math.html
# # ADD COLUMNS AND CREATE NEW COLUMN
# df['New Column'] = df['Attack'] + df['Defense']
# print(df.head(10))
#
# ##############################################
#
# """
# BASIC PLOTTING IN PYTHON
# """
#
# # IMPORT BODACIOUS COLORS
# # https://seaborn.pydata.org/tutorial/color_palettes.html
# colors = sns.color_palette("rocket", 3)
# # seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
# # #            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry
#
# # Generate first panel
# # remember, the grid spec is rows, then columns
# # xtr_subsplot = fig.add_subplot(gs[0:4, 0:2])
#
# # plot data for left panel
# # fig = plt.figure(1)
# # plt.scatter(X, Y, linestyle='-', marker='^', label='NaOH Measured 14CO2 at BARING HEAD from RRL', color=colors[2]) # plot data
# # # create a legend
# # plt.legend()
# # plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
# # # plot limits
# # plt.xlim([min(X), max(X)])
# # plt.ylim([min(Y), max(Y)])
#
# # save the figure
# # plt.savefig(r'PATH / Figure name . png', dpi=300, bbox_inches="tight")
#
#
# #plotting with error bars
#
# #plt.errorbar(bhd_date, bhd_14c, yerr=bhd_14c_err, fmt = 'o',color=colors[2],
# #             ecolor='black', elinewidth = 1, capsize=2, label='BHD NaOH 14CO2')
#
# """
# SAVE DATA TO NEW FILE
# """
#
#
# """
# MISC
# """
#
# # change date to decimal date
# # import datetime
# # from astropy.time import Time
#
# # input_date =  datetime.datetime(2007, 4, 14, 11, 42, 50)
# # astropy_time_object = Time(input_date,format='datetime')
# #
# # decimal_year = astropy_time_object.decimalyear
# #
# # print(decimal_year)
# # #2007.2835289827499
#
# # t-test
# # https://www.statology.org/two-sample-t-test-python/
#
# # print conclusions, keep decimal points short.
# # print("The average and standard error for NWT4 measured at RRL is {:.2f} \u00B1 {:.2f}".format(y4_average, y4_stderr))
#
#
# # # do some final math
# # def final_calculation(x):
# #     result1 = np.average(x)
# #     result2 = np.std(x)
# #     result2 = result2 / len(x)
# #     # return result1, result2
# #     return print("The average and standard error is {:.1f} \u00B1 {:.1f}".format(result1, result2))
# #
# # final_calculation(y1)
# # final_calculation(y2)
# # final_calculation(y3)
# # final_calculation(y4)




# # convert the dd/mm/yyyy to decimal date (found in Heidelberg Intercomparison2)
# for i in range(0, len(x_plot)):
#     j = x_plot[i]
#     decy = pyasl.decimalYear(j)
#     decy = float(decy)
#     # print(decy)
#     array.append(decy)
# print(array)
# x_decimal = array

fake_x = np.linspace(1980, 2020, 1000)
print(fake_x)
