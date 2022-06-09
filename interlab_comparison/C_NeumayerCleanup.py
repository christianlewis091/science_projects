"""
In a previous python file, I find the interlaboratory offsets between Uni Heidelberg and RRL through time.
I am now going to apply these calculated offsets to the remaining Southern Hemisphere data from Uni Heidelberg,
which is the Neumayer dataset.

"""

import matplotlib as mpl
import pandas as pd
import seaborn as sns

# general plot parameters
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

neumayer = pd.read_excel(r'H:\The Science\Datasets\heidelberg_neumayer.xlsx', skiprows=40)  # import heidelberg data
# This file contains data from 1983 to 2021.












