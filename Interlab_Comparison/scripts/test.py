"""
Purpose:

We have two long-term record of 14C02 from the Southern Hemisphere (among some other shorter ones).
One is the Baring Head Record, from the GNS Rafter Radiocarbon Lab (measured by gas counting, then AMS)
Next is Ingeborg Levin and Sam Hammer's Tasmania Cape Grim CO2 record (measured by gas counting).
This script is meant to compare the differences between the datasets over time, to determine if
temporally consistent offsets exist, and if so, how to best correct them to create a harmonized background reference
dataset for future carbon cycle studies.

The script first imports and cleans the data, before using a CCGCRV Curve smoothing program to smooth through the data.
There is precedent for this procedure in the scientific literature following
https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1029/JD094iD06p08549 (Thoning et al., 1989): use of the CCGCRV
https://acp.copernicus.org/articles/17/14771/2017/ (Turnbull et al., 2017): use of CCGCRV in the Baring Head Record
https://gml.noaa.gov/ccgg/mbl/crvfit/crvfit.html: NOAA details about the CCGCRV curve smoothing.

A Monte Carlo simulation is used to determine errors on the CCGCRV smoothing data. These errors are important because
we will need them for comparison with other carbon cycle datasets, of course.

The file outputs a text file with the t-test results. However, it will keep adding to the file, so if you want a fresh
one, delete the remaining text file from the directory.
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend
from Pre_Processing_Heidelberg import combine_heidelberg
from scipy import stats

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

heidelberg = pd.read_excel(r'H:\Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)  # import heidelberg data
baringhead = pd.read_excel(r'H:\Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data
df2_dates = pd.read_excel(r'H:\Science\Datasets\BHD_MeasurementDates.xlsx')  # CO2 measure date
extraction_dates = pd.read_excel(r'H:\Science\Datasets\BHDFlasks_WithExtractionDates.xlsx')  # CO2 extract date

""" TIDY UP THE DATA FILES"""
""" 
Some of the "Date formatting" can be quite tricky. The first step in cleaning the data is to convert
long-format dates to decimal dates that can be used in the CCGCRV curve smoothing algorithm. This is done using a 
function I wrote and lives in my_functions.py.
"""
heidelberg = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'CGO')]
baringhead = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'BHD')]

print(len(heidelberg))
print(min(heidelberg['Decimal_date']))
print(max(heidelberg['Decimal_date']))
step_size_heid = len(heidelberg) / ((max(heidelberg['Decimal_date'])) - (min(heidelberg['Decimal_date'])))
step_size_bhd =  len(baringhead) / ((max(baringhead['Decimal_date'])) - (min(baringhead['Decimal_date'])))
print(step_size_heid)
print(step_size_bhd)

