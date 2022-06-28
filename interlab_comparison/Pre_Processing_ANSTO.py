"""
This file is used to pre-process data that will compare measurements of the same Kauri Tree ring from ANSTO and
us at RRL.
This file doesn't do any math, it just cleans and re-packages the data into a Pandas DataFrame for later use.
"""

import pandas as pd
from X_my_functions import fm_to_d14c

df = pd.read_excel(r'H:\The Science\Datasets\Ansto_intercomparison.xlsx', skiprows=28)

ansto = df.loc[(df['Site'] == 'ANSTO')]                                              # extract ANSTO data
ansto = ansto.rename(columns={"Year of Growth":"Decimal_date", "error":"FM_err"})    # ensure the column is named correctly for later
x = fm_to_d14c(ansto['FM'], ansto['FM_err'], ansto['Decimal_date'])                  # add the D14C column to ANSTO by calculating it using my function
ansto['D14C'] = x[0]                                                                 # add the D14C output
ansto['D14C_err'] = x[1]                                                             # add the D14C_err output
ansto = ansto[['Site','Decimal_date', 'D14C', 'D14C_err','FM','FM_err']]

rrl = df.loc[(df['Site'] == 'RRL')]                                                  # extract RRL
rrl = rrl.rename(columns={"Year of Growth": "Decimal_date", "error": "FM_err"})      # ensure the column is named correctly for later
rrl = rrl[['Site', 'NZA','R','Job', 'Decimal_date', 'D14C', 'D14C_err','FM','FM_err']]

combine = pd.merge(rrl, ansto, how='outer')






