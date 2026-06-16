"""
having a look at some data
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3562/COMBINED.csv", skiprows=3)
print(df)
df['m5'] = (df['14Ccnts']*df['12Ccurr'])/(df['13Ccurr']*df['13Ccurr'])

p0 = df.loc[df['position']  == 0]
p7 = df.loc[df['position']  == 7]
p14 = df.loc[df['position']  == 14]
p21 = df.loc[df['position']  == 21]
p28 = df.loc[df['position']  == 28]
p35 = df.loc[df['position']  == 35]

plt.plot(p0['13Ccurr'], p0['m5'], marker='o', label='0')
plt.plot(p7['13Ccurr'], p7['m5'], marker='o', label='7')
plt.plot(p14['13Ccurr'], p14['m5'], marker='o', label='14')
plt.plot(p21['13Ccurr'], p21['m5'], marker='o', label='21')
plt.plot(p28['13Ccurr'], p28['m5'], marker='o', label='28')
plt.plot(p35['13Ccurr'], p35['m5'], marker='o', label='35')

plt.legend()
plt.show()