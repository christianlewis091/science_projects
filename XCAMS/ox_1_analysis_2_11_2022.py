import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt


df = pd.read_excel('H:/Science/Current_Projects/04_ams_data_quality/OX1_analyses/oxs_as_of_1_11_2022.xlsx')
df = df[['Ratio to standard', 'Date Run','TW']].dropna(subset='Ratio to standard')
df = df.loc[df['TW'] > 3360]
tws = np.unique(df['TW'])

arr = []
tw = []
for i in range(0, len(tws)):
    x = int(tws[i])
    wheel = df.loc[df['TW'] == int(tws[i])]
    std = np.std(wheel['Ratio to standard'])
    arr.append(std*1000)  # expressed as per mil
    tw.append(x)

x = pd.DataFrame({"TW":tw, "Ratio to standard": arr})
x = x.loc[x['Ratio to standard'] < 3]

plt.scatter(x['TW'], x['Ratio to standard'])
plt.title('Variability of OX-1 STD over time; red line = TW3460')


plt.xlabel('TW Wheel Number')
plt.ylabel('OX-1 Variability (\u2030)')

font = {'color':  'black', 'weight': 'normal', 'size': 12}
plt.text(3360, 1.3, 'Mean', fontdict=font)
plt.axhline(y=np.mean(x['Ratio to standard']), color="black", linestyle="--")

font = {'color':  'darkred', 'weight': 'normal', 'size': 12}
plt.axhline(y=(np.std([.99955, 1.00157, 1.00127, .99802, .99958, 1.00014])*1000), color="darkred", linestyle="-")
plt.text(3360, 1.0, '3460', fontdict=font)

plt.savefig('H:/Science/Current_Projects/04_ams_data_quality/OX1_analyses/oxs.png',
            dpi=300, bbox_inches="tight")


