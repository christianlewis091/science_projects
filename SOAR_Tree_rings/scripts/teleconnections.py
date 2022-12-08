import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from soar_analysis3 import chile_experiment


sam = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/sam.xlsx')
enso = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/enso.xlsx', skiprows=5)

print(enso.columns)
print(sam.columns)

# I'm editing the Chile data so the years in SAM and ENSO index appear in the same format as the Decimal Date
#
chile_experiment['Date_Truncated'] = chile_experiment['Decimal_date']

resultarray = []
for i in range(0, len(chile_experiment)):
    currentrow = chile_experiment.iloc[i]  # grab first row
    dates = str(currentrow['Date_Truncated'])
    date_trunc = int(dates[0:4])
    resultarray.append(date_trunc)

chile_experiment['YEAR'] = resultarray

merged = pd.merge(chile_experiment, sam, how='outer', on='YEAR')  # merge the files back together
merged.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/blahblah.xlsx')
# merged = merged.loc[merged['Site'] == 'Raul Marin Balmaceda']


fig = plt.figure(4, figsize=(7.5, 7.5))
gs = gridspec.GridSpec(9, 2)
gs.update(wspace=.15, hspace=6)

# make first plot
xtr_subsplot = fig.add_subplot(gs[0:3, 0:2])
plt.bar(enso['YEAR'], enso['DJ'])
plt.title('ENSO Index (December/January only)')
plt.xlim(1980, 2022)

xtr_subsplot = fig.add_subplot(gs[3:6, 0:2])
plt.bar(sam['YEAR'], sam['JAN'])
plt.title('Sam Index (January only)')
plt.xlim(1980, 2022)

xtr_subsplot = fig.add_subplot(gs[6:9, 0:2])
plt.scatter(merged['r2_diff_trend'], merged['JAN'])

# plt.show()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/teleconnections.png',
            dpi=300, bbox_inches="tight")
plt.close()


plt.scatter(merged['r2_diff_trend'], merged['NOV'])
plt.xlabel('DD14C')
plt.ylabel('SAM Index')
plt.show()






