
"""
SUPERCEEDED BY 13C_SPE_reboot.oy
"""
# """
# Lets clean up the 13C data for the reboot of this paper!
# """
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import math
# from scipy import stats
#
#
# """
# Importing data
# """
# # read in SPE data
# df = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\Cleaned_data.xlsx')
# df = df.dropna(subset='Raw d13C')
#
# # read in bulk data
# doc = pd.read_excel(r'H:\Science\Current_Projects\00_UCI_13C\bulkDOCdatabase.xlsx', sheet_name='New').dropna(subset='Value')
# doc = doc.replace('P16N.2', 'P16N')
#
# # read in P18 data to look at correlations with bottom depth/seamounts
# p18 = pd.read_csv('H:\Science\Datasets\Hydrographic\P18_2016.csv', skiprows=174).dropna(subset='DATE')
#
#
# """
# Part 1. Need to calculate the mass-balance corrected 13C value for the small contribution from the PPL cartridge
# # the relative abundances of Cex vs sample is defined from 9 ug Cex contribution from my first paper.
# """
#
# # define a number for the 13C of Cex
# cex_13C = -30  # typical value for petroleum 13C
#
# # calculate the mass-balance
# df['13C_corr'] = (df['Raw d13C'] - (cex_13C*df['X_blank']) ) / df['X_sample']
#
# # Propogate the error
# # for the multiplied term
# a = np.sqrt((0.2/cex_13C)**2 + (df['X_blank_err']/df['X_blank'])**2)
#
# # and now the whole numerator
# b = np.sqrt(a**2 + df['13cerr']**2)
# value = (df['Raw d13C'] - (cex_13C*df['X_blank']) )
#
# # and now the whole thing
# df['13C_corr_err'] = np.sqrt((b/value)**2 + (df['X_sample_err']/df['X_sample'])**2)
# # in the end, the error propogation makes the errors too small, so I'm putting the 0.2 back in
#
# # how much does the mass balance actually change the value? What is the percent change?
# df['pct_ch'] = ((df['Raw d13C'] - df['13C_corr']) / df['Raw d13C']) * 100
# # print(max(df['pct_ch']))
#
#
# """
#
# Comparing total DOC and SPE-DOC
#
# """
#
# names = ['P18', 'P16N','I7N']
# names2 = ['P18', 'P16','IO7']
#
# # Initialize some arrays to store data later
# bulk_av = []
# bulk_std = []
# SPE_av = []
# SPE_std = []
# descrip_doc = []
# descrip_spe = []
# nonret = []
# nonret_error = []
# ppl_rec = []
# ppl_rec_err = []
# count  = []
# for i in range(0, len(names)):
#
#     # grab the DOC from each cruise
#     a = doc.loc[doc['Ocean Region'] == names[i]]
#     # break up into surface and deep
#     a_s = a.loc[(a['Depth'] < 200)]
#     a_d = a.loc[(a['Depth'] < 4000) & (a['Depth'] > 2000)]
#
#     bulk_av.append(np.average(a_s['Value']))
#     bulk_std.append(np.std(a_s['Value']))
#     descrip_doc.append(f'Surface {names[i]}')
#
#     bulk_av.append(np.average(a_d['Value']))
#     bulk_std.append(np.std(a_d['Value']))
#     descrip_doc.append(f'Deep {names[i]}')
#
#
#     # grab the SPE-DOC from each cruise
#     b = df.loc[(df['Cruise'] == names2[i])]
#     # break up into surface and deep
#     b_s = b.loc[b['SorD'] == 'Surface']
#     print(b_s)
#     count.append(len(b_s))
#     b_d = b.loc[b['SorD'] == 'Deep']
#     print(b_d)
#     count.append(len(b_d))
#
#     SPE_av.append(np.average(b_s['13C_corr']))
#     SPE_std.append(np.std(b_s['13C_corr']))
#     # descrip_spe.append(f'Surface, SPE-DOC {names2[i]}')
#
#     SPE_av.append(np.average(b_d['13C_corr']))
#     SPE_std.append(np.std(b_d['13C_corr']))
#     # descrip_spe.append(f'Deep, SPE-DOC {names2[i]}')
#
#     # calculate non-retained's (surface)
#     rec = (np.nanmean(b_s['PPL % Recovery']))/100
#     rec_err = (np.nanstd(b_s['PPL % Recovery']))/100
#     ppl_rec.append(rec)
#     ppl_rec_err.append(rec_err)
#
#     nonretained_surface = (np.nanmean(a_s['Value']) - (np.nanmean(b_s['13C_corr'])*rec)) / (1-rec)
#     nonret.append(nonretained_surface)
#
#     # propogate the error
#     a = np.sqrt((np.nanmean(b_s['13C_corr_err'])/np.nanmean(b_s['13C_corr'])**2) + (np.nanmean(b_s['±.12'])/np.nanmean(b_s['PPL % Recovery'])**2))
#     b = np.sqrt(a**2 + np.nanmean(a_s['±']**2))
#     value = np.nanmean(a_s['Value']) - (np.nanmean(b_s['13C_corr'])*rec)
#     nonret_error_fin = -1*nonretained_surface*(np.sqrt((b/value)**2 + (np.nanmean(b_s['±.12'])/np.nanmean(b_s['PPL % Recovery'])**2)))
#     print(nonret_error_fin)
#     nonret_error.append(np.nanmean(nonret_error_fin))
# # #
#     # calculate non-retained's (deep)
#     rec = (np.nanmean(b_d['PPL % Recovery']))/100
#     rec_err = (np.nanstd(b_d['PPL % Recovery']))/100
#     ppl_rec.append(rec)
#     ppl_rec_err.append(rec_err)
#     nonretained_deep = (np.nanmean(a_d['Value']) - (np.nanmean(b_d['13C_corr'])*rec)) / (1-rec)
#     nonret.append(nonretained_deep)
#     # propogate the error
#     a = np.sqrt((np.nanmean(b_d['13C_corr_err'])/np.nanmean(b_d['13C_corr'])**2) + (np.nanmean(b_d['±.12'])/np.nanmean(b_d['PPL % Recovery'])**2))
#
#     b = np.sqrt(a**2 + np.nanmean(a_d['±']**2))
#     value = np.nanmean(a_d['Value']) - (np.nanmean(b_d['13C_corr'])*rec)
#     nonret_error_fin = -1*nonretained_deep*(np.sqrt((b/value)**2 + (np.nanmean(b_d['±.12'])/np.nanmean(b_d['PPL % Recovery'])**2)))
#     print(nonret_error_fin)
#     nonret_error.append(np.nanmean(nonret_error_fin))
#
#
# results = pd.DataFrame({"Description": descrip_doc, 'DOC 13C': bulk_av, 'error1': bulk_std,
#                         'SPE-DOC 13C': SPE_av, "error2": SPE_std, "PPL % Recovery": ppl_rec, "error3": ppl_rec_err,
#                         "Nonretained 13C": nonret, "error4": nonret_error, "N": count})
# #results.to_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\results_table.xlsx')
# plt.close()
#
#
# # plot the new model data
# colors = ['#d73027','#fc8d59','#91bfdb','#4575b4']
# markers = ['o','x','^','D','s']
#
# plt.errorbar(results['Description'], results['DOC 13C'], yerr=results['error1'], fmt=markers[0], color=colors[0], capsize=4)
# plt.scatter(results['Description'], results['DOC 13C'], color=colors[0], marker=markers[0], label='DOC')
#
# plt.errorbar(results['Description'], results['SPE-DOC 13C'], yerr=results['error2'], fmt=markers[1], color=colors[1], capsize=4)
# plt.scatter(results['Description'], results['SPE-DOC 13C'], color=colors[1], marker=markers[1], label='SPE-DOC')
#
# plt.errorbar(results['Description'], results['Nonretained 13C'], yerr=results['error4'], fmt=markers[2], color=colors[2], capsize=4)
# plt.scatter(results['Description'], results['Nonretained 13C'], color=colors[2], marker=markers[2], label='Nonretained')
# plt.legend()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Discussion1.png', dpi=95, bbox_inches="tight")
#
#
# """
# Based on my conversation with Ellen and Brett on 9/2/23, how does total DOC change with latitude? Do we see progressive reworking?
# """
#
# doc = doc.loc[doc['Flag'] != 'X']
# plt.close()
#
# names = ['I7N', 'P18','P16N']
#
# cruise = []
# means = []
# stds = []
# for i in range(0, len(names)):
#
#     # grab the DOC from each cruise
#     a = doc.loc[doc['Ocean Region'] == names[i]]
#
#     # grab only the deep ocean
#     a = a.loc[a['Depth'] >= 1500]
#     means.append(np.nanmean(a['Value']))
#     stds.append(np.nanstd(a['Value']))
#     cruise.append(names[i])
#
#     # plt.scatter(a['corr DEL 14C'], a['Value'])
#     # plt.show()
#
# dfnew = pd.DataFrame({"Cruise": cruise, "Mean": means, "STD": stds})
# plt.errorbar(cruise, means, yerr=stds)
# plt.plot(cruise, means)
# plt.scatter(cruise, means)
# plt.title('Mean DOC 13C <1500 m; progressive reworking of DOM?')
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Results4.png', dpi=300, bbox_inches="tight")
#
#
#
#
#
#
# # plt.scatter(doc['corr DEL 14C'], doc['Value'])
# # plt.xlabel('14C')
# # plt.ylabel('13C')
# # plt.show()
#
