import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit4.xlsx", sheet_name='Clean Dataset')

# df = df.loc[df['TW'] <3553 ]
# # how many samples are <0.3 for each group? 
# results = []

# for r in np.unique(df['Job::R']):
#     dfr = df[df['Job::R'] == r]

#     n_lt_03 = (dfr['wtgraph'] < 0.3).sum()
#     n_gt_03 = (dfr['wtgraph'] >= 0.3).sum()

#     results.append({
#         'Job::R': r,
#         'n_wtgraph_lt_0.3': n_lt_03,
#         'n_wtgraph_gt_0.3': n_gt_03
#     })

# summary_df = pd.DataFrame(results)

# print(summary_df)

"""
Water Blanks before and after ?
"""

df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit4.xlsx", sheet_name='Clean Dataset')

# # we're interested in 14047/11
# df = df.loc[df['Job::R'] == '14047/11']
# dfb4 = df.loc[df['TP'] < 87423]
# dfa = df.loc[df['TP'] >= 87423]

# plt.scatter(dfb4['TP'], dfb4['F_corrected_normed'])
# plt.scatter(dfa['TP'], dfa['F_corrected_normed'])

# a = np.mean(dfb4['F_corrected_normed'])
# aa = np.std(dfb4['F_corrected_normed'])
# print(len(dfb4['F_corrected_normed']))
# b = np.mean(dfa['F_corrected_normed'])
# bb = np.std(dfa['F_corrected_normed'])
# print(len(dfa['F_corrected_normed']))
# acra = -8033*np.log(a)
# bcra = -8033*np.log(b)
# plt.close()

# print(f'The mean before extra cleaning was {a:.4f}_{aa:.4f}, and the mean after was {b:.4f}_{bb:.4f},')
# print(f'The mean before extra cleaning was {acra:.0f}, and the mean after was {bcra:.0f}')


"""
Quick plkot
"""
cell = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='CELL')].copy()
aaa = df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA')].copy()

plt.scatter(aaa['TP'], aaa['F_corrected_normed'])
plt.scatter(cell['TP'], cell['F_corrected_normed'])
plt.show()