import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\TW3586_p1.csv")

# RLIMS has TP and size
tw3586_rlim = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_met.xlsx", sheet_name='RLIMSoutput')

# Runlist has TP and position
tw3586_run = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_met.xlsx", sheet_name='runlist')

# Merge the two above and you have the size and position combined
tw3586_metadata = tw3586_rlim.merge(tw3586_run, on='TP')

# # AccelNET/ CALAMS has data and position....
# tw3586_calam = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\TW3586_mode5_csv.CSV")

# merge once more and you have all combined
df = df.rename(columns={"position": "Position"})
df = tw3586_metadata.merge(df, on='Position')

# df.to_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_concatonated.xlsx")

position = np.unique(df['Position'])
df['lims'] = df['13Ccurr']/df['12Ccurr']

for pos in position:

    this_one = df.loc[df['Position'] == pos]
    # Get first-row metadata
    wtgraph = this_one['wtgraph'].iloc[0]
    desc    = this_one['Sample Name 2'].iloc[0]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    mode5 = (this_one['14Ccnts']*this_one['12Ccurr'])/(this_one['13Ccurr']**2)
    c13c12 = this_one['13Ccurr']/this_one['12Ccurr']

    # -------------------------------
    # LEFT PLOT: RTS vs Runs Completed
    # -------------------------------
    sc = axs[0].scatter( this_one['run'], mode5, c=this_one['12CLEcurr'],cmap='viridis')
    axs[0].set_xlabel('Runs Completed')
    axs[0].set_ylabel('Mode 5 Approx')
    axs[0].set_title(f'RTS Drift — Pos {pos}')

    # Colorbar (attach to entire figure)
    cbar = fig.colorbar(sc, ax=axs[0], label='12CLEcurr')

    # -------------------------------
    # RIGHT PLOT: 13C/12C vs 12C[uA]
    # -------------------------------
    axs[1].scatter(this_one['run'], c13c12, marker='o', linestyle='')
    axs[1].set_xlabel('Runs Completed')
    axs[1].set_ylabel('13C/12C')
    axs[1].set_title(f'13C/12C vs Beam — Pos {pos}')
    axs[1].set_ylim(np.min(df['lims']), np.max(df['lims']))

    fig.suptitle(
        f"wtgraph: {wtgraph}    |    sample description: {desc}",
        fontsize=14, fontweight='bold', y=1.03
    )


    # -------------------------------
    # SAVE FIGURE
    # -------------------------------
    plt.tight_layout()
    # plt.show()
    plt.savefig(fr"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\plots_combined\pos{pos}.png",dpi=300,bbox_inches="tight")
    plt.close()



#
# df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\ADE2_analysis_Dec5.xlsx", sheet_name='Sheet1')
#
# # add a new column and set some variables
# df['unc2_edit'] = np.abs(df['unc2'])*df['13C/12C']
# c13min = np.min(df['13C/12C'])
# c13max = np.max(df['13C/12C'])
#
# position = np.unique(df['pos'])
#
# for pos in position:
#     this_one = df.loc[df['pos'] == pos]
#     fig, axs = plt.subplots(1, 2, figsize=(12, 5))
#
#     # -------------------------------
#     # LEFT PLOT: RTS vs Runs Completed
#     # -------------------------------
#     axs[0].errorbar(this_one['run max'],this_one['Oxalic Ratio'],yerr=np.abs(this_one['Uncertainty']),fmt='none',ecolor='gray',alpha=0.7)
#     sc = axs[0].scatter( this_one['run max'],this_one['Oxalic Ratio'],c=this_one['12C[uA]'],cmap='viridis')
#     axs[0].set_xlabel('Runs Completed')
#     axs[0].set_ylabel('RTS')
#     axs[0].set_title(f'RTS Drift — Pos {pos}')
#
#     # Colorbar (attach to entire figure)
#     cbar = fig.colorbar(sc, ax=axs[0], label='12C [uA]')
#
#     # -------------------------------
#     # RIGHT PLOT: 13C/12C vs 12C[uA]
#     # -------------------------------
#     axs[1].errorbar(this_one['run max'],this_one['13C/12C'],yerr=np.abs(this_one['unc2_edit']), marker='o', linestyle='')
#     axs[1].set_xlabel('Runs Completed')
#     axs[1].set_ylabel('13C/12C')
#     axs[1].set_title(f'13C/12C vs Beam — Pos {pos}')
#     axs[1].set_ylim(c13min, c13max)
#
#     # -------------------------------
#     # SAVE FIGURE
#     # -------------------------------
#     plt.tight_layout()
#     plt.savefig(fr"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\plots_combined\pos{pos}.png",dpi=300,bbox_inches="tight")
#     plt.close()

# """
# REPEAT FOR ADE1
# """
#
# df = pd.read_excel(
#     r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\ADE1_analysis_Dec5.xlsx",
#     sheet_name='Sheet3'
# )
# df['unc2_edit'] = np.abs(df['unc2'])*df['13C/12C']
# c13min = np.min(df['13C/12C'])
# c13max = np.max(df['13C/12C'])
#
# position = np.unique(df['pos'])
#
# for pos in position:
#     this_one = df.loc[df['pos'] == pos]
#     fig, axs = plt.subplots(1, 2, figsize=(12, 5))
#
#     # -------------------------------
#     # LEFT PLOT: RTS vs Runs Completed
#     # -------------------------------
#     axs[0].errorbar(this_one['run max'],this_one['Oxalic Ratio'],yerr=np.abs(this_one['Uncertainty']),fmt='none',ecolor='gray',alpha=0.7)
#     sc = axs[0].scatter( this_one['run max'],this_one['Oxalic Ratio'],c=this_one['12C[uA]'],cmap='viridis')
#     axs[0].set_xlabel('Runs Completed')
#     axs[0].set_ylabel('RTS')
#     axs[0].set_title(f'RTS Drift — Pos {pos}')
#
#     # Colorbar (attach to entire figure)
#     cbar = fig.colorbar(sc, ax=axs[0], label='12C [uA]')
#
#     # -------------------------------
#     # RIGHT PLOT: 13C/12C vs 12C[uA]
#     # -------------------------------
#     axs[1].errorbar(this_one['run max'],this_one['13C/12C'],yerr=np.abs(this_one['unc2_edit']), marker='o', linestyle='')
#     axs[1].set_xlabel('Runs Completed')
#     axs[1].set_ylabel('13C/12C')
#     axs[1].set_title(f'13C/12C vs Beam — Pos {pos}')
#     axs[1].set_ylim(c13min, c13max)
#
#     # -------------------------------
#     # SAVE FIGURE
#     # -------------------------------
#     plt.tight_layout()
#     # -------------------------------
#     # SAVE FIGURE
#     # -------------------------------
#     plt.tight_layout()
#     plt.savefig(
#         fr"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\plots_combined\pos{pos}.png",
#         dpi=300,
#         bbox_inches="tight"
#     )
#     plt.close()
#
#
#
#
#
#
#
#
#











































#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# """
# OLD JUNK BELOW!
# """
#
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# # df = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_test.CSV")
# # df2 = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_test_m1.CSV")
# #
# # positions = np.unique(df[' Position'])
# # # positions = [1., 0.,5.,20.,25.,30.,35.]
# # positions=[25]
# # for i in range(0, len(positions)):
# #     subset = df.loc[df[' Position'] == positions[i]]
# #     subset2 = df.loc[df[' Position'] == positions[i]]
# #     mean_red = np.mean(subset[' Reduced'])
# #     unc = 1/np.sqrt(subset[' C-14 counts'])
# #
# #     plt.errorbar(subset[' Run'], subset[' Reduced'], label=positions[i], yerr=unc, marker='o', color='black', linestyle='')
# #     plt.errorbar(subset2[' Run'], subset2[' Reduced'], label=positions[i], yerr=unc, marker='o', color='black', linestyle='')
# #     plt.legend()
# #     # plt.ylim(0.150,0.202)
# #
# #     plt.show()
#
# """
# Trying to analyze ADE1 and ADE2 TW3586 and TW3587
# """
#
# """
# data wrangle TW3587
# """
# # # RLIMS has TP and size
# # tw3587_rlim = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\tw3587_met.xlsx", sheet_name='RLIMSoutput')
# # # Runlist has TP and position
# # tw3587_run = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\tw3587_met.xlsx", sheet_name='runlist')
# #
# # # CALAMS has data and position....
# # tw3587_calam = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\3587_mode5_csv.CSV")
# #
# # tw3587_metadata = tw3587_rlim.merge(tw3587_run, on='TP')
# # tw3587_df = tw3587_metadata.merge(tw3587_calam, on='Position')
# #
# # tw3587_df.to_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\3587_concatonated.xlsx")
# # tw3587_df['TW'] = 3587
# """
# data wrangle TW3586
# """
# # # RLIMS has TP and size
# # tw3586_rlim = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_met.xlsx", sheet_name='RLIMSoutput')
# # # Runlist has TP and position
# # tw3586_run = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_met.xlsx", sheet_name='runlist')
# #
# # # CALAMS has data and position....
# # tw3586_calam = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\TW3586_mode5_csv.CSV")
# #
# # tw3586_metadata = tw3586_rlim.merge(tw3586_run, on='TP')
# # tw3586_df = tw3586_metadata.merge(tw3586_calam, on='Position')
# #
# # tw3586_df.to_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_concatonated.xlsx")
# # tw3586_df['TW'] = 3586
# #
# # ade1_2 = pd.concat([tw3586_df,tw3587_df])
# # ade1_2.to_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\3586_3587_concatonated.xlsx")
#
# """
# Now we can do some analyses
# """
# """
# BELOW IS THE FULLD DATA FROM CALAMS RUN BY RUN
# """
#
# # import matplotlib.pyplot as plt
# # df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\3586_3587_concatonated.xlsx")
# #
# # firi_ade1 = df.loc[(df['TW'] == 3586) & (df['Sample Name 2'] == 'FIRI-D:_wood')]
# # firi_ade2 = df.loc[(df['TW'] == 3587) & (df['Sample Name 2'] == 'FIRI-D:_wood')]
# #
# # ox_ade1 = df.loc[(df['TW'] == 3586) & (df['Sample Name 2'] == 'NBS_Oxalic_I')]
# # ox_ade2 = df.loc[(df['TW'] == 3587) & (df['Sample Name 2'] == 'NBS_Oxalic_I')]
# #
# #
# # fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 3 rows, 1 column
# # axs[1].scatter(firi_ade1['wtgraph'], firi_ade1[' C-13/C-12 HE [ ]'], label='ADE 1', marker='o', color='black', linestyle='')
# # axs[1].scatter(firi_ade2['wtgraph'], firi_ade2[' C-13/C-12 HE [ ]'], label='ADE 2', marker='D', color='gray', linestyle='')
# #
# # axs[0].scatter(ox_ade1['wtgraph'], ox_ade1[' C-13/C-12 HE [ ]'], label='ADE 1', marker='o', color='black', linestyle='')
# # axs[0].scatter(ox_ade2['wtgraph'], ox_ade2[' C-13/C-12 HE [ ]'], label='ADE 2', marker='D', color='gray', linestyle='')
# #
# # axs[0].legend()
# # axs[0].set_title('NBS Oxalic I')
# # axs[1].set_title('FIRI-D: wood')
# #
# # plt.show()
#
"""
HERE IS THE SUMMARY DATA IN RLIMS, BLANK CORRECTED
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_86 = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586/OLD_MISC\3586_V4.xlsx")
df_87 = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587/OLD_MISC\3587_V4.xlsx")
firis = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587/OLD_MISC\historical_firi.xlsx")

df_86_firi = df_86.loc[df_86['Samples::Sample Description'] == 'FIRI-D: wood']
df_87_firi = df_87.loc[df_87['Samples::Sample Description'] == 'FIRI-D: wood']

df_86_ox = df_86.loc[df_86['Samples::Sample Description'] == 'Kauri Renton Road ']
df_87_ox = df_87.loc[df_87['Samples::Sample Description'] == 'Kauri Renton Road ']
kauri = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587/OLD_MISC\kauri_hist.xlsx")


plt.close()
fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 3 rows, 1 column

axs[0].errorbar(df_86_ox['wtgraph'], df_86_ox['F_corrected_normed'], label='ADE1', yerr=df_86_ox['F_corrected_normed_error'], marker='o', color='black', linestyle='')
axs[0].errorbar(df_87_ox['wtgraph'], df_87_ox['F_corrected_normed'], label='ADE2', yerr=df_87_ox['F_corrected_normed_error'], marker='D', color='red', linestyle='')
axs[0].errorbar(kauri['wtgraph'], kauri['F_corrected_normed'], label='KAURI HISTORICAL', yerr=kauri['F_corrected_normed_error'], marker='D', color='blue', linestyle='', alpha=0.1)

axs[1].errorbar(firis['wtgraph'], firis['F_corrected_normed'], label='Historical FIRI', yerr=firis['F_corrected_normed_error'], marker='s', color='blue', linestyle='', alpha=0.05)
axs[1].errorbar(df_86_firi['wtgraph'], df_86_firi['F_corrected_normed'], label='ADE1', yerr=df_86_firi['F_corrected_normed_error'], marker='o', color='black', linestyle='')
axs[1].errorbar(df_87_firi['wtgraph'], df_87_firi['F_corrected_normed'], label='ADE2', yerr=df_87_firi['F_corrected_normed_error'], marker='D', color='red', linestyle='')

cra_expected = 4508
fm_expected = np.exp(cra_expected/-8033)

axs[0].set_title('Kauri 0157 - Wk17031')
axs[1].set_title('FIRI-D: wood')
axs[1].axhline(y=fm_expected, color='black')
# axs[0].set_ylim(1,1.07)
axs[0].legend()

# plt.ylim(0.150,0.202)
plt.savefig(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587/blanks.png", dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
# """
# FIRI vs Histoprical FITI and MCC size
# """
#
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
# df_86 = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\3586_V3_output_forchecking.xlsx")
# df_87 = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\3587_V3_output_forchecking.xlsx")
# firis = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\historical_firi.xlsx")
#
# df_86_firi = df_86.loc[df_86['Samples::Sample Description'] == 'FIRI-D: wood']
# df_87_firi = df_87.loc[df_87['Samples::Sample Description'] == 'FIRI-D: wood']
#
# df_86_ox = df_86.loc[df_86['Samples::Sample Description'] == 'NBS Oxalic I']
# df_87_ox = df_87.loc[df_87['Samples::Sample Description'] == 'NBS Oxalic I']
#
# plt.close()
# fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # 3 rows, 1 column
#
# axs[0].errorbar(firis['wtgraph'], firis['F_corrected_normed'], label='Historical FIRI', yerr=firis['F_corrected_normed_error'], marker='s', color='blue', linestyle='', alpha=0.5)
# axs[0].errorbar(df_86_firi['wtgraph'], df_86_firi['F_corrected_normed'], label='ADE1', yerr=df_86_firi['F_corrected_normed_error'], marker='o', color='black', linestyle='')
# axs[0].errorbar(df_87_firi['wtgraph'], df_87_firi['F_corrected_normed'], label='ADE2', yerr=df_87_firi['F_corrected_normed_error'], marker='D', color='red', linestyle='')
#
# axs[1].errorbar(firis['wtgraph'], firis['MCC'], label='Historical FIRI', yerr=firis['MCC_error'], marker='s', color='blue', linestyle='', alpha=0.5)
# axs[1].errorbar(df_86_firi['wtgraph'], df_86_firi['MCC'], label='ADE1', yerr=df_86_firi['MCC_error'], marker='o', color='black', linestyle='')
# axs[1].errorbar(df_87_firi['wtgraph'], df_87_firi['MCC'], label='ADE2', yerr=df_87_firi['MCC_error'], marker='D', color='red', linestyle='')
#
#
# cra_expected = 4508
# fm_expected = np.exp(cra_expected/-8033)
#
# axs[0].set_title('FIRI-D Corrected, ADE1 & ADE2 vs historic')
# axs[1].set_title('MCC Record')
# axs[0].axhline(y=fm_expected, color='black')
# # axs[0].set_ylim(1,1.07)
# axs[0].legend()
# axs[0].set_xlabel('wtgraph')
# axs[1].set_xlabel('wtgraph')
# axs[0].set_ylabel('F_corrected_normed')
# axs[1].set_ylabel('MCC')
# # plt.ylim(0.150,0.202)
#
# plt.savefig(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587/MCC_analysis.png", dpi=300, bbox_inches="tight")
# # plt.show()
#
#
#
#

# plt.close()
# # TW3586
# plt.scatter([0.17,0.25,0.08], [0.04,0.01,0.1], label='TW3586')
# # TW3587
# plt.scatter([.09,.25,.07,.09,.15,.93], [.042,.02,.091,.0504,.02,.004], label='TW3587')
# plt.xlabel('wtgraph')
# plt.ylabel('Assigned RTS required to match FIRI-D target value')
# plt.legend()
# plt.show()