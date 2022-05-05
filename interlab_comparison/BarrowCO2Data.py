"""
Purpose:
This data was imported from NOAA to test if I can recreate the smooth curve
fits that Jocelyn and Thorning make and then try to recreate it on our data
https://gml.noaa.gov/aftp/data/trace_gases/co2/in-situ/surface/brw/co2_brw_surface-insitu_1_ccgg_MonthlyData.txt
https://gml.noaa.gov/ccgg/mbl/crvfit/

Outcome:
The Miller Smoothing algoritm works.
Mine kind of works but we will not be using it, so it largely obsolete.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
from numpy.fft import fft, ifft
import seaborn as sns
from scipy import optimize
from cbl_curve_fitting_algorithm import cbl_curve_fit
from miller_curve_algorithm import ccgFilter
from my_functions import year_month_todecimaldate
warnings.simplefilter('ignore', np.RankWarning)
# Source:
# IMPORT DATA INTO PYTHON
df = pd.read_csv(r'H:\The Science\Datasets'
                 r'\co2_brw_surface-insitu_1_ccgg_DailyData.csv')

# print(df.columns)  # Shows the column names in imported data
df = df.loc[(df['year'].between(2000, 2011))]  # filter values from 2000-2011
df = df.loc[(df['value'] > 0)]  # filter out all flag values (-1000)
df = df.reset_index()
date = (df['time_decimal'])
co2 = (df['value'])

# call in the curve fitting programs
cbl_smooth = cbl_curve_fit(date, co2)
miller_smooth = ccgFilter(date, co2).getMonthlyMeans()
miller_smooth_x = year_month_todecimaldate(miller_smooth[0], miller_smooth[1])
miller_smooth_y = miller_smooth[2]

plt.plot(date, cbl_smooth, linestyle='solid', marker='', label='CBL Smoothing Algorith', color= 'tab:blue')
plt.plot(miller_smooth_x, miller_smooth_y, linestyle='solid', marker='', label='Miller Smoothing Algorith', color='tab:red')
plt.scatter(date, co2, marker='^', label='CO2 Data Barrow Alaska', color='gray', edgecolors='gray')
plt.legend(fontsize=6)  # add the legend (will default to 'best' location)
plt.legend()
# plt.xlim([2010, 2020])
# plt.ylim([0, 60])
plt.xlabel('Date', fontsize=14)
plt.ylabel('[CO2] ppm', fontsize=14)  # label the y axis

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/BarrowCO2Data_py_result.png',
            dpi=300, bbox_inches="tight")



