"""
I'll use this file to remove all data besides the OX-1's to see them more clearly in CALAMS
"""

import pandas as pd
import warnings
import numpy as np
warnings.filterwarnings("ignore")

df = pd.read_excel("I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3450-3499/TW3460/TW_3460_1.xlsx", skiprows=3)
df = df.loc[(df['position'] == 11) | (df['position'] == 15)| (df['position'] == 19) | (df['position'] == 23)| (df['position'] == 27) | (df['position'] == 31)]
df.to_excel("I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3450-3499/TW3460/TW_3460_1_out.xlsx")