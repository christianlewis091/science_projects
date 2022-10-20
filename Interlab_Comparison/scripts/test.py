"""
"""
import pandas as pd

df = pd.read_excel(r'I:\C14Data\C14_blank_corrections_dev\TW3435.xlsx').reset_index(drop=True)
df_pres = pd.read_excel(r'I:\C14Data\C14_blank_corrections_dev\TW3435_PreTreatments.xlsx').reset_index(drop=True)

merged = pd.merge(df, df_pres, on='Job', how='outer')
print(merged)
merged.to_excel(r'I:\C14Data\C14_blank_corrections_dev\mergetest.xlsx')