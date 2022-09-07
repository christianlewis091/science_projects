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

df = pd.read_excel(r'H:\The Science\Datasets\heidelberg_MQA.xlsx', skiprows=0)
df = df.dropna(subset=['D14C']).reset_index(drop=True)

# This file contains data from 1983 to 2021.

df = pd.read_excel(r'H:\The Science\Datasets\heidelberg_MQA.xlsx', skiprows=0)
x = df['Average of Dates']  # extract x-values from heidelberg dataset
x = long_date_to_decimal_date(x)  # convert the x-values to a decimal date
df['Decimal_date'] = x  # add these decimal dates onto the dataframe
df = df.dropna(subset=['D14C'])  # drop NaN's in the column I'm most interested in

# This dataset goes from 1992 - 2020
# h1 = df.loc[(df['Decimal_date'] > 1986) & (df['Decimal_date'] < 1991)].reset_index()
h2 = df.loc[(df['Decimal_date'] > 1991) & (df['Decimal_date'] < 1994)].reset_index()
h3 = df.loc[(df['Decimal_date'] > 1994) & (df['Decimal_date'] < 2006)].reset_index()
h4 = df.loc[(df['Decimal_date'] > 2006) & (df['Decimal_date'] < 2009)].reset_index()
h5 = df.loc[(df['Decimal_date'] > 2009) & (df['Decimal_date'] < 2012)].reset_index()
h6 = df.loc[(df['Decimal_date'] > 2012)].reset_index()  # allow all data after 2012, if I chop off at 2016, and there is some data removed. Here it is in POST-AMS range.

h2['D14C_1'] = h2['D14C'] + offset2
h3['D14C_1'] = h3['D14C'] + offset3
h4['D14C_1'] = h4['D14C'] + offset4
h5['D14C_1'] = h5['D14C'] + offset5
h6['D14C_1'] = h6['D14C'] + offset6
h2['weightedstderr_D14C_1'] = np.sqrt(h2['1sigma_error']**2 + error2**2)
h3['weightedstderr_D14C_1'] = np.sqrt(h3['1sigma_error']**2 + error3**2)
h4['weightedstderr_D14C_1'] = np.sqrt(h4['1sigma_error']**2 + error4**2)
h5['weightedstderr_D14C_1'] = np.sqrt(h5['1sigma_error']**2 + error5**2)
h6['weightedstderr_D14C_1'] = np.sqrt(h6['1sigma_error']**2 + error6**2)
#
df = pd.merge(h2, h3, how='outer')
df = pd.merge(df, h4, how='outer')
df = pd.merge(df, h5, how='outer')
df = pd.merge(df, h6, how='outer')

y = [offset1, offset1, offset1, offset3, offset3, offset3, offset4, offset4, offset4, offset6, offset6, offset6]  # pulled from A_heidelberg Intercomparison.
y_err = [error1, error1, error1, error3, error3, error3, error4, error4, error4, error6, error6, error6]
x =[min(df['Decimal_date']), (1986 + 1991)/2, 1992, 1994, (1994 + 2005)/2, 2005, 2006, (2006 + 2009)/2, 2009, 2012, (2012 + 2016)/2, max(df['Decimal_date'])]  # find the middle of each time- chunk.

dff = pd.DataFrame({"offset_xs": x, "offset_ys": y, "offset_errs": y_err})  # my function works best when data are pulled from pandas DF

offset_smoothed = monte_carlo_randomization_trend(dff['offset_xs'], df['Decimal_date'], dff['offset_ys'], dff['offset_errs'], cutoff, n)  # use the offset values to create an offset smoothing curve
offset_smoothed_summary = offset_smoothed[2]  # extract summary file
offset_smoothed_mean = offset_smoothed_summary['Means']  # grab means
offset_smoothed_stdevs = offset_smoothed_summary['stdevs']  # grab stdevs
df['smoothed_offset'] = offset_smoothed_mean  # deposit the number for the smoothed offset in the excel sheet
df['D14C_2'] = df['D14C'] + df['smoothed_offset']  # add it to the original data (correct the offset)
df['smoothed_offset_error'] = offset_smoothed_stdevs
df['weightedstderr_D14C_2'] = np.sqrt(df['1sigma_error']**2 + offset_smoothed_stdevs**2)
# is there a meaningful difference between the smoothed offset and the Pre and Post offset?

df = df.rename(columns={"1sigma_error": "D14C_err"})
df = df.rename(columns={"smoothed_offset": "offset2"})
df = df.rename(columns={"smoothed_offset_error": "offset2_err"})
df = df.rename(columns={"weightedstderr_D14C_2": "D14C_2_err"})
df = df.rename(columns={"weightedstderr_D14C_1": "D14C_1_err"})


# Reorder the columns in an order that makes more sense
df = df[['#location', 'Decimal_date', 'D14C', 'D14C_err', 'D14C_1', 'D14C_1_err', 'offset2', 'offset2_err', 'D14C_2', 'D14C_2_err']]
df.to_excel('MCQ_offset.xlsx')

"""
This is the third of three Heidelberg inter-comparison files that I am correcting for these offsets. Now I'm going 
to combine them all into one for clarity
"""
cgo = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\CapeGrim_offset.xlsx')
neu = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\Neumayer_offset.xlsx')

all_offset_corrected_heid = pd.merge(cgo, df, how='outer')  # combine cape grim and MCQ first
all_offset_corrected_heid = pd.merge(all_offset_corrected_heid, neu, how='outer')   # tack on neumayer

all_offset_corrected_heid = all_offset_corrected_heid[['#location', 'Decimal_date','D14C','D14C_err','D14C_1','D14C_1_err','D14C_2','D14C_2_err']]
all_offset_corrected_heid.to_excel('Heidelberg_OffsetCorrections.xlsx')













