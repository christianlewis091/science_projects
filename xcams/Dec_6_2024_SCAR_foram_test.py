"""
We ran the SCAR test wheel to see if we'd be able to measure this student's small samples
Here is some analysis of the results

Dec 6, 2024
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from RLIMS_eqns_as_funcs import *
import math

# grab a recent export of data from RLIMS
df = pd.read_excel('I:\C14Data\C14_blank_corrections_NEW\import_from_RLIMS\historical_data/TW3545standards.xlsx')
df['TW'] = df['TW'].astype(str)
df = df.loc[df['TW'] == '3545.0']

# write the selected wheel so I can read it in easier/faster
# df.to_excel('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3545/python_stuff/test.xlsx')

"""
What's the MCC
"""

df = pd.read_excel('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3545/python_stuff/test.xlsx')

# find the blanks
blanks = df.loc[df['AMS Category ID XCAMS'] == 'CBIn']

sl = 'I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3545/python_stuff'

UCI_MCC_plot(blanks['wtgraph'], blanks['Ratio to standard'], sl, 'MCC_v1')

"""
We can determine from the MCC_v1 that the M value is between 1 and 0.8 from this we can calculate an MCC value for LAC and LAA1 corals
"""

df['M'] = 0.9 # m value from MCC_v1
df['MCC'] = -999 # placeholder

# find the small coral samples and apply the MCC value
df.loc[((df['Samples::Sample ID'] == 'LAC1') | (df['Samples::Sample ID'] == 'LAA1')) & (df['wtgraph'] < 0.2), 'MCC'] = df['M']/(1000*df['wtgraph'])
df.to_excel('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3545/python_stuff/test2.xlsx')

# choose three coral standards as our secondaries. These are LAC1, expected age is 3243.
seconds = [89547, 89553, 89551]
secondsdf = df.loc[df['TP'].isin(seconds)]
print(secondsdf)
dcc_test = [0.01, 0.05, 0.1, 0.15, 0.2]
for i in range(0, len(dcc_test)):

    # calculate RTS with the different dcc's
    rts_corr = rts_corrected(secondsdf['Ratio to standard'],
                  secondsdf['MCC'], dcc_test[i], 0)

    rce = rts_corr_error(secondsdf['Ratio to standard'], secondsdf['Ratio to standard error'],
                         secondsdf['MCC'], 0.45*secondsdf['MCC'],
                         dcc_test[i], 0.45*dcc_test[i], 0,0)
    # Stand spec act const = 0.987
    fc = f_normed_corrected(rts_corr, 0.987)
    fce = f_corr_norm_err(rts_corr, rce, 0.13)

    # cra = -8033*math.log(fc)
    # crae = -8033*math.log(fce)

    plt.scatter(secondsdf['wtgraph'], fc)
    plt.axhline(.668)
    plt.show()
