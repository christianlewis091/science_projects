"""
This file is used to pre-process data that will compare measurements of the same Kauri Tree ring from ANSTO and
us at RRL.
This file doesn't do any math, it just cleans and re-packages the data into a Pandas DataFrame for later use.
"""

import pandas as pd
import numpy as np
import openpyxl

def fm_to_d14c(fm, fm_err, date):
    # D14C = 1000*(fm - 1)   # first, find D14C (without the age correction)
    age_corr = np.exp((1950 - date) / 8267)
    Del14C = 1000 * ((fm*age_corr) - 1)
    Del14C_err = 1000 * fm_err
    return Del14C, Del14C_err


df = pd.read_excel(r'H:\Science\Datasets\Ansto_intercomparison.xlsx', skiprows=28)

ansto = df.loc[(df['Site'] == 'ANSTO')]                                              # extract ANSTO data
ansto = ansto.rename(columns={"Year of Growth":"Decimal_date", "error":"FM_err"})    # ensure the column is named correctly for later
x = fm_to_d14c(ansto['FM'], ansto['FM_err'], ansto['Decimal_date'])                  # add the D14C column to ANSTO by calculating it using my function
ansto['D14C'] = x[0]                                                                 # add the D14C output
ansto['D14C_err'] = x[1]                                                             # add the D14C_err output
ansto = ansto[['Site','Decimal_date', 'D14C', 'D14C_err','FM','FM_err']]

rrl = df.loc[(df['Site'] == 'RRL')]                                                  # extract RRL
rrl = rrl.rename(columns={"Year of Growth": "Decimal_date", "error": "FM_err"})      # ensure the column is named correctly for later
rrl = rrl[['Site', 'NZA','R','Job', 'Decimal_date', 'D14C', 'D14C_err','FM','FM_err']]

combine_ANSTO = pd.concat([rrl, ansto])

print('I did it')







