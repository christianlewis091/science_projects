"""
Reviewer has asked me to compare Campbell Island to Macquarie Island
I had done this before but actually somehow it didn't make it into the ifnal version of the paper. We will add that now.

Important noets:
Reference_to_sample_xvals.py currently includes MCQ. This means the monte carlo output DOES EXIST at the x values of MCQ dataset.
I just need to ensure that MCQ is added onto the "sample" dataset in the "main_analysis.py".
Mush below is copied from main_analysis.py
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
Copy of reference_to_sample_xvals.py BUT n is set to 10
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

# 12/12/2023 I need to add MCQ comparison (to validate CMP) into the paper. Need to add these into the works here,
# will add Heidelberg data now, and remove before main plots.
mcq = pd.read_excel('H:/Science/Datasets/heidelberg_MQA.xlsx')

res = []
# need to convert MCQ dates to decimal dates
for i in range(0, len(mcq)):
    row = mcq.iloc[i]
    date_string = str(row['Average of Dates'])
    date_string = date_string[:10]
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    decimal_date = date_object.year + (date_object.timetuple().tm_yday - 1) / 365.25
    res.append(decimal_date)
mcq['Average of Dates'] = res

mcq = mcq[['#location', 'Average of Dates', 'D14C','1sigma_error']]
mcq = mcq.rename(columns={'#location': 'Site', 'Average of Dates': 'DecimalDate', '1sigma_error':'∆14Cerr','D14C':'∆14C'})
samples = pd.concat([samples, mcq])
# samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned.xlsx')

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
# # montes.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
# montes.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/monte_output.xlsx')


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

# samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/samples_with_references10000.xlsx')
# changing new output location to the EGU submission folder
# samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/samples_with_references10000_MCQ.xlsx')

neumayer_lat = -70.6666
neumayer_lon = -8.2667  # E
mcq_lat = -54.6208
mcq_lon = 158.8556  # E

lat_array = []
lon_array = []
for i in range(0, len(samples)):
    current_row = samples.iloc[i]
    if current_row['Site'] == 'NMY':
        lat_array.append(neumayer_lat)
        lon_array.append(neumayer_lon)
    elif current_row['Site'] == 'Macquarie_Isl.':
        lat_array.append(mcq_lat)
        lon_array.append(mcq_lon)
    elif current_row['Site'] == 'Eastbourne 1, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    elif current_row['Site'] == 'Eastbourne 2, NZ':
        lat_array.append(-41.2923)
        lon_array.append(174.8971)  # change Chilean Longitudes to degrees East.
    else:
        lat_array.append(current_row['Lat'])
        lon_array.append(current_row['Lon'])
samples['NewLat'] = lat_array
samples['NewLon'] = lon_array


samples['Country'] = -999  # Chile = 0, NZ = 1, NMY = 2
country_array = []
for i in range(0, len(samples)):
    current_row = samples.iloc[i]
    if current_row['NewLon'] > 90:
        country_array.append(1)
    elif 50 < current_row['NewLon'] < 90:
        country_array.append(0)
    elif current_row['NewLon'] < 0:
        country_array.append(2)
    else:
        x = 1
        # print(current_row)
samples['Country'] = country_array
samples = samples.drop_duplicates().reset_index(drop=True)

print(samples.columns)
samples = samples.rename(columns={'∆14C':'D14C_1'})
samples = samples.rename(columns = {'∆14Cerr':'weightedstderr_D14C_1'})
samples = samples.sort_values(by=['DecimalDate'])

"""
12/12/2023
Need to make the new plot to compare CMP and MCQ before I remove mcquarie island for the tree-ring plots. 
Even though the MCQ figure will be last
"""

from cmcrameri import cm
cmap=cm.davos
color_mcq = cm.lapaz(0.75)  # Lighter shade from batlow
color_cam = cm.lapaz(0.3)  # Darker shade from batlow

fig = plt.figure(figsize=(24, 8))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=.2, hspace=0.1)

ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

# copied from main analysis so the labels NZ_max/min are outdated but that OK for now
maxlat = -55
minlat = -45
nz_max_lon = 171
nz_min_lon = 158
ax1.set_extent([nz_min_lon, nz_max_lon, minlat, maxlat], crs=ccrs.PlateCarree())  # Set map extent
ax1.add_feature(cf.OCEAN)
ax1.add_feature(cf.LAND, edgecolor='black')
gl = ax1.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False



# COPIED FROM MAIN_ANALYSIS.PY
# The difference between the data, and REFERENCE 1, BHD with CGO in the gaps (WEIGHTED RESIDUAL)
samples['r3_diff_trend'] = samples['D14C_1'] - samples['D14C_ref3t_mean']
samples['r3_diff_trend_errprop'] = np.sqrt(samples['weightedstderr_D14C_1'] ** 2 + samples['D14C_ref3t_std'] ** 2)

mcq = samples.loc[samples['Site'] == 'Macquarie_Isl.']
cam = samples.loc[samples['Site'] == 'Campbell Island, NZ']

ax2.errorbar(mcq['DecimalDate'], mcq['D14C_1'], yerr=mcq['weightedstderr_D14C_1'], color=color_mcq, marker='o', label='Macquarie Island')
ax2.errorbar(cam['DecimalDate'], cam['D14C_1'], yerr=cam['weightedstderr_D14C_1'], color=color_cam, marker='D', label='Campbell Island')
ax2.set_xlim(1992, 2004)
ax2.set_ylim(62, 145)
ax2.set_ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')

ax3.errorbar(mcq['DecimalDate'], mcq['r3_diff_trend'], yerr=mcq['r3_diff_trend_errprop'], color=color_mcq, marker='o')
ax3.errorbar(cam['DecimalDate'], cam['r3_diff_trend'], yerr=cam['r3_diff_trend_errprop'], color=color_cam, marker='D')
ax3.set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
print('')
print('Is there a difference between Campbell Island and Macquarie Island? Null Hypothesis says: theres no difference!')
c = stats.ttest_ind(cam['r3_diff_trend'], mcq['r3_diff_trend'])
print(c)

ax3.set_xlim(1992, 2004)
ax3.set_ylim(-20, 20)

ax2.legend()
plt.savefig(
    f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/reviewer_MCQ_question/cmp_mcq.png',
    dpi=300, bbox_inches="tight")
plt.close()





