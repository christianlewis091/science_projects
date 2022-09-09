from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_UniMagallanes import combine_Magallanes
from Pre_Processing_SIO_LLNL import combine_SIO
from X_my_functions import intercomparison_ttest, monte_carlo_randomization_trend, long_date_to_decimal_date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']

"""
This file uses PRE-CLEANED data from the following institutions, 
and compares them to RRL using the specified type of data:
ANSTO: Tree Rings
SIO/LLNL: Standard Materials NWT3 and NWT4
University of Magallanes: Tree Rings
University of Heidelberg: Atmospheric CO2 measurements. 
The null hypothesis for the following t-tests is: "There is NO systematic bias between institutions". If p-values 
come out less than 0.01, or 1%, or 98% confidence interval, I call that they are significantly different. 

FOR INTERCOMPARISONS, USE FM WHERE POSSIBLE

All data visualizations will appear in another .py file. 

First I'm going to just index the data I need for the t-tests for ANSTO, SIO/LLNL (NWT3 and NWT4) and Magallanes. 
"""

ansto = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'ANSTO')].reset_index(drop=True)
rrl = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'RRL')].reset_index(drop=True)


NWT3 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT3')]
sio_nwt3 = NWT3.loc[(NWT3['Site'] == 'LLNL')]
rrl_nwt3 = NWT3.loc[(NWT3['Site'] == 'RRL')]
NWT4 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT4')]
sio_nwt4 = NWT4.loc[(NWT4['Site'] == 'LLNL')]
rrl_nwt4 = NWT4.loc[(NWT4['Site'] == 'RRL')]

y1 = sio_nwt3['D14C']
y1_average = np.average(y1)
y1_1sigma = np.std(y1)

y2 = sio_nwt4['D14C']
y2_average = np.average(y2)
y2_1sigma = np.std(y2)

y3 = rrl_nwt3['D14C']
y3_average = np.average(y3)
y3_1sigma = np.std(y3)

y4 = rrl_nwt4['D14C']
y4_average = np.average(y4)
y4_1sigma = np.std(y4)

y1_fm = sio_nwt3['FM']
y1_average_fm = np.average(y1_fm)
y1_1sigma_fm = np.std(y1_fm)

y2_fm = sio_nwt4['FM']
y2_average_fm = np.average(y2_fm)
y2_1sigma_fm = np.std(y2_fm)

y3_fm = rrl_nwt3['FM']
y3_average_fm = np.average(y3_fm)
y3_1sigma_fm = np.std(y3_fm)

y4_fm = rrl_nwt4['FM']
y4_average_fm = np.average(y4_fm)
y4_1sigma_fm = np.std(y4_fm)


# UNCOMMENT WHEN DONE WRITING THIS FILE! HERE ARE THE OTHER INTERCOMPARISON!
# I was first supplied with FM data from ANSTO so I'm going to use FM for this calculation.
a = intercomparison_ttest(rrl['D14C'], ansto['D14C'], 'ANSTO v RRL Test: Tree Rings, D14C', 'paired')
b = intercomparison_ttest(rrl['FM'], ansto['FM'], 'ANSTO v RRL Test: Tree Rings, FM', 'paired')

# I'll do this one in FM as well because it minimizes the amount of extra calculatinos
# that can lead to fake systematic bias.
c = intercomparison_ttest(rrl_nwt3['FM'], sio_nwt3['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison (FM)', 'not-paired')
d = intercomparison_ttest(rrl_nwt4['FM'], sio_nwt4['FM'], 'SIO/LLNL v RRL, NWT4 Intercomparison (FM)', 'not-paired')
e = intercomparison_ttest(rrl_nwt3['D14C'], sio_nwt3['D14C'], 'SIO/LLNL v RRL, NWT3 Intercomparison (D14C)', 'not-paired')
f = intercomparison_ttest(rrl_nwt4['D14C'], sio_nwt4['D14C'], 'SIO/LLNL v RRL, NWT4 Intercomparison (D14C', 'not-paired')

# TODO deal with the multiple records from the same year
e = intercomparison_ttest(combine_Magallanes['D14C_x'], combine_Magallanes['D14C_y'], 'Magallanes v RRL Test: Tree Rings (D14C)', 'paired')
e = intercomparison_ttest(combine_Magallanes['FM_x'], combine_Magallanes['FM_y'], 'Magallanes v RRL Test: Tree Rings (FM)', 'paired')

# <editor-fold desc="Flask v NaOH Method Intercomparison">
"""
Shown below are intercomparisons between GNS internally:
Method Intercomparison: NaOH v Flask for CO2 measurements. 

An initial method intercomparison from my remote work shows that there is a difference between the two groups. I'm going to
expand this analysis the entire dataset I have on hand of BHD and see if there is a difference...
"""
# I'm adding in some extra intercomparisons from GNS,
# Cape Grim vs BHD intercomparison
# NaOH v Flask Intercomparison.

"""
This two lines below show the initial intercomparison. 
"""

flaskvn = pd.read_excel(r'H:\Science\Datasets\FlaskvNaOH.xlsx', skiprows=3).dropna(subset = 'D14C_flask')  # import heidelberg data
f = intercomparison_ttest(flaskvn['D14C_flask'], flaskvn['D14C_NaOH'], 'Flask v NaOH @ Baring Head', 'paired')

"""
Updated intercomparison
"""
bhd = pd.read_excel(r'H:\Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data
bhd = bhd.loc[(bhd['DELTA14C_ERR'] > 0)]                                          # filter out all data where the errors are less than zero
bhd1 = bhd.loc[(bhd['DEC_DECAY_CORR'] > 1984) & (bhd['DEC_DECAY_CORR'] < 1993)]   # grab only data that is between 1984 and 1993
bhd2 = bhd.loc[(bhd['DEC_DECAY_CORR'] > 2012)]                                    # then grab data that is after 2012 (we're removing the intermediate period)

naoh1 = bhd1.loc[(bhd1['METH_COLL'] == 'NaOH_static')]
flask1 = bhd1.loc[(bhd1['METH_COLL'] == 'Whole_air')]
naoh2 = bhd2.loc[(bhd2['METH_COLL'] == 'NaOH_static')]
flask2 = bhd2.loc[(bhd2['METH_COLL'] == 'Whole_air')]

n = 10
fake_x1 = np.linspace(min(flask1['DEC_DECAY_CORR']), max(naoh1['DEC_DECAY_CORR']), len(bhd['DEC_DECAY_CORR']))  # create arbitrary set of x-values to control output
fake_x2 = np.linspace(min(flask2['DEC_DECAY_CORR']), max(flask2['DEC_DECAY_CORR']), len(bhd['DEC_DECAY_CORR']))  # create arbitrary set of x-values to control output
trend_naoh1 = monte_carlo_randomization_trend(naoh1['DEC_DECAY_CORR'], fake_x1, naoh1['DELTA14C'], naoh1['DELTA14C_ERR'], 667, n)
trend_naoh2 = monte_carlo_randomization_trend(naoh2['DEC_DECAY_CORR'], fake_x2, naoh2['DELTA14C'], naoh2['DELTA14C_ERR'], 667, n)
trend_flask1 = monte_carlo_randomization_trend(flask1['DEC_DECAY_CORR'], fake_x1, flask1['DELTA14C'], flask1['DELTA14C_ERR'], 667, n)
trend_flask2 = monte_carlo_randomization_trend(flask2['DEC_DECAY_CORR'], fake_x2, flask2['DELTA14C'], flask2['DELTA14C_ERR'], 667, n)

naoh_summary = trend_naoh1[2]
naoh_means1 = naoh_summary['Means']
naoh_summary = trend_naoh2[2]
naoh_means2 = naoh_summary['Means']
flask_summary = trend_flask1[2]
flask_means1 = flask_summary['Means']
flask_summary = trend_flask2[2]
flask_means2 = flask_summary['Means']

f = intercomparison_ttest(naoh_means1, flask_means1, 'Flask v NaOH @ Baring Head, Trended, Part1', 'paired')
f = intercomparison_ttest(naoh_means2, flask_means2, 'Flask v NaOH @ Baring Head, Trended, Part2', 'paired')
# </editor-fold>

# <editor-fold desc="Extraction Dates">
"""
Very very frustrating issues with date formatting when trying to deal with the extraction date data. Will come back to this at future time. 
"""
"""
Does the extraction date impact the data ?
"""
ed = pd.read_excel(r'H:\Science\Datasets\Extraction_Dates.xlsx')  # import Baring Head data
bhd = pd.read_excel(r'H:\Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data
ed = ed.dropna(subset=['NZ'])
ed = ed.dropna(subset=['Extract'])
#
#
combined = pd.merge(bhd, ed, on = 'NZ')
# combined.to_excel('test.xlsx')
x = combined['Extract']
x = long_date_to_decimal_date(x)

combined['Extraction Date Difference'] = x - combined['DEC_DECAY_CORR']

# combined.to_excel('test.xlsx')

## combined['Extract'] = long_date_to_decimal_date(combined['Extract'])

# #
# naoh = combined.loc[(combined['METH_COLL'] == 'NaOH_static')]
# flask = combined.loc[(combined['METH_COLL'] == 'Whole_air')]
#
# mtarray = []
# for i in range(0, len(naoh)):
#     row1 = naoh.iloc[i]
#
#     for k in range(0, len(flask)):
#         row2 = flask.iloc[k]
#
#         if row1['DATE_ST_asnum'] < row2['DATE_COLLasnum'] < row1['DATE_END_asnum']:
#             mtarray.append(row1)
#             mtarray.append(row2)
#
# mtarray = pd.DataFrame(mtarray)
# mtarray.to_excel('test2.xlsx')
#
# </editor-fold>

