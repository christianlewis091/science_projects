import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date

colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

""" STEP 1: LOAD UP THE DATA"""
southpole = pd.read_excel(r'H:\The Science\Datasets\Graven_etal_2012_SouthPole.xlsx')
Palmerstation = pd.read_excel(r'H:\The Science\Datasets\Graven_etal_2012_PalmerStation.xlsx')
ManuaLoa = pd.read_excel(r'H:\The Science\Datasets\Graven_etal_2012_ManuaLoa.xlsx')
KumukahiHawaii = pd.read_excel(r'H:\The Science\Datasets\Graven_etal_2012_KumukahiHawaii.xlsx')
barrow = pd.read_excel(r'H:\The Science\Datasets\Graven_etal_2012_BarrowAlaska.xlsx')
samoa = pd.read_excel(r'H:\The Science\Datasets\Graven_etal_2012_AmericanSamoa.xlsx')

combine = pd.concat([southpole,
                     Palmerstation,
                     ManuaLoa,
                     KumukahiHawaii,
                     barrow,
                     samoa])  # Keeps ALL Data
combine = combine.reset_index(drop=True)

x = combine['Sample Date']  # x-values from heidelberg dataset
x = long_date_to_decimal_date(x)
combine['Decimal_date'] = x  # add these decimal dates onto the dataframe


"""
Here is the output from Pre_Processing_SIO_LLNL.py:

             0          1         2     3
0         LLNL  41.588889  1.104842   9.0
1          RRL  44.306932  0.281048  88.0
2  Both Series  42.947910  2.117606   NaN
             0          1         2     3
0         LLNL -32.840000  0.722157   9.0
1          RRL -30.400116  0.199599  86.0
2  Both Series -31.620058  1.424766   NaN

The final offset for NWT3 is: LLNL is -2.7180429292929347 ± 1.0684976598008669 offset from RRL

The final offset for NWT4 is: LLNL is -2.439883720930233 ± 0.6652241642057785 offset from RRL

The OFFSET FOR LLNL is -2.5789633251115838 ± 1.258654216869433 , which is an average of NWT3 and NWT4 offsets

I'm going to ADD this offset to all Graven's data. 
"""

combine['D14C_offset_corrected'] = combine['Δ14C (‰)'] + 2.58
print(combine.columns)
combine['D14C_offset_corrected_error'] = np.sqrt(combine['σTot (‰)']**2 + 1.26**2)

combine.to_excel('Graven_OffsetCorrections.xlsx')



