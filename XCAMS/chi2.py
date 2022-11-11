"""
Trying to understand the "goodness of fit test" that is used in AccelNet and also understand/be able to write/derive
our measurement precision on my own for deeper understanding.

According to J C Turnbull et al., "Chi square tests are used to evaluate the consistency of the data set by examining
the scatter of the mean values and their assigned uncertainties. When the chi-square right tail-probability is less
than 25% for the full dataset, or less than 2.5% for a single target, we increase sigma_ams to account for excess
variability.

The things I need to know for this is: in AccelNet, what is the chiLIM? Is it the chiStat for the 25% boundary of the
right tail?
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.stats import chisquare

"""
This region of the code explores the data downloaded from AccelNet (copied from the website, where the 
chi2 is calculated using the 14/12he ratio and the data is reduced by taking the AVERAGE OF EACH OX CATHODE
"""

# df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\TW3438_testing.xlsx', skiprows=3)

df2 = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\Book3.xlsx')
calibration_positions = [0, 5, 10, 15, 20, 25, 30, 35]

df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\testing_postcalams.xlsx', skiprows=3)


"""
Chi2 using output from AccelNet and FCIR calculation, each OX cathode is AVERAGED. 
"""
# The first thing we need is the "M" which is our FCIR (3a (Zondervan 2015))
# arrays are based on cell names in excel
g = []
columni = []
j = []
k = []
sig = []

for i in range(0, len(calibration_positions)):
    cat = df.loc[df['position'] == calibration_positions[i]]
    c14_i, c12_i, c13_i, t = cat['14Ccnts'], cat['12Ccurr'], cat['13Ccurr'], cat['Tdetect']
    fcir_i = (c14_i * c12_i) / (t * (c13_i**2))  # calculates PER RUN FCIR
    fcir_j = np.average(fcir_i)  # This is our "M"

    sigma_j = fcir_j / np.sqrt(sum(cat['14Ccnts']) + 1)
    # sigma_j = np.average(sigma_i)  # This is our "sigma"

    sigma_j2 = sigma_j**2           # This is our "sigma^2"
    Mz_num = fcir_j / sigma_j      # Equivalent to column J in excel sheet
    Mz_denom = 1 / sigma_j         # Equivalent to column K in excel sheet

    sig.append(sigma_j)
    g.append(fcir_j)
    columni.append(sigma_j2)
    j.append(Mz_num)
    k.append(Mz_denom)
#
chi2data = pd.DataFrame({"M": g, "sigma^2": columni, "Mznum": j, "Mzdenom": k, "sig": sig})
# chi2data.to_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\test2.xlsx')

mz_num = np.sum(chi2data['Mznum'])
mz_den = np.sum(chi2data['Mzdenom'])
mz = mz_num/mz_den

dof = (len(calibration_positions)) - 1
chi2data['chi2'] = ((chi2data['M'] - mz)**2 ) / chi2data['sigma^2']
# chi2data['chi2'] = ((chi2data['M'] - mz)**2 ) / chi2data['sig']
chi2_norm = np.sum(chi2data['chi2'])
chi2_red = np.sum(chi2data['chi2']) / dof

chilim = 14.1


print("X^2 using FCIR data and OX1's are averaged (cathode global, not runs): X^2: {}, chiLim: {}".format(chi2_red, chilim))















# """
# Chi2 using data from Accelnet and 12/14 ratio, each OX cathode is AVERAGED.
# """
# # The first thing we need is the "M" which is our FCIR (3a (Zondervan 2015))
# # arrays are based on cell names in excel
# g = []
# columni = []
# j = []
# k = []
# sig = []
# for i in range(0, len(calibration_positions)):
#     cat = df2.loc[df2['Pos'] == calibration_positions[i]]
#     # c14_i, c12_i, c13_i, t = cat['CntTotGT'], cat['12Cle'], cat['13Che'], 180
#     # fcir_i = (c14_i * c12_i) / (t * (c13_i**2))  # calculates PER RUN FCIR
#     fcir_i = cat['(14/12)he']   # calculates PER RUN FCIR
#     fcir_j = np.average(fcir_i)  # This is our "M"
#
#     # sigma_i = 1 / np.sqrt(cat['CntTotBG'] + 1)
#     sigma_i = cat['stat']
#     sigma_j = np.average(sigma_i)  # This is our "sigma"
#
#     sigma_j2 = sigma_j**2           # This is our "sigma^2"
#
#     Mz_num = fcir_j / sigma_j      # Equivalent to column J in excel sheet
#     Mz_denom = 1 / sigma_j         # Equivalent to column K in excel sheet
#
#     sig.append(sigma_j)
#     g.append(fcir_j)
#     columni.append(sigma_j2)
#     j.append(Mz_num)
#     k.append(Mz_denom)
# #
# chi2data = pd.DataFrame({"M": g, "sigma^2": columni, "Mznum": j, "Mzdenom": k, "sig": sig})
# # chi2data.to_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\test2.xlsx')
#
# mz_num = np.sum(chi2data['Mznum'])
# mz_den = np.sum(chi2data['Mzdenom'])
# mz = mz_num/mz_den
#
# dof = (len(calibration_positions)) - 1
# chi2data['chi2'] = ((chi2data['M'] - mz)**2 ) / chi2data['sigma^2']
# # chi2data['chi2'] = ((chi2data['M'] - mz)**2 ) / chi2data['sig']
# chi2_norm = np.sum(chi2data['chi2'])
# chi2_red = np.sum(chi2data['chi2']) / dof
#
# chilim = 14.1
#
#
# print("X^2 using 14/12He ratio data and OX1's are averaged (cathode global, not runs): X^2: {}, chiLim: {}".format(chi2_red, chilim))
#
#
# """
# Lets try only using scipy chisquare function:
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.chisquare.html
# """
#
# df2 = pd.DataFrame()
# for i in range(0, len(calibration_positions)):
#     cat = df.loc[df['position'] == calibration_positions[i]]
#     df2 = pd.concat([df2, cat])
#
# c14_i, c12_i, c13_i, t = df2['14Ccnts'], df2['12Ccurr'], df2['13Ccurr'], df2['Tdetect']
# df2['FCIR'] = (c14_i * c12_i) / (t * (c13_i**2))  # calculates PER RUN FCIR
#
#
# x = chisquare(df2['FCIR'], ddof=7)
# print(x)
#
#
#




































# df2.to_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\test3.xlsx')  # checking concat works




















