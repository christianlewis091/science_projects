import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


df = pd.read_csv('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3553/TW3553_p4.csv')
df2 = pd.read_excel('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3553/mgC_data.xlsx')

df = df.merge(df2, on='TP#')


pos = np.unique(df['position'])
for i in range(0, len(pos)):
    df_i = df.loc[df['position'] == i].reset_index(drop=True)
    mgC = df_i['wtgraph']
    mgC = mgC[0]
    plt.plot(df_i['run'], df_i['12CLEcurr'])
    plt.scatter(df_i['run'], df_i['12CLEcurr'])
    plt.ylim(0, 120)
    plt.title(f'{mgC}')
plt.show()