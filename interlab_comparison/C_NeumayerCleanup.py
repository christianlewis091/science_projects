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
from A_heidelberg_intercomparison import offset1, offset2, offset3, offset4, offset5, offset6
from A_heidelberg_intercomparison import error1, error2, error3, error4, error5, error6
from X_my_functions import monte_carlo_randomization_trend
from A_heidelberg_intercomparison import cutoff, n
from scipy import stats

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

neumayer = pd.read_excel(r'H:\The Science\Datasets\heidelberg_neumayer.xlsx', skiprows=40)  # import heidelberg data
neumayer = neumayer.dropna(subset=['D14C']).reset_index(drop=True)
print(neumayer)
print(neumayer.columns)
print(len(neumayer))

# This file contains data from 1983 to 2021.


x_init = neumayer['Average']  # extract x-values from heidelberg dataset
x_init = long_date_to_decimal_date(x_init)  # convert the x-values to a decimal date
neumayer['Decimal_date'] = x_init  # add these decimal dates onto the dataframe
# print(len(neumayer))

"""
Break up the Neumayer dataset into the same time-periods that I used for the Heidelberg Intercomparison and offset
calculation:
Any data prior to 1986 (the minimum X value in the Heidelberg dataset) gets 0 offset correction.

"""

h0 = neumayer.loc[(neumayer['Decimal_date'] < 1986)].reset_index() # there is some data before the CGO dataset begins, I cannot correct for these because it is outside the bounds of my intercomparison (1986 - 1991 is first interval)
h1 = neumayer.loc[(neumayer['Decimal_date'] > 1986) & (neumayer['Decimal_date'] < 1991)].reset_index()
h2 = neumayer.loc[(neumayer['Decimal_date'] > 1991) & (neumayer['Decimal_date'] < 1994)].reset_index()
h3 = neumayer.loc[(neumayer['Decimal_date'] > 1994) & (neumayer['Decimal_date'] < 2006)].reset_index()
h4 = neumayer.loc[(neumayer['Decimal_date'] > 2006) & (neumayer['Decimal_date'] < 2009)].reset_index()
h5 = neumayer.loc[(neumayer['Decimal_date'] > 2009) & (neumayer['Decimal_date'] < 2012)].reset_index()
h6 = neumayer.loc[(neumayer['Decimal_date'] > 2012)].reset_index()  # allow all data after 2012, if I chop off at 2016, and there is some data removed. Here it is in POST-AMS range.

h0['D14C_1'] = h0['D14C'] + offset1  # apply the 1986 - 1991 offset to data before 1986, as this is the PRE-AMS range.
h1['D14C_1'] = h1['D14C'] + offset1
h2['D14C_1'] = h2['D14C'] + offset2
h3['D14C_1'] = h3['D14C'] + offset3
h4['D14C_1'] = h4['D14C'] + offset4
h5['D14C_1'] = h5['D14C'] + offset5
h6['D14C_1'] = h6['D14C'] + offset6
h0['weightedstderr_D14C_1'] = np.sqrt(h0['weightedstderr_D14C']**2 + error1**2)
h1['weightedstderr_D14C_1'] = np.sqrt(h1['weightedstderr_D14C']**2 + error1**2)  # propagate the error and REPLACE original
h2['weightedstderr_D14C_1'] = np.sqrt(h2['weightedstderr_D14C']**2 + error2**2)
h3['weightedstderr_D14C_1'] = np.sqrt(h3['weightedstderr_D14C']**2 + error3**2)
h4['weightedstderr_D14C_1'] = np.sqrt(h4['weightedstderr_D14C']**2 + error4**2)
h5['weightedstderr_D14C_1'] = np.sqrt(h5['weightedstderr_D14C']**2 + error5**2)
h6['weightedstderr_D14C_1'] = np.sqrt(h6['weightedstderr_D14C']**2 + error6**2)

neu = pd.merge(h0, h1, how='outer')
neu = pd.merge(neu, h2, how='outer')
neu = pd.merge(neu, h3, how='outer')
neu = pd.merge(neu, h4, how='outer')
neu = pd.merge(neu, h5, how='outer')
neu = pd.merge(neu, h6, how='outer')

print(len(neu))

y = [offset1, offset1, offset1, offset3, offset3, offset3, offset4, offset4, offset4, offset6, offset6, offset6]  # pulled from A_heidelberg Intercomparison.
y_err = [error1, error1, error1, error3, error3, error3, error4, error4, error4, error6, error6, error6]
x =[min(neu['Decimal_date']), (1986 + 1991)/2, 1992, 1994, (1994 + 2005)/2, 2005, 2006, (2006 + 2009)/2, 2009, 2012, (2012 + 2016)/2, max(neu['Decimal_date'])]  # find the middle of each time- chunk.

dff = pd.DataFrame({"offset_xs": x, "offset_ys": y, "offset_errs": y_err})  # my function works best when data are pulled from pandas DF

offset_smoothed = monte_carlo_randomization_trend(dff['offset_xs'], neu['Decimal_date'], dff['offset_ys'], dff['offset_errs'], cutoff, n)  # use the offset values to create an offset smoothing curve
offset_smoothed_summary = offset_smoothed[2]  # extract summary file
offset_smoothed_mean = offset_smoothed_summary['Means']  # grab means
offset_smoothed_stdevs = offset_smoothed_summary['stdevs']  # grab stdevs
neu['smoothed_offset'] = offset_smoothed_mean  # deposit the number for the smoothed offset in the excel sheet
neu['D14C_2'] = neu['D14C'] + neu['smoothed_offset']  # add it to the original data (correct the offset)
neu['smoothed_offset_error'] = offset_smoothed_stdevs
neu['weightedstderr_D14C_2'] = np.sqrt(neu['weightedstderr_D14C']**2 + offset_smoothed_stdevs**2)
# is there a meaningful difference between the smoothed offset and the Pre and Post offset?
pairedtest = stats.ttest_rel(neu['D14C_1'], neu['D14C_2'])  # paired t test between the two offset-type calculations
print(pairedtest)

neu.to_excel('Neumayer_offset.xlsx')


