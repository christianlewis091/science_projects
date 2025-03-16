"""
Answering reviewer 3's Q about error bars in Figure 3.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

full_results = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/final_results.xlsx')
means = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/summary_means_January2_2025.xlsx', comment='#')

chile_full = full_results.loc[full_results['Country'] == 0].reset_index(drop=True)
chile_means = means.loc[means ['Country'] == 0].reset_index(drop=True)

nz_full = full_results.loc[full_results['Country'] == 1].reset_index(drop=True)
nz_means = means.loc[means ['Country'] == 1].reset_index(drop=True)

nz1_x = nz_means['Lat']
nz1_x = np.array(nz1_x)
nz1_y = nz_means['Mean']
nz1_y = np.array(nz1_y)

ch1_x = chile_means['Lat']
ch1_x = np.array(ch1_x)
ch1_y = chile_means['Mean']
ch1_y = np.array(ch1_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch1_x, ch1_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(nz1_x, nz1_y)

print("ChileMEANS: y=%.3fx+%.3f\R$^2$=%.3f__%.3f"%(slope, intercept,rvalue**2, pvalue))
print("NZMEANS: y=%.3fx+%.3f\R$^2$=%.3f__%.3f"%(sslope, sintercept,srvalue**2, spvalue))


# GETS "LOCS", LOCATIONS, WHILE PRESERVING LATITUDES IN PREVIOUSLY SORTED ORDER
# u, indices = np.unique(a, return_index=True) # https://numpy.org/doc/stable/reference/generated/numpy.unique.html
u1, locs1 = np.unique(chile_full['Site'], return_index=True)
temp = pd.DataFrame({"ind": u1, "locs":locs1}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs1 = temp['ind']
u2, locs2 = np.unique(nz_full['Site'], return_index=True)
temp2 = pd.DataFrame({"ind": u2, "locs":locs2}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs2 = temp2['ind']


# PREPARE THE FIGURE
# SELECT COLORS WE"LL USE FOR THE PAPER:
c1, c2, c3, c4, c5, c6, c7, c8 = '#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'
colors = [c1, c2, c3, c4, c5, c6, c7, c8]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']
size1 = 8



"""
Copy of NEW FIGURE 3 from Main Analysis 
"""

fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])

for i in range(0, len(locs1)):
    # PLOT THE MEAN
    slice = chile_means.loc[chile_means['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = np.unique(slice['Lat'])
    plt.errorbar(lat, slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

    #PLOT THE WHOLE DATA
    slice = chile_full.loc[chile_full['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.scatter(slice['Lat'], slice['r3_diff_trend'], alpha=.1, marker=markers[i], color=colors[i])
plt.plot(ch1_x, slope*ch1_x+intercept, color='black', alpha=0.25)

plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.xticks([], [])
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+2, 7, '[A] Chile', horizontalalignment='center', verticalalignment='center', fontweight="bold")

xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
for i in range(0, len(locs2)):
    # PLOT THE MEAN
    slice = nz_means.loc[nz_means['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = np.unique(slice['Lat'])
    plt.errorbar(lat, slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

    #PLOT THE WHOLE DATA
    slice = nz_full.loc[nz_full['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    print(locs2[i])
    print(slice)
    plt.scatter(slice['Lat'], slice['r3_diff_trend'], alpha=.1, marker=markers[i], color=colors[i])
plt.plot(nz1_x, sslope*nz1_x+sintercept, color='black', alpha=0.25)

plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Latitude (N)')
plt.text(-60+3.5, 7, '[B] New Zealand', horizontalalignment='center', verticalalignment='center', fontweight="bold")

plt.savefig(
    f'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Images_and_Figures/reviwer3_errorbar_question/New_Figure3_alldata.png',
    dpi=300, bbox_inches="tight")
plt.close()