import pandas as pd
import warnings
import numpy as np
warnings.filterwarnings("ignore")

df = pd.read_excel('H:/Science/Current_Projects/04_ams_data_quality/OX1_analyses/oxs_as_of_1_11_2022.xlsx')
df = df[['Ratio to standard', 'Date Run']].dropna(subset='Ratio to standard')
df = df.resample('M').mean()
print(df)
np.linspace(2.0, 3.0, num=5)

# df = df.resample('D', level=0).sum()
#
# df.set_index('index').resample('D').pad().rolling(window=8).mean()