"""
Recreate albert's figure from poster and see how he calcultes RES
"""
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore')

"""
July 1, 2024:
I discussed the idea of sigma_res with JCT today. Essentially, sigma_res is an added error term in the chi2 equation
Paper is updated now with the right equation

BELOW, I tried to recreate some data from Albert's 2022 Radiocarbon Poster, but it was folly. I cant reproduce his sigma_res.
I'm going to try to do that his "simplified_RLIMS_dataset by recreating the data in his "Tables.xlsx" that came with his data and v1 of paper
"""

df = pd.read_csv('H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/Alberts_Version/simplified RLIMS dataset.csv')
df = df.loc[df['FracMOD'] != 'Missing[]']
cols = ['FracMOD','FerrNOwtw','FerrNOwtwNOsys','FracMODerr','RTSerr','MCC','MCCerr','RTS']
df[cols] = df[cols].apply(pd.to_numeric, errors='coerce', axis=1)

# data with the secondaries to filter on
df2 = pd.read_excel('H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/seconds.xlsx')

# groups to filter on
rs = np.unique(df2['R_number'])


"""
# lets loop through the R numbers and get means and stats assigned to each value in the database...
"""

group_name = []
R_num = []
length = []
wmean_arr = []
stdev_arr = []
sterr_arr = []
chi2_red_arr = []
sig_res_arr = []
opt_chi = []


for i in range(0, len(rs)):
    subset1 = df.loc[df['R_number'] == rs[i]]
    R_num.append(rs[i])

    group = df2.loc[df2['R_number'] == rs[i]]
    group_name.append(np.unique(group['Group']).astype(str))

    length.append(len(subset1))

    wmean_num = np.sum(subset1['FracMOD']/subset1['FerrNOwtwNOsys']**2)
    wmean_dem = np.sum(1/subset1['FerrNOwtwNOsys']**2)
    wmean = wmean_num / wmean_dem
    wmean_arr.append(wmean)

    stdev_arr.append(np.std(subset1['FracMOD']))
    sterr_arr.append(np.sum(1/(subset1['FerrNOwtwNOsys']**2))**-0.5)

    # calc chi2
    chi2_red_num = np.sum((subset1['FracMOD']-wmean)**2/subset1['FerrNOwtwNOsys']**2)
    chi2_red_denom = len(subset1)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom
    chi2_red_arr.append(chi2_red)

    """
    Optomize Chi2 to find sigma_residual
    """
    sig_res = np.linspace(0.00001, 0.010, 100)

    # Variables to store the best result
    best_sig_res = None
    closest_chi2_red = float('inf')
    target_chi2_red = 1.0

    for i in range(len(sig_res)):
        # Calculate chi2_red for the current sig_res
        chi2_red_num = np.sum((subset1['FracMOD'] - wmean)**2 / (subset1['FerrNOwtwNOsys']**2 + sig_res[i]**2))
        chi2_red_denom = len(subset1)-1
        chi2_red = chi2_red_num / chi2_red_denom

        # Check if this chi2_red is closer to 1
        if abs(chi2_red - target_chi2_red) < abs(closest_chi2_red - target_chi2_red):
            closest_chi2_red = chi2_red
            best_sig_res = sig_res[i]

    sig_res_arr.append(best_sig_res)
    opt_chi .append(closest_chi2_red)

output1 = pd.DataFrame({'R Numbers in Group': R_num, 'Data Length (n)': length,
                        'Weighted Mean': wmean_arr,'Standard Deviation': stdev_arr,'Standard Error': sterr_arr,
                        'Chi2 Reduced': chi2_red_arr, 'Sigma Residual': sig_res_arr, 'Optd Chi2': opt_chi, 'Group':group_name})

output1.to_excel('H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/statistics.xlsx')














# attach group name later








    # # assign these WMEANS onto the dataframe
    # df.loc[(df['R_number'] == rs[i]), 'WMEAN_for_this_R'] = wmean
    # df.loc[(df['R_number'] == rs[i]), 'STDEV_for_this_R'] = stdev
    # df.loc[(df['R_number'] == rs[i]), 'RESIDUAL'] = ((subset1['FracMOD']-wmean)**2/subset1['FerrNOwtwNOsys']**2)














# we will loop through the groups, and calculate stats for each one
# # below I make some arrays to put the data in later
#
# group_name = []
# R_num_List = []
# chi2_red_arr = []       # normal chi2 reduced
# sig_res_arr = []        # sigma residual is found by adding error so that chi2 = 1
# optomized_chi_arr = []  # sigma residual is found by adding error so that chi2 = 1, how close is the final chi2 value
#
#
# for i in range(0, len(groups)):
#     group1 = df2.loc[df2['Group'] == groups[i]]

    # # how many unique R numbers are in this group?
    # rs_in_group = np.unique(group1['R_number'])
    #
    # for j in range(0, len(rs_in_group)):
    #     # find wherever these TP's are in the main data sheet
    #     subset1 = df.loc[df['R_number'] == rs_in_group[i]]
    #
    #
    #     # # append the name of this group
    #     # group_name.append(groups[i])
    #     #
    #     # # append the list of rs in this group
    #     # R_num_List.append(rs_in_group[i])
    #     #
    #     # # how many samples are there total?
    #     # length_arr.append(len(subset1))
    #
    #     # append some of the stats
    #     # straight_mean.append(np.mean(subset1['FracMOD']))
    #     #
    #     wmean_num = np.sum(subset1['FracMOD']/subset1['FerrNOwtwNOsys']**2)
    #     wmean_dem = np.sum(1/subset1['FerrNOwtwNOsys']**2)
    #     wmean = wmean_num / wmean_dem
    #     #
    #     #
    #     # stdev_arr.append(np.std(subset1['FracMOD']))
    #     # sterr_arr.append(np.sum(1/(subset1['FerrNOwtwNOsys']**2))**-0.5)
    #
    #     # calc chi2
    #     chi2_red_num = np.sum((subset1['FracMOD']-wmean)**2/subset1['FerrNOwtwNOsys']**2)
    #     chi2_red_denom = len(subset1)-len(rs_in_group) # subtract number of groups in degrees of freedom calc.
    #     chi2_red = chi2_red_num/chi2_red_denom
    #     chi2_red_arr.append(chi2_red)
    #

#
#     """
#     Optomize Chi2 to find sigma_residual
#     """
#     sig_res = np.linspace(0.0001, 0.0010, 50)
#
#     # Variables to store the best result
#     best_sig_res = None
#     closest_chi2_red = float('inf')
#     target_chi2_red = 1.0
#
#     for i in range(len(sig_res)):
#         # Calculate chi2_red for the current sig_res
#         chi2_red_num = np.sum((subset1['FracMOD'] - wmean)**2 / (subset1['FerrNOwtwNOsys']**2 + sig_res[i]**2))
#         chi2_red_denom = len(subset1)-len(rs_in_group)
#         chi2_red = chi2_red_num / chi2_red_denom
#
#         # Check if this chi2_red is closer to 1
#         if abs(chi2_red - target_chi2_red) < abs(closest_chi2_red - target_chi2_red):
#             closest_chi2_red = chi2_red
#             best_sig_res = sig_res[i]
#
#     sig_res_arr.append(best_sig_res)
#     optomized_chi_arr.append(closest_chi2_red)
#
# output1 = pd.DataFrame({'Group Name': group_name, 'R Numbers in Group': R_num_List, 'Data Length (n)': length_arr,
#                         'Mean': straight_mean, 'Weighted Mean': wmean_arr,'Standard Deviation': stdev_arr,'Standard Error': sterr_arr,
#                         'Chi2 Reduced': chi2_red_arr, 'Sigma Residual': sig_res_arr, 'Optd Chi2': optomized_chi_arr})
#
# output1.to_excel('H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/statistics.xlsx')




