"""
October 6, 2022.
This file has been declared deprecated.
This file was meant to calculate and/or apply offsets to Cape Grim data.
Now, offsets are calculated in another script, with the directories shown after this code block.
The offsets are applied right before the data is harmonized to the BHD record for ONE OF THREE background references
for the SOAR Program. Therefore this file is not needed.

"""
#C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\scripts\heidelberg_intercomparison_wD14C.py
#C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\scripts\heidelberg_intercomparison_wFM.py
# C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\output\FinalOutput_12September2022.txt






# """
# Purpose:
#
# Calculate the offsets in the Cape Grim data using two offset types.
# 1. Pre and Post AMS offset
# 2. Smoothed offset using CCGCRV
#
# Writes the data to excel file.
#
# This data will LATER be harmonized with BHD as a reference background.
#
# """
#
# import numpy as np
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import pandas as pd
# import seaborn as sns
# from X_my_functions import long_date_to_decimal_date
# from B_CGO_BHD_harmonization import offset1, offset2, offset3, offset4, offset5, offset6
# from B_CGO_BHD_harmonization import error1, error2, error3, error4, error5, error6
# from A_heidelberg_intercomparison import dff  # import the dataframe to produce the smoothed offset calcs
# from A_heidelberg_intercomparison import cutoff
# from X_miller_curve_algorithm import ccgFilter
# from X_my_functions import monte_carlo_randomization_trend
# from scipy import stats
# from A_heidelberg_intercomparison import n
#
# colors = sns.color_palette("rocket", 6)
# colors2 = sns.color_palette("mako", 6)
# mpl.rcParams['pdf.fonttype'] = 42
# mpl.rcParams['font.size'] = 10
# size1 = 5
# """
#
# """
#
# """ STEP 1: LOAD UP AND TIDY THE DATA"""
# heidelberg = pd.read_excel(r'H:\The Science\Datasets'
#                            r'\heidelberg_cape_grim.xlsx', skiprows=40)
#
# # remove some of the columns that I dont want/need, to simplify the later merge
# heidelberg['key'] = np.ones(len(heidelberg))
# # add decimal dates to DataFrame if not there already
# x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
# x_init_heid = long_date_to_decimal_date(x_init_heid)
# heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe
#
# # drop NaN's in the column I'm most interested in
# heidelberg = heidelberg.dropna(subset=['D14C'])
# heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]  # remove an outlier
# heidelberg = heidelberg.drop(columns=['sampler_id', 'samplingheight', 'startdate', 'enddate',
#                                       'Average pf Start-date and enddate', 'date_d_mm_yr', 'date_as_number',
#                                       'samplingpattern',
#                                       'wheightedanalyticalstdev_D14C', 'nbanalysis_D14C', 'd13C', 'flag_D14C',
#                                       ], axis=1)
# """
# STEP 2: INDEX THE DATA ACCORDING TO TIMES LISTED ABOVE
# index 1 = "h1" for heidelberg-1, and so on.
# h1 = 1986 - 1991
# h2 = 1991 - 1994
# h3 = 1994 - 2006
# h4 = 2006 - 2009
# h5 = 2009 - 2012
# h6 = 2012 - 2016
# """
# h1 = heidelberg.loc[(heidelberg['Decimal_date'] < 1991)].reset_index()
# h2 = heidelberg.loc[(heidelberg['Decimal_date'] > 1991) & (heidelberg['Decimal_date'] < 1994)].reset_index()
# h3 = heidelberg.loc[(heidelberg['Decimal_date'] > 1994) & (heidelberg['Decimal_date'] < 2006)].reset_index()
# h4 = heidelberg.loc[(heidelberg['Decimal_date'] > 2006) & (heidelberg['Decimal_date'] < 2009)].reset_index()
# h5 = heidelberg.loc[(heidelberg['Decimal_date'] > 2009) & (heidelberg['Decimal_date'] < 2012)].reset_index()
# h6 = heidelberg.loc[(heidelberg['Decimal_date'] > 2012) & (heidelberg['Decimal_date'] < 2016)].reset_index()
#
# """
# In order to apply the offsets, I'm going to add a new column with the new value, rather than try
# to change to original value
# """
# # apply offsets using Pre and POst AMS OFFset
# h1['pre-postAMS_offset'] = h1['key'] * offset1  # first, deposit the offset into the excel sheet for future reference.
# h2['pre-postAMS_offset'] = h2['key'] * offset2  # the way i'm doing this is a bit of a hack, by multiplying it by the "key"
# h3['pre-postAMS_offset'] = h3['key'] * offset3  # which is set to 1 for data from heidelberg (0's  are for baring head)
# h4['pre-postAMS_offset'] = h4['key'] * offset4
# h5['pre-postAMS_offset'] = h5['key'] * offset5
# h6['pre-postAMS_offset'] = h6['key'] * offset6
# h1['pre-postAMS_offset_err'] = h1['key'] * error1  # first, deposit the offset into the excel sheet for future reference.
# h2['pre-postAMS_offset_err'] = h2['key'] * error2  # the way i'm doing this is a bit of a hack, by multiplying it by the "key"
# h3['pre-postAMS_offset_err'] = h3['key'] * error3  # which is set to 1 for data from heidelberg (0's  are for baring head)
# h4['pre-postAMS_offset_err'] = h4['key'] * error4
# h5['pre-postAMS_offset_err'] = h5['key'] * error5
# h6['pre-postAMS_offset_err'] = h6['key'] * error6
#
# h1['D14C_1'] = h1['D14C'] + offset1  # store offset values in new column
# h2['D14C_1'] = h2['D14C'] + offset2
# h3['D14C_1'] = h3['D14C'] + offset3
# h4['D14C_1'] = h4['D14C'] + offset4
# h5['D14C_1'] = h5['D14C'] + offset5
# h6['D14C_1'] = h6['D14C'] + offset6
#
# h1['weightedstderr_D14C_1'] = np.sqrt(h1['weightedstderr_D14C']**2 + error1**2)  # propogate the error and REPLACE original
# h2['weightedstderr_D14C_1'] = np.sqrt(h2['weightedstderr_D14C']**2 + error2**2)
# h3['weightedstderr_D14C_1'] = np.sqrt(h3['weightedstderr_D14C']**2 + error3**2)
# h4['weightedstderr_D14C_1'] = np.sqrt(h4['weightedstderr_D14C']**2 + error4**2)
# h5['weightedstderr_D14C_1'] = np.sqrt(h5['weightedstderr_D14C']**2 + error5**2)
# h6['weightedstderr_D14C_1'] = np.sqrt(h6['weightedstderr_D14C']**2 + error6**2)
#
# # merge heidelberg file back onto itself, after adding the first TYPE of offset...
# heidelberg = pd.merge(h1, h2, how='outer')
# heidelberg = pd.merge(heidelberg, h3, how='outer')
# heidelberg = pd.merge(heidelberg, h4, how='outer')
# heidelberg = pd.merge(heidelberg, h5, how='outer')
# heidelberg = pd.merge(heidelberg, h6, how='outer')
#
# # APPLY OFFSET USING SMOOTHED OFFSET
# offset_smoothed = monte_carlo_randomization_trend(dff['offset_xs'], heidelberg['Decimal_date'], dff['offset_ys'], dff['offset_errs'], cutoff, n)  # use the offset values to create an offset smoothing curve
# offset_smoothed_summary = offset_smoothed[2]  # extract summary file
# offset_smoothed_mean = offset_smoothed_summary['Means']  # grab means
# offset_smoothed_stdevs = offset_smoothed_summary['stdevs']  # grab stdevs
# heidelberg['smoothed_offset'] = offset_smoothed_mean # deposit the number for the smoothed offset in the excel sheet
# heidelberg['D14C_2'] = heidelberg['D14C'] + heidelberg['smoothed_offset']  # add it to the original data (correct the offset)
# heidelberg['smoothed_offset_error'] = offset_smoothed_stdevs
# heidelberg['weightedstderr_D14C_2'] = np.sqrt(heidelberg['weightedstderr_D14C']**2 + offset_smoothed_stdevs**2)
# # is there a meaningful difference between the smoothed offset and the Pre and Post offset?
#
# """
# I'm going to clean and deposit this Cape Grim data into it's own excel sheet for later use. I'm actually going to do this
# for all the Heidelberg data, CGO, Neumayer, and MCQ so that I can load them up right from the excel sheet without
# python having the run throuhg all the Monte Carlo stuff.
# """
# # df2_dates = df2_dates.rename(columns={"NZ/NZA": "NZ"})
# heidelberg = heidelberg.rename(columns={"weightedstderr_D14C": "D14C_err"})
# heidelberg = heidelberg.rename(columns={"F14C_ERR": "F14C_err"})
# heidelberg = heidelberg.rename(columns={"pre-postAMS_offset": "offset1"})
# heidelberg = heidelberg.rename(columns={"pre-postAMS_offset_err": "offset1_err"})
# heidelberg = heidelberg.rename(columns={"smoothed_offset": "offset2"})
# heidelberg = heidelberg.rename(columns={"smoothed_offset_error": "offset2_err"})
# heidelberg = heidelberg.rename(columns={"weightedstderr_D14C_2": "D14C_2_err"})
# heidelberg = heidelberg.rename(columns={"weightedstderr_D14C_1": "D14C_1_err"})
# # Reorder the columns in an order that makes more sense
# heidelberg = heidelberg[['#location', 'Decimal_date', 'D14C', 'D14C_err', 'offset1', 'offset1_err', 'D14C_1', 'D14C_1_err', 'offset2', 'offset2_err', 'D14C_2', 'D14C_2_err']]
# heidelberg.to_excel('CapeGrim_offset.xlsx')
#
