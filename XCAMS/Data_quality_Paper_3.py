"""
Data Quality Paper 1 = adding descriptors and flagging
Data Quality Ppaer 2 = looking at blanks and making plots
This sheet (Data Quality Paper 3) calculate residuals of secondary standards and making plots

"""
import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
today = date.today()
from drawing import *
import seaborn as sns
import statsmodels.api as sm

# read in the csv file that was created at the end of the last script
df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_2_output/DF.csv')


knowns = ['CBOr','GB','CBAi','CBIn','UNSt','GB','OX1','OX1_SM'] # although this script is meant for secondaries only, it doesn't huty to just run it for everything, cuz I"m going to filter on it later on to make specific plots of certain groups of secondaries
sub_list = df.loc[df['AMScategID'].isin(knowns)]  # I'm keeping
knowns_Rs = np.unique(sub_list['New_R'])

df['CBL_stat_flags'] = -999 # add a new column to filter on or change later

# create some arrays in which to store data later
wmean = []
one_sigma = []
sterr = []
n = []
name = []
chi2_red = []
knownR = []
ams_cat = []
df_resdiuals = pd.DataFrame()

# lets loop through the subset of data that we've selected in the rows above
for i in range(0, len(knowns_Rs)):

    # this line below actually grabs the subset based on the R number
    subset = df.loc[df['New_R'] == knowns_Rs[i]].sort_values(by=['TP']).reset_index(drop=True)

    # line below: we only want to do stats on R numbers where there's at least 3 data points. This also helps remove
    # loads of one-off R numbers that would clutter the analysis
    if len(subset) > 3:
        wm = (np.mean(subset['RTS']))
        wmean.append(np.mean(subset['RTS']))  # calculate and append average RTS value
        one_sigma.append(np.std(subset['RTS'])) # calc and append standard deviation
        n.append(len(subset))

        # calc standard error
        error_squared = subset['RTSerr']**2
        oneover = 1/error_squared
        sum = np.sum(oneover)
        sterr.append(sum**-0.5) # the 4 lines above calculate and append the standard error

        # caclulate chi2 reduced
        data_squared = (subset['RTS'] - (np.mean(subset['RTS'])))**2
        error_squared = subset['RTSerr']**2
        numerator = np.sum(data_squared/error_squared)
        denominator = len(subset) - 1
        chi2 = (numerator/denominator)
        chi2_red.append(chi2)

        #prepare the plot
        one_sig = np.std(subset['RTS'])
        desc = subset['sampleDESC']
        ddd = subset['AMScategID']

        # append a few more things
        name.append(desc[0])
        knownR.append(knowns_Rs[i])
        ams_cat.append(ddd[0])

        # find residual
        subset['Residual'] = (subset['RTS'] - (np.mean(subset['RTS']))) / (np.std(subset['RTS']))

        fig = plt.figure(figsize=(12, 8))
        plt.scatter(subset['TP'], subset['Residual'], color='black', alpha=0.5)
        plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
        plt.fill_between(subset['TP'], -1, 1, alpha=.05, color='black')
        plt.fill_between(subset['TP'], -2, 2, alpha=.05, color='black')
        plt.title(f'{knowns_Rs[i]}, {desc[0]}, Chi2 Reduced = {"{:.1f}".format(chi2)}')
        plt.ylabel(f'Residual (x-\u0078\u0305/1-\u03c3)')
        plt.xlabel('TP, chronological lab identifier')
        plt.ylim(-3,3)
        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/{knowns_Rs[i]}_{desc[0]}.png', dpi=300, bbox_inches="tight")
        plt.close()

        # concatonate the residual data
        df_resdiuals = pd.concat([df_resdiuals, subset])


# save the arrays into a dataframe
res = pd.DataFrame({"Name": name, "R": knownR, "AMScategID": ams_cat, "Mean RTS": wmean, "Mean RTS 1sigma": one_sigma, "Chi2 Reduced": chi2_red, "n": n}).sort_values(by=['Chi2 Reduced']).reset_index(drop=True)
res.to_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/summary_table.csv')

df_resdiuals.to_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/df_with_residuals.csv')
