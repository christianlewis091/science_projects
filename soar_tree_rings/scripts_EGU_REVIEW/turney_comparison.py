"""
OLD!

"""

# """
# Reviewer asked me to compare our results with Turney 2018 which is totally reasonable since he has a record of Lonliest tree and others from
# campbell Island as well.
# I don't want to edit my other scritps themselves, but I'll just copy and edit them here all in one go.
#
# """
# import pandas as pd
# from X_my_functions import monte_carlo_randomization_smooth
# from X_my_functions import monte_carlo_randomization_trend
# from datetime import datetime
# import numpy as np
#
#
# samples = pd.read_excel('H:\Science\Papers\In Prep Work/2023_Lewis_SOARTreeRings\V9_Jan282025_reviewer_comments/Turney_data.xlsx', skiprows=2)
# samples = samples.loc[samples['Year']>=1980]
#
# # 12/12/2023 I need to add MCQ comparison (to validate CMP) into the paper. Need to add these into the works here,
# # will add Heidelberg data now, and remove before main plots.
# # mcq = pd.read_excel('H:/Science/Datasets/heidelberg_MQA.xlsx')
#
# # res = []
# # # need to convert MCQ dates to decimal dates
# # for i in range(0, len(mcq)):
# #     row = mcq.iloc[i]
# #     date_string = str(row['Average of Dates'])
# #     date_string = date_string[:10]
# #     date_object = datetime.strptime(date_string, '%Y-%m-%d')
# #     decimal_date = date_object.year + (date_object.timetuple().tm_yday - 1) / 365.25
# #     res.append(decimal_date)
# # mcq['Average of Dates'] = res
#
# # mcq = mcq[['#location', 'Average of Dates', 'D14C','1sigma_error']]
# # mcq = mcq.rename(columns={'#location': 'Site', 'Average of Dates': 'DecimalDate', '1sigma_error':'∆14Cerr','D14C':'∆14C'})
# # samples = pd.concat([samples, mcq])
# # samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned.xlsx')
#
# # read in the references
# ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/harmonized_dataset.xlsx')
# ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/reference1.xlsx')
#
# output_xvals = pd.concat([ref2['Decimal_date'], ref1['Decimal_date'], samples['Year']]).reset_index(drop=True)
# output_xvals = pd.DataFrame({'x': output_xvals}).sort_values(by=['x'], ascending=True).reset_index(drop=True)
#
# # edited down tenfold for computation time for reviewer quick test
# n = 2  # set the amount of times the code will iterate (set to 10,000 once everything is final)
# cutoff = 667  # FFT filter cutoff
# #
# # """
# # See Interlab_comparison project heidelberg_intercomparison_wD14C for further explanation of this function.
# # """
# reference2_smooth = monte_carlo_randomization_smooth(ref2['Decimal_date'], output_xvals['x'], ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
# reference2_trend = monte_carlo_randomization_trend(ref2['Decimal_date'], output_xvals['x'], ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
# reference3_smooth = monte_carlo_randomization_smooth(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)
# reference3_trend = monte_carlo_randomization_trend(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)
#
# reference2_smooth = reference2_smooth[2]
# reference2_trend = reference2_trend[2]
# reference3_smooth = reference3_smooth[2]
# reference3_trend = reference3_trend[2]
#
# montes = pd.DataFrame({'Decimal_date': output_xvals['x'],
#                        'D14C_ref2s_mean': reference2_smooth['Means'], 'D14C_ref2s_std': reference2_smooth['stdevs'],
#                        'D14C_ref2t_mean': reference2_trend['Means'], 'D14C_ref2t_std': reference2_trend['stdevs'],
#                        'D14C_ref3s_mean': reference3_smooth['Means'], 'D14C_ref3s_std': reference3_smooth['stdevs'],
#                        'D14C_ref3t_mean': reference3_trend['Means'], 'D14C_ref3t_std': reference3_trend['stdevs']
#                        }).drop_duplicates(subset='Decimal_date')
#
#
# D14C_ref2s_mean = []  # initialize an empty array
# D14C_ref2s_std = []  # initialize an empty array
#
# D14C_ref2t_mean = []  # initialize an empty array
# D14C_ref2t_std = []  # initialize an empty array
#
# D14C_ref3s_mean = []  # initialize an empty array
# D14C_ref3s_std = []  # initialize an empty array
#
# D14C_ref3t_mean = []  # initialize an empty array
# D14C_ref3t_std = []  # initialize an empty array
#
# for i in range(0, len(samples)):
#     samples_row = samples.iloc[i]
#     sample_date = samples_row['Year']
#
#     for k in range(0, len(montes)):
#         df_row = montes.iloc[k]
#         df_date = df_row['Decimal_date']
#
#         if sample_date == df_date:
#             D14C_ref2s_mean.append(df_row['D14C_ref2s_mean'])
#             D14C_ref2s_std.append(df_row['D14C_ref2s_std'])
#             D14C_ref2t_mean.append(df_row['D14C_ref2t_mean'])
#             D14C_ref2t_std.append(df_row['D14C_ref2t_std'])
#             D14C_ref3s_mean.append(df_row['D14C_ref3s_mean'])
#             D14C_ref3s_std.append(df_row['D14C_ref3s_std'])
#             D14C_ref3t_mean.append(df_row['D14C_ref3t_mean'])
#             D14C_ref3t_std.append(df_row['D14C_ref3t_std'])
#
# samples['D14C_ref2s_mean'] = D14C_ref2s_mean
# samples['D14C_ref2s_std'] = D14C_ref2s_std
# samples['D14C_ref2t_mean'] = D14C_ref2t_mean
# samples['D14C_ref2t_std'] = D14C_ref2t_std
# samples['D14C_ref3s_mean'] = D14C_ref3s_mean
# samples['D14C_ref3s_std'] = D14C_ref3s_std
# samples['D14C_ref3t_mean'] = D14C_ref3t_mean
# samples['D14C_ref3t_std'] = D14C_ref3t_std
#
#
# # The difference between the data, and REFERENCE 1, BHD with CGO in the gaps (WEIGHTED RESIDUAL)
# samples['r3_diff_trend'] = samples['14C'] - samples['D14C_ref3t_mean']
# samples['r3_diff_trend_errprop'] = np.sqrt(samples['1sig'] ** 2 + samples['D14C_ref3t_std'] ** 2)
# pn = np.mean(samples['r3_diff_trend'])
# std = np.std(samples['r3_diff_trend'])
# print(f'PN mean is {pn}, std is {std}')
#
#
#
#
#
