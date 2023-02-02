import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# df = pd.read_excel(r'H:\Science\Datasets\All_Basins_Data_Merged_Hansell_2022.xlsx', skiprows=1)
#
# doc = df.loc[df['DELTA14C-DOC'] != -999]
#
# doc.to_excel('H:/Science/Datasets/HansellData_DOC14_only.xlsx')

doc = pd.read_excel(r'H:\Science\Datasets\HansellData_DOC14_only.xlsx')
print(len(doc))

plt.xlabel('Latitude')
plt.ylabel('Depth (CTD Pressure)')

doc = doc.loc[(doc['CTD PRESSURE'] > -998) & (doc['LATITUDE'] > -998)]
plt.scatter(doc['LATITUDE'], doc['CTD PRESSURE'], c=doc['DELTA14C-DOC'], cmap='magma')
plt.colorbar(), plt.ylim(max(doc['CTD PRESSURE']), min(doc['CTD PRESSURE']))
plt.show()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Supp1.png', dpi=95, bbox_inches="tight")