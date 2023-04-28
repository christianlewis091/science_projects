"""
See overleaf supplementary information relating to thermal component calculation
"""

U = 7.5  # (m/s) ^2
U2 = U**2
Ua = 49
Sc = 600

k_w = 0.31*U2*(Sc/600)**(-0.5)  # in cm/hr
k_w_newunit = k_w * (8760/100)

D_e = 0.01* (U / Ua)**2

temp = 5
zeta = -2.5 / temp

sats = (23.37 - (0.96*23.37))
#
# print(zeta)
# print(sats)
# print(k_w_newunit)
# print(D_e)

phi_corr = k_w_newunit * (1+zeta+D_e) * sats

phi_tot = k_w_newunit * sats

print(phi_tot)
print(phi_corr)
print(phi_corr/phi_tot)
































# # copying import statement from soar_analysis3 - need to go back to here to normalize to temperature
# import pandas as pd
# import numpy as np
# from soar_analysis1 import df_2
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# from scipy import stats
#
#
# # grab yearly ocean data from NOAA
# oceandata = pd.read_excel(r'H:\Science\Datasets\oceanhist.xlsx')
#
# # I only care about data after 1980
# oceandata = oceandata.loc[oceandata['Year'] > 1979]
#
# # Here's a commented out plot of the data for later...
# # plt.scatter(oceandata['Year'], oceandata['Anomaly'])
# # plt.xlabel('Year')
# # plt.ylabel('Ocean Surface Temperature Anomaly')
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/ocean_temps.png',
# #             dpi=300, bbox_inches="tight")
# # plt.close()
#
# # have a look at the data to this point:
# # df_2.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
#
# # get rid of the decimals to grab only the year from each tree ring record
# end_arr = []
# for i in range(0, len(df_2)):
#     row = df_2.iloc[i]
#     date = row['Decimal_date']
#     date = str(date)
#     date = date[:4]
#     end_arr.append(date)
# df_2['Year'] = end_arr
#
# # associate the anomalies from the ocean data with the years of the records...
# end_arr1 = []
# end_arr2 = []
# for i in range(0, len(df_2)):
#     row = df_2.iloc[i]
#     tree_year = int(row['Year'])
#
#     for j in range(0, len(oceandata)):
#         orow = oceandata.iloc[j]
#         ocean_year = int(orow['Year'])
#
#         if tree_year == ocean_year:
#             end_arr1.append(orow['Anomaly'])
#             end_arr2.append(orow['total variance'])
#
# df_2['Assoc_anom'] = end_arr1
# df_2['Assoc_anom_err'] = end_arr2
#
# # now, normalize the data by the SST anomaly:
# df_2['r2_diff_trend_by_SST'] = df_2['r2_diff_trend'] / df_2['Assoc_anom']
# df_2['r2_diff_trend_by_SST_err'] = np.sqrt(df_2['r2_diff_trend_errprop']**2 + df_2['Assoc_anom_err']**2)
#
# #Here's a commented out plot of the data for later...
#
# plt.scatter(df_2['Decimal_date'], df_2['r2_diff_trend_by_SST'])
# plt.xlabel('Year')
# plt.ylabel('DD14C normalized by temp anomaly')
# # plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/ocean_temps.png',
# #             dpi=300, bbox_inches="tight")
# plt.show()
# plt.close()









# print(df_2['Decimal_date'][:4])

# df_2['YearOnly'] = str(df_2['Decimal_date'])[:4]
# print(df_2['YearOnly'])
#
# number = 1520
# x = int(str(number)[:2])
# print(x)















