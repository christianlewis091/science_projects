import pandas as pd
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_excel('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3450-3499\TW3491/cathode_drop.xlsx')
tw3490 = df.loc[df['TW'] == 'TW3490_p1']
tw3490_2 = df.loc[df['TW'] == 'TW3490_p2']
tw3491 = df.loc[df['TW'] == 'TW3491_p1']
pos = df.loc[df['TW'] == 'TW3491_p1']
pos = pos.loc[(pos['position'] >32) | (pos['position'] < 3)]

print(len(pos))
plt.scatter(tw3490['run'], tw3490['12Ccurr'], marker='o', label='TW3490_1', color='black')
plt.scatter(tw3490_2['run'], tw3490_2['12Ccurr'], marker='s', label='TW3490_2', color='gray', alpha=1)
plt.scatter(tw3491['run'], tw3491['12Ccurr'], marker='D', label='TW3491_1', color='blue')
plt.scatter(pos['run'], pos['12Ccurr'], marker='s', label='TW3491_1_suspectcats', color='red')
plt.ylabel('12C current')
plt.xlim(0, 300)
plt.xlabel('Run #')
plt.legend()
plt.show()
# df = df.loc[df['R_number'] == '14047/1']
# df = df.loc[df['TW'] > (3490-300)]
#
# plt.errorbar(df['TW'], df['Ratio to standard'], yerr = df['Ratio to standard error'])
# plt.scatter(df['TW'], df['Ratio to standard'])
#
# plt.title('14047/1, TW3190-TW3490')
# plt.xlabel('TW')
# plt.ylabel('RTS')
plt.savefig('I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3450-3499\TW3491/cathode_drop.png',
            dpi=300, bbox_inches="tight")
# #
# #
#
#
