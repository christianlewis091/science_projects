"""
How many wheels have we measured over time?
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r'I:\C14Data\C14_blank_corrections_NEW\import_from_RLIMS\historical_data\TW3510standards.xlsx')
df = df[['TW', 'Date Run']]
df['Date Run'] = pd.to_datetime(df['Date Run'])

df = df.drop_duplicates(subset='TW')

# # I only want data after I arrived:
AZ_ME = df.loc[(df['Date Run'] > '2022-05-28') | (df['Date Run'] < '2022-09-01')]
ME_HY = df.loc[(df['Date Run'] > '2022-09-01') | (df['Date Run'] < '2023-09-01')]
ME_KS = df.loc[(df['Date Run'] > '2023-09-01') | (df['Date Run'] < '2024-05-10')]

print(f'Albert and I measured {len(AZ_ME)} wheels over 4 months, Hayden and I {len(ME_HY)} over 1 year, and KS and I {len(ME_KS)} over 9 months')




