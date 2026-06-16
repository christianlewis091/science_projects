# why are our calibrations so bad recently? What is their normal spread now versus past??
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_excel('I:/C14Data/C14_blank_corrections_NEW/import_from_RLIMS/historical_data/TW3547standards.xlsx')
print(df.columns)
plt.scatter(df['Ratio to standard'], df['Ratio to standard error'])
plt.xlim(0,1)
plt.ylim(0.00,0.02)
plt.show()
# df = df.loc[(df['Job::CorrectionCategory'] == 'Primary') & (df['AMS Category ID XCAMS'] == 'OxI')]
# df = df.loc[df['TW'] > 3450]
# df = df.loc[df['TW'] == 3546]
# print(np.unique(df['TP']))
# fig = plt.figure(figsize=(8, 8))
# gs = gridspec.GridSpec(2, 1)
# gs.update(wspace=.15, hspace=0.5)
#
# ax1 = fig.add_subplot(gs[0, 0])
# ax2 = fig.add_subplot(gs[1, 0])
#
# std_ix = []
# wheels = np.unique(df['TW'])
# for i in range(0, len(wheels)):
#     df_i = df.loc[df['TW'] == wheels[i]]
#     ax1.scatter(df_i['TW'], df_i['Ratio to standard'])
#
#     std_ix.append(np.std(df_i['Ratio to standard']))
#
# ax2.scatter(wheels, std_ix)
#
# # add labels
# ax2.set_xlabel('TW')
# ax1.set_ylabel('RTS')
# ax2.set_ylabel('RTS STD')
#
# df2 = pd.DataFrame({"TW": wheels, "std": std_ix})
# df2.to_excel('I:/XCAMS/20_REPORTS_AFTER_XCAMS_ISSUES/Dec2024_Jan2025_BadCalibrations+Geometry/January_13_2025_some_outputs.xlsx')
# # plt.savefig(
# #     f'I:/XCAMS/20_REPORTS_AFTER_XCAMS_ISSUES/Dec2024_Jan2025_BadCalibrations+Geometry/January_13_2025_TW_v_RTS_and_stdev.png',
# #     dpi=300, bbox_inches="tight")
# # plt.close()
# plt.show()

"""
Section 2 can I find a relationship between position and badness? 
"""

# df = pd.read_excel('I:/C14Data/C14_blank_corrections_NEW/import_from_RLIMS/historical_data/TW3547standards.xlsx')
# df = df.loc[(df['Job::CorrectionCategory'] == 'Primary') & (df['AMS Category ID XCAMS'] == 'OxI')]
# df = df.loc[df['TW'] > 3450]

# fig = plt.figure(figsize=(8, 8))

# wheels = np.unique(df['TW'])
# for i in range(0, len(wheels)):
#     df_i = df.loc[df['TW'] == wheels[i]]
#     std_i_plot = np.std(df_i['Ratio to standard']) # this is exclusively for the subloop below
#
#     if std_i_plot > 0.002:
#         plt.scatter(df_i['Position'], df_i['Ratio to standard'])
# plt.scatter(df['Position'], df['Ratio to standard'])
# plt.savefig(
#     f'I:/XCAMS/20_REPORTS_AFTER_XCAMS_ISSUES/Dec2024_Jan2025_BadCalibrations+Geometry/January_13_2025_position_v_rts_2.png',
#     dpi=300, bbox_inches="tight")
# plt.close()
