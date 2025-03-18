"""
Reviewer has asked me to compare Campbell Island to previous Campbell Island records.
The other record is Turney et al., 2018.
I have the following script below which compares CMP to MCQ. BUT I WILL ADAPT IT HERE TO COMPARE WITH TURNEY CMP.
"""

import numpy
import pandas as pd
from datetime import datetime
import matplotlib.ticker as mticker
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
from X_my_functions import long_date_to_decimal_date
from matplotlib.patches import Polygon
from sklearn.linear_model import LinearRegression
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import cartopy.crs as ccrs
import cartopy.feature as cf

"""
Copy of reference_to_sample_xvals.py 
"""
import pandas as pd
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend
from datetime import datetime
import matplotlib.pyplot as plt
# read in the list of all SAMPLES (SOAR)
# samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
# Dec 3 check from final EGU runs
samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/FINAL_DATA_JAN3_2025/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
samples = samples.loc[samples['DecimalDate'] > 1980].reset_index(drop=True)

# 12/12/2023 I need to add MCQ comparison (to validate CMP) into the paper. Need to add these into the works here,
# will add Heidelberg data now, and remove before main plots.
mcq = pd.read_excel('H:/Science/Datasets/Turney2018.xlsx', comment='#')
mcq = mcq.loc[mcq['Year'] > 1979]


mcq = mcq.rename(columns={'location': 'Site', 'Year': 'DecimalDate', '1sigma':'∆14Cerr','14C':'∆14C'})
samples = pd.concat([samples, mcq])
# samples.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/turney2018_comp/concat.xlsx')


# read in the references
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/FINAL_DATA_JAN3_2025/harmonized_dataset.xlsx')
ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/FINAL_DATA_JAN3_2025/reference1.xlsx')

output_xvals = pd.concat([ref2['Decimal_date'], ref1['Decimal_date'], samples['DecimalDate']]).reset_index(drop=True)
output_xvals = pd.DataFrame({'x': output_xvals}).sort_values(by=['x'], ascending=True).reset_index(drop=True)

n = 1000  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff
#
# """
# See Interlab_comparison project heidelberg_intercomparison_wD14C for further explanation of this function.
# """
reference2_smooth = monte_carlo_randomization_smooth(ref2['Decimal_date'], output_xvals['x'], ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
reference2_trend = monte_carlo_randomization_trend(ref2['Decimal_date'], output_xvals['x'], ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
reference3_smooth = monte_carlo_randomization_smooth(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)
reference3_trend = monte_carlo_randomization_trend(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)

reference2_smooth = reference2_smooth[2]
reference2_trend = reference2_trend[2]
reference3_smooth = reference3_smooth[2]
reference3_trend = reference3_trend[2]

montes = pd.DataFrame({'Decimal_date': output_xvals['x'],
                       'D14C_ref2s_mean': reference2_smooth['Means'], 'D14C_ref2s_std': reference2_smooth['stdevs'],
                       'D14C_ref2t_mean': reference2_trend['Means'], 'D14C_ref2t_std': reference2_trend['stdevs'],
                       'D14C_ref3s_mean': reference3_smooth['Means'], 'D14C_ref3s_std': reference3_smooth['stdevs'],
                       'D14C_ref3t_mean': reference3_trend['Means'], 'D14C_ref3t_std': reference3_trend['stdevs']
                       }).drop_duplicates(subset='Decimal_date')

"""
Copy of reference_to_sample_xvals2.py REMOVING ALL BUT REF3trend because that's what we ended up using
"""

D14C_ref3t_mean = []  # initialize an empty array
D14C_ref3t_std = []  # initialize an empty array

for i in range(0, len(samples)):
    samples_row = samples.iloc[i]
    sample_date = samples_row['DecimalDate']

    for k in range(0, len(montes)):
        df_row = montes.iloc[k]
        df_date = df_row['Decimal_date']

        if sample_date == df_date:
            D14C_ref3t_mean.append(df_row['D14C_ref3t_mean'])
            D14C_ref3t_std.append(df_row['D14C_ref3t_std'])

samples['D14C_ref3t_mean'] = D14C_ref3t_mean
samples['D14C_ref3t_std'] = D14C_ref3t_std

samples.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/turney2018_comp/line96.xlsx')

samples = samples.drop_duplicates().reset_index(drop=True)


samples = samples.rename(columns={'∆14C':'D14C_1'})
samples = samples.rename(columns = {'∆14Cerr':'weightedstderr_D14C_1'})
samples = samples.sort_values(by=['DecimalDate'])



from cmcrameri import cm
cmap=cm.davos
color_mcq = cm.lapaz(0.75)  # Lighter shade from batlow
color_cam = cm.lapaz(0.3)  # Darker shade from batlow

fig = plt.figure(figsize=(12, 6))
gs = gridspec.GridSpec(1, 2)
gs.update(wspace=.2, hspace=0.1)

# ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(gs[0, 0])
ax3 = fig.add_subplot(gs[0, 1])

# COPIED FROM MAIN_ANALYSIS.PY
# The difference between the data, and REFERENCE 1, BHD with CGO in the gaps (WEIGHTED RESIDUAL)
samples['r3_diff_trend'] = samples['D14C_1'] - samples['D14C_ref3t_mean']
samples['r3_diff_trend_errprop'] = np.sqrt(samples['weightedstderr_D14C_1'] ** 2 + samples['D14C_ref3t_std'] ** 2)

mcq = samples.loc[samples['Site'] == 'Campbell Island, Turney']
cam = samples.loc[samples['Site'] == 'Campbell Island, NZ']


ax2.errorbar(mcq['DecimalDate'], mcq['D14C_1'], yerr=mcq['weightedstderr_D14C_1'], color=color_mcq, marker='o', label='Campbell Island, (Turney et al., 2018)')
ax2.errorbar(cam['DecimalDate'], cam['D14C_1'], yerr=cam['weightedstderr_D14C_1'], color=color_cam, marker='D', label='Campbell Island', alpha=0.7)
# ax2.set_xlim(1980, 2020)
# ax2.set_ylim(62, 145)
ax2.set_ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')

ax3.errorbar(mcq['DecimalDate'], mcq['r3_diff_trend'], yerr=mcq['r3_diff_trend_errprop'], color=color_mcq, marker='o')
ax3.errorbar(cam['DecimalDate'], cam['r3_diff_trend'], yerr=cam['r3_diff_trend_errprop'], color=color_cam, marker='D', alpha=0.7)
ax3.set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')

# print('Is there a difference between Campbell Island and Macquarie Island? Null Hypothesis says: theres no difference!')
# c = stats.ttest_ind(cam['r3_diff_trend'], mcq['r3_diff_trend'])
# print(c)

# ax3.set_xlim(1980, 2020)
# ax3.set_ylim(-20, 20)

print(f"Mean DD14C for this work for Campbell Island is {np.mean(cam['r3_diff_trend'])}, while that of Turney et al 2018 is {np.mean(mcq['r3_diff_trend'])}")


ax2.legend()
plt.savefig(
    f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/turney2018_comparison/cmp_turney.png',
    dpi=300, bbox_inches="tight")
plt.close()





