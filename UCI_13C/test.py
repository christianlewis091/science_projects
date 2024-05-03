import numpy as np
import pandas as pd

df = pd.read_excel(r'H:\Science\Papers\In Prep Work\2023_Lewis_13C\9_GRL_Accepted_PROOFS\Notes_on_Uncertainty_calcs.xlsx')

# calculate the PER-SUBSET DIFFERENCE between Spe and total
df['diff'] = df['spe13C'] - df['doc13C']
df['diff_unc2'] = df['DOC_u']**2 + df['SPE_u']**2

total = df.loc[df['Cruise'] == 'Total']
subs = df.loc[df['Cruise'] != 'Total']

total_unc_fin = float(np.sqrt(total['diff_unc2']))
subs_unc_fin = np.sqrt(sum(subs['diff_unc2']))

print(f'The total propogated uncertainty when I take the difference of the two datasets as a whole is: {total_unc_fin}')
print(f'The total propogated uncertainty when looking at each subset (cruise, depth) and then mergeing the uncertainties is: {subs_unc_fin}')