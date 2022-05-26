# TODO:  ADD / TEST AN ALREADY CODED T_TEST to SIMPLIFY MY LIFE AND HELP PROVIDE CONFIDENCE. FINISH FIXING MY_FINCTIONS FILE.
# from __future__ import print_function, division
import numpy as np
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import seaborn as sns
from miller_curve_algorithm import ccgFilter
from PyAstronomy import pyasl
from datetime import datetime
from my_functions import long_date_to_decimal_date
from my_functions import monte_carlo_randomization_smooth
from my_functions import monte_carlo_randomization_trend


heidelberg = pd.read_excel(r'H:\The Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)  # import heidelberg data
baringhead = pd.read_excel(r'H:\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data
df2_dates = pd.read_excel(r'H:\The Science\Datasets\BHD_MeasurementDates.xlsx')  # CO2 measure date
extraction_dates = pd.read_excel(r'H:\The Science\Datasets\BHDFlasks_WithExtractionDates.xlsx') # CO2 extract date

""" TIDY UP THE DATA FILES"""
""" 
Some of the "Date formatting" can be quite tricky. The first step in cleaning the data is to convert
long-format dates to decimal dates that can be used in the CCGCRV curve smoothing algorithm. This is done using a 
function I wrote and lives in my_functions.py.
"""
x_init_heid = heidelberg['Average pf Start-date and enddate']  # extract x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)           # convert the x-values to a decimal date
heidelberg['Decimal_date'] = x_init_heid                       # add these decimal dates onto the dataframe
heidelberg = heidelberg.dropna(subset=['D14C'])                # drop NaN's in the column I'm most interested in
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]         # Filtering out an outlier around 2019
heidelberg.reset_index()                                       # reset the index to avoid heaps of gnarly errors
baringhead = baringhead.dropna(subset=['DELTA14C'])            # drop NaN's in the column I'm most interested in

print(min(x_init_heid))





