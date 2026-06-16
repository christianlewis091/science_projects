import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt

df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\tw3503_1_countsvsize.xlsx')

standards = [0,5,10,15,20,25,30,35]
sizes = [.41,.45,.45,.49,.55,.51,.66,.44]

df_1 = pd.DataFrame()
for i in range(0,len(standards)):
    this_one = df.loc[df['position'] == standards[i]]
    this_one['size'] = sizes[i]
    df_1 = pd.concat([df_1, this_one])
df_1 = df_1.sort_values(by=['size'])

uns = np.unique(df_1['position'])
for i in range(0,len(standards)):
    this_one = df.loc[df['position'] == standards[i]]
    plt.scatter(this_one['run'], this_one['14Ccnts'], label=str(sizes[i]))
plt.legend()
plt.savefig(r'H:\Science\Current_Projects\04_ams_data_quality\countssize.png', dpi=300, bbox_inches="tight")