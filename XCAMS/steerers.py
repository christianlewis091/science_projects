import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from scipy.stats import chisquare

df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\steerers.xlsx')
esx1_0 = df['esx1'] / df['esx0']
esx2_0 = df['esx2'] / df['esx0']

esy1_0 = df['esy1'] / df['esy0']
esy2_0 = df['esy2'] / df['esy0']

plt.scatter(df['TW'], esx1_0)
plt.scatter(df['TW'], esx2_0)
plt.show()
plt.close()

plt.scatter(df['TW'], esy1_0)
plt.scatter(df['TW'], esy2_0)
plt.show()
plt.close()