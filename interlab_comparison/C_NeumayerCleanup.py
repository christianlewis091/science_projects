"""
In a previous python file, I find the interlaboratory offsets between Uni Heidelberg and RRL through time.
I am now going to apply these calculated offsets to the remaining Southern Hemisphere data from Uni Heidelberg,
which is the Neumayer dataset.

"""
import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date
from B_CGO_BHD_harmonization import offset1, offset2, offset3, offset4, offset5, offset6
from B_CGO_BHD_harmonization import error1, error2, error3, error4, error5, error6

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

neumayer = pd.read_excel(r'H:\The Science\Datasets\heidelberg_neumayer.xlsx', skiprows=40)  # import heidelberg data
print(neumayer.columns)
# This file contains data from 1983 to 2021.
x_init = neumayer['Average']  # extract x-values from heidelberg dataset
x_init = long_date_to_decimal_date(x_init)  # convert the x-values to a decimal date
neumayer['Decimal_date'] = x_init  # add these decimal dates onto the dataframe

"""
Offset the data using the PRE and POST OFFSET 
"""

h0 = neumayer.loc[(neumayer['Decimal_date'] < 1986)].reset_index() # there is some data before the CGO dataset begins, I cannot correct for these because it is outside the bounds of my intercomparison (1986 - 1991 is first interval)
h1 = neumayer.loc[(neumayer['Decimal_date'] > 1986) & (neumayer['Decimal_date'] < 1991)].reset_index()
h2 = neumayer.loc[(neumayer['Decimal_date'] > 1991) & (neumayer['Decimal_date'] < 1994)].reset_index()
h3 = neumayer.loc[(neumayer['Decimal_date'] > 1994) & (neumayer['Decimal_date'] < 2006)].reset_index()
h4 = neumayer.loc[(neumayer['Decimal_date'] > 2006) & (neumayer['Decimal_date'] < 2009)].reset_index()
h5 = neumayer.loc[(neumayer['Decimal_date'] > 2009) & (neumayer['Decimal_date'] < 2012)].reset_index()
h6 = neumayer.loc[(neumayer['Decimal_date'] > 2012) & (neumayer['Decimal_date'] < 2016)].reset_index()

h1['D14C'] = h1['D14C'] + offset1
h2['D14C'] = h2['D14C'] + offset2
h3['D14C'] = h3['D14C'] + offset3
h4['D14C'] = h4['D14C'] + offset4
h5['D14C'] = h5['D14C'] + offset5
h6['D14C'] = h6['D14C'] + offset6
h1['weightedstderr_D14C'] = np.sqrt(h1['weightedstderr_D14C']**2 + error1**2)  # propagate the error and REPLACE original
h2['weightedstderr_D14C'] = np.sqrt(h2['weightedstderr_D14C']**2 + error2**2)
h3['weightedstderr_D14C'] = np.sqrt(h3['weightedstderr_D14C']**2 + error3**2)
h4['weightedstderr_D14C'] = np.sqrt(h4['weightedstderr_D14C']**2 + error4**2)
h5['weightedstderr_D14C'] = np.sqrt(h5['weightedstderr_D14C']**2 + error5**2)
h6['weightedstderr_D14C'] = np.sqrt(h6['weightedstderr_D14C']**2 + error6**2)








