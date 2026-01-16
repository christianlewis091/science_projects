"""
I need to figure out which oxalics to remove from TW3585 and I freaking can't view them in CALAMS properly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3585\test.xlsx")
stds = [0,5,10,15,20,25,30, 35]
df = df.loc[df['position'].isin(stds)]
df.to_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3585\TW3585_p1_2_3_stds.csv")

# df['mode5'] = (df['14Ccnts']*df['12Ccurr'])/(df['13Ccurr']**2)
# df['poisson_err'] = 1/np.sqrt(df['14Ccnts'])


# pos = np.unique(df['position'])
#
# for i in range(0, len(pos)):
#     subset = df.loc[df['position'] == pos[i]]
#
#     # fig, axs = plt.subplots(2, 1, figsize=(6, 8))  # 3 rows, 1 column
#
#     plt.errorbar(subset['run'],subset['mode5'] , yerr=subset['poisson_err'], color='black', linestyle='', label = f'{pos[i]}', marker='o')
#     plt.legend()
#     plt.axhline(y=np.mean(subset['mode5']), linestyle='--', linewidth=1)
#
#     plt.tight_layout()
#     plt.show()
#     # plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_3_2025_output/blanks/{name[i]}.png',
#     #             dpi=300, bbox_inches="tight")
#     plt.close()

