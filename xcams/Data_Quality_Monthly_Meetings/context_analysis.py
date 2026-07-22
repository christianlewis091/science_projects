# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

# df = pd.read_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\context_analysis2.xlsx")

# stands_HP = [0,5,10,15,20,25,30,35]
# stands_RP = [0,7,14,21,28,35]
# wack = [0,2,3,5,6,8,9,11,12]

# tws = np.unique(df['TW_full'])

# retunes = ['3600_1', '3613_1','3615_1', '3617_1','3622_1','3623_1', '3623_2', '3624_1','3627_1','3629_1','3629_2']

# for i in range(0, len(tws)):

#     fig, axs = plt.subplots(4, 1, figsize=(8, 8))

#     # grab first wheel
#     subdf_i = df.loc[df['TW_full'] == tws[i]]

#     # whats precision: 
#     precision = subdf_i['Pres'].iloc[0]

#     if precision == 'HP': 
#         subdf_i = subdf_i.loc[subdf_i['DMANitem'].isin(stands_HP)]
#     elif precision == 'WACK': 
#         subdf_i = subdf_i.loc[subdf_i['DMANitem'].isin(wack)]
#     else:
#         subdf_i = subdf_i.loc[subdf_i['DMANitem'].isin(stands_RP)]

#     # grab individual cathodes: 
#     targets = np.unique(subdf_i['DMANitem'])

#     for j in range(0, len(targets)):
#         t_j = subdf_i.loc[subdf_i['DMANitem']==targets[j]]
#         t_j = t_j.dropna(subset='12CLE')
#         t_j = t_j.sort_values(by='12CLE')

#         # grab first 
#         t_j["12CLE"] = t_j["12CLE"]*1e6 
#         t_j["14_12_HE"] = t_j["14_12_HE"]*1e12
#         t_j["14_13_HE"] = t_j["14_13_HE"]*1e10
        

#         axs[0].plot(t_j["12CLE"],t_j["13_12_HE"], label=f'{targets[j]}', linestyle='-', marker='o')
#         axs[1].plot(t_j["12CLE"],t_j["14_12_HE"], linestyle='-', marker='o')
#         axs[2].plot(t_j["12CLE"],t_j["14_13_HE"], linestyle='-', marker='o')
#         axs[3].plot(t_j["serial"],t_j["12CLE"], linestyle='', marker='o')
#         axs[0].legend
    
#     if tws[i] in retunes:
#         axs[0].set_title(f'{tws[i]}_RETUNED', color='red')
#     else:
#         axs[0].set_title(f'{tws[i]}')

#     axs[0].set_ylim(0.01085,0.01125)
#     axs[1].set_ylim(1.18,1.235)
#     axs[2].set_ylim(1.05,1.13)
#     axs[3].set_ylim(0,110)

#     axs[0].set_xlim(0,110)
#     axs[1].set_xlim(0,110)
#     axs[2].set_xlim(0,110)

#     axs[0].axvline(x=100, color='red')
#     axs[1].axvline(x=100, color='red')
#     axs[2].axvline(x=100, color='red')

#     axs[0].set_ylabel('13/12HE')
#     axs[1].set_ylabel('14/12HE')
#     axs[2].set_ylabel('14/13HE')
#     axs[2].set_xlabel('LEC12- (uA)')
#     axs[3].set_xlabel('Run #')

#     axs[0].legend()

#     plt.savefig(rf"C:\Users\clewis\IdeaProjects\plots\{tws[i]}.png",
#                dpi=300, bbox_inches="tight")

#     "I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3600-3649\TW3629\plots"









