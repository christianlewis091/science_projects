"""
Adding some extra analysis of the HYSPLIT DATA for the results section

"""
import pandas as pd
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt

landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data//landfracresults.xlsx')
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
easy_access_CH = easy_access.loc[easy_access['Code'] == 'CH'].sort_values(by='NewLat', ascending=False).reset_index(drop=True)
easy_access_NZ = easy_access.loc[easy_access['Code'] == 'NZ'].sort_values(by='NewLat', ascending=False).reset_index(drop=True)
codenames_CH = easy_access_CH['Codename']
codenames_NZ = easy_access_NZ['Codename']
#
# codenames = easy_access['Codename']
# code = easy_access['Code']
# lat = easy_access['NewLat']
# lon = easy_access['ChileFixLon']

year = ['2005_2006', '2010_2011','2015_2016','2020_2021']
means_dataframe_100_56 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2005_2006.xlsx')
means_dataframe_100_1011 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2010_2011.xlsx')
means_dataframe_100_1516 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2015_2016.xlsx')
means_dataframe_100_2021 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2020_2021.xlsx')

# for every site, we want to plot the average height over time

fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 4)
gs.update(wspace=0.1, hspace=0.15)

xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])

for i in range(0,len(codenames_CH)):
    site = means_dataframe_100_56.loc[means_dataframe_100_56['Codename'] == codenames_CH[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_CH[i]}')
    plt.xticks([])
    plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])

for i in range(0,len(codenames_CH)):
    site = means_dataframe_100_1011.loc[means_dataframe_100_1011['Codename'] == codenames_CH[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_CH[i]}')
    plt.yticks([])
    plt.xticks([])
    plt.legend()


xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])

for i in range(0,len(codenames_CH)):
    site = means_dataframe_100_1516.loc[means_dataframe_100_1516['Codename'] == codenames_CH[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_CH[i]}')
    plt.yticks([])
    plt.xticks([])
    plt.legend()

xtr_subsplot = fig.add_subplot(gs[0:1, 3:4])

for i in range(0,len(codenames_CH)):
    site = means_dataframe_100_2021.loc[means_dataframe_100_2021['Codename'] == codenames_CH[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_CH[i]}')
    plt.yticks([])
    plt.xticks([])
    plt.legend()


xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])

for i in range(0,len(codenames_NZ)):
    site = means_dataframe_100_56.loc[means_dataframe_100_56['Codename'] == codenames_NZ[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_NZ[i]}')
    plt.legend()

xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])

for i in range(0,len(codenames_NZ)):
    site = means_dataframe_100_1011.loc[means_dataframe_100_1011['Codename'] == codenames_NZ[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_NZ[i]}')
    plt.yticks([])
    plt.legend()

xtr_subsplot = fig.add_subplot(gs[1:2, 2:3])

for i in range(0,len(codenames_NZ)):
    site = means_dataframe_100_1516.loc[means_dataframe_100_1516['Codename'] == codenames_NZ[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_NZ[i]}')
    plt.yticks([])
    plt.legend()

xtr_subsplot = fig.add_subplot(gs[1:2, 3:4])

for i in range(0,len(codenames_NZ)):
    site = means_dataframe_100_2021.loc[means_dataframe_100_2021['Codename'] == codenames_NZ[i]].reset_index(drop=True)
    plt.plot(site['timestep'], site['z'], label=f'{codenames_NZ[i]}')
    plt.yticks([])
    plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis2/altitude_summary.png',
            dpi=300, bbox_inches="tight")
plt.close()




"""
Copied the code below from Glodap Overlay to calculate time-integrated means of hysplit output 
"""
means_dataframe_100_1 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2005_2006.xlsx')
means_dataframe_100_2 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2010_2011.xlsx')
means_dataframe_100_3 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2015_2016.xlsx')
means_dataframe_100_4 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2020_2021.xlsx')

means_dataframe_100 = pd.concat([means_dataframe_100_1, means_dataframe_100_2, means_dataframe_100_3, means_dataframe_100_4])
codenames = np.unique(means_dataframe_100['Codename'])
time_integrated_means = pd.DataFrame()

std_arr = []
for i in range(0,len(codenames)):

    # LOCATE FIRST SITE
    site1 = means_dataframe_100.loc[means_dataframe_100['Codename'] == codenames[i]]
    means1 = site1.groupby('timestep', as_index=False).mean()
    std1 = site1.groupby('timestep', as_index=False).std()
    means1['Codename'] = codenames[i]
    time_integrated_means = pd.concat([time_integrated_means, means1]).reset_index(drop=True)

ends = time_integrated_means.loc[time_integrated_means['timestep'] == -168]
merged = ends.merge(easy_access)
merged['LatDiff'] = merged['y'] - merged['NewLat']
merged['LonDiff'] = merged['x'] - merged['NewLon']
# merged.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis2/lat_difference.xlsx')
import scipy
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(merged['NewLat'], merged['LatDiff'])
print(r_value)
plt.scatter(merged['NewLat'], merged['LatDiff'])
plt.show()























