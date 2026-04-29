"""

Toubleshooting travertine now!
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""
April 16, now I'm trying the same thing with the travertines
"""
trav = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\Final_results.xlsx", sheet_name='Clean Dataset')
trav_carb = trav.loc[trav['Job::R'] == '14047/2'].copy()
trav_water = trav.loc[trav['Job::R'] == '14047/12'].copy()

plt.scatter(trav_carb['wtgraph'], trav_carb['residual'])
plt.scatter(trav_water['wtgraph'], trav_water['residual'])
plt.show()









#
#
#
# # apply the average error from Trav carbonate to both, and see if waters still look better on chi2 test...
# # mean rts_corr_err for travertine carbonate is 0.001358
# trav_carb['RTS_err_test'] = .001358
# trav_water['RTS_err_test'] = .001358
# # check it first under normal case
# wmean_num = np.sum(trav_carb['RTS_corrected']/trav_carb['RTS_err_test']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
# wmean_dem = np.sum(1/trav_carb['RTS_err_test']**2)
# trav_carb['wmean'] = wmean_num / wmean_dem
#
# chi2_red_num = np.sum((trav_carb['RTS_corrected']-trav_carb['wmean'])**2/trav_carb['RTS_err_test']**2)
# chi2_red_denom = len(trav_carb)-1 # subtract number of groups in degrees of freedom calc.
# chi2_red = chi2_red_num/chi2_red_denom
# print('Travertine carbonate with fixed error')
# print(chi2_red)
# print()
#
# # check it first under normal case
# wmean_num = np.sum(trav_water['RTS_corrected']/trav_water['RTS_err_test']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
# wmean_dem = np.sum(1/trav_water['RTS_err_test']**2)
# trav_carb['wmean'] = wmean_num / wmean_dem
#
# chi2_red_num = np.sum((trav_water['RTS_corrected']-trav_water['wmean'])**2/trav_water['RTS_err_test']**2)
# chi2_red_denom = len(trav_water)-1 # subtract number of groups in degrees of freedom calc.
# chi2_red = chi2_red_num/chi2_red_denom
# print('Travertine water with fixed error')
# print(chi2_red)
# print()
#
# """
# What about standard deviation of the dataset as whole?
# """
# print(np.std(trav_carb['RTS_corrected']))