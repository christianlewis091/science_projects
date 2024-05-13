import pandas as pd
import gsw
import pandas.errors
from os import listdir
from os.path import isfile, join
import numpy as np
import seawater
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

df = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP3_data_workup/STEP3_WATER_MASSES_ASSIGNED.xlsx')
df = df.loc[df['DELC14'] > -998]

ocean = np.unique(df['OCEAN_LABEL'].astype(str))

# re import the metadata so that we can add the minimum and max potential density anomalies on top
wmc_Talley = pd.read_excel(f'H:\Science\Datasets\Water_Mass_Characteristics.xlsx',sheet_name='Talley', skiprows=1, comment='#')

results_list = []
# loop creating plots for each ocean
for i in range(0, len(ocean)):
    this_ocean = df.loc[df['OCEAN_LABEL'] == ocean[i]]
    watermasses = np.unique(this_ocean['Tally_assigned'])

    # sub loop creates plot for each water mass
    for k in range(0, len(watermasses)):
        this_water_mass = this_ocean.loc[this_ocean['Tally_assigned'] == watermasses[k]]
        metadata = wmc_Talley.loc[(wmc_Talley['Talley Label'] == ocean[i]) & (wmc_Talley['Name'] == watermasses[k])].reset_index(drop=True)
        roe_min = metadata['roe min']
        roe_min = roe_min[0]

        roe_max = metadata['roe max']
        roe_max = roe_max[0]

        # I'm going to find the global mean, but I also want to find the mean by decade...
        nineties = this_water_mass.loc[(this_water_mass['DATE'] >= 19900000) & (this_water_mass['DATE'] < 20000000)]
        aughts = this_water_mass.loc[(this_water_mass['DATE'] >= 20000000) & (this_water_mass['DATE'] < 20100000)]
        tens = this_water_mass.loc[(this_water_mass['DATE'] >= 20100000) & (this_water_mass['DATE'] < 20200000)]

        # radiocarbon mean data
        sub_results = {
            "Ocean Region": ocean[i],
            "Water Mass": watermasses[k],
            "DELC14_MEAN_ALL": np.average(this_water_mass['DELC14']),
            "DELC14_STD_ALL": np.std(this_water_mass['DELC14']),
            "DELC14_MEAN_1990s": np.average(nineties['DELC14']),
            "DELC14_STD_1990s": np.std(nineties['DELC14']),
            "DELC14_MEAN_2000s": np.average(aughts['DELC14']),
            "DELC14_STD_2000s": np.std(aughts['DELC14']),
            "DELC14_MEAN_2010s": np.average(tens['DELC14']),
            "DELC14_STD_2010s": np.std(tens['DELC14']),
            "roe_min": roe_min,
            "roe_max": roe_max,
        }

        results_list.append(sub_results)

        fig = plt.figure(figsize=(12, 5))
        gs = gridspec.GridSpec(2, 3)
        gs.update(wspace=0.3, hspace=0.35)

        xtr_subsplot = fig.add_subplot(gs[0:2, 1:3])

        plt.scatter(this_water_mass['LATITUDE'],this_water_mass['CTDPRS'], c=this_water_mass['DELC14'], vmin=-500, vmax=150)
        plt.ylim(6000, 0)
        plt.xlim(-90, 90)
        plt.xlabel('Latitude N')
        plt.ylabel('CTDPRS')
        plt.title(f'{ocean[i]} Ocean, {watermasses[k]},\u03C3$_\u03B8$ >={roe_min} & < {roe_max}')
        plt.colorbar(label = '\u0394$^1$$^4$C (\u2030)')

        xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])

        maxlat = 90
        minlat = -90
        max_lon = 180
        min_lon = -180

        map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
        map.etopo()
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
        map.drawmeridians(np.arange(-180, 180, 60), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)

        # grab its lats and lons
        lats = this_water_mass['LATITUDE']
        lons = this_water_mass['LONGITUDE']

        z, a = map(lons,  lats)
        map.scatter(z, a, marker='o', s = 3.5, color='yellow', edgecolor='yellow')

        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/{ocean[i]}_{watermasses[k]}.jpg', dpi=300, bbox_inches="tight")
        plt.close()


results1 = pd.DataFrame(results_list)
# results1.to_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS.xlsx')

"""
REPEAT THE ABOVE BUT USE THE SECOND LABEL. This will give us the statistics regarding the Southern Ocean by 3 basin sectors, and the arctic. 
"""

ocean = np.unique(df['OCEAN_LABEL_2'].astype(str))

results_list = []
# loop creating plots for each ocean
for i in range(0, len(ocean)):
    this_ocean = df.loc[df['OCEAN_LABEL_2'] == ocean[i]]
    watermasses = np.unique(this_ocean['Tally_assigned'])

    # sub loop creates plot for each water mass
    for k in range(0, len(watermasses)):
        this_water_mass = this_ocean.loc[this_ocean['Tally_assigned'] == watermasses[k]]

        # I'm going to find the global mean, but I also want to find the mean by decade...
        nineties = this_water_mass.loc[(this_water_mass['DATE'] >= 19900000) & (this_water_mass['DATE'] < 20000000)]
        aughts = this_water_mass.loc[(this_water_mass['DATE'] >= 20000000) & (this_water_mass['DATE'] < 20100000)]
        tens = this_water_mass.loc[(this_water_mass['DATE'] >= 20100000) & (this_water_mass['DATE'] < 20200000)]

        # radiocarbon mean data
        sub_results = {
            "Ocean Region": ocean[i],
            "Water Mass": watermasses[k],
            "DELC14_MEAN_ALL": np.average(this_water_mass['DELC14']),
            "DELC14_STD_ALL": np.std(this_water_mass['DELC14']),
            "DELC14_MEAN_1990s": np.average(nineties['DELC14']),
            "DELC14_STD_1990s": np.std(nineties['DELC14']),
            "DELC14_MEAN_2000s": np.average(aughts['DELC14']),
            "DELC14_STD_2000s": np.std(aughts['DELC14']),
            "DELC14_MEAN_2010s": np.average(tens['DELC14']),
            "DELC14_STD_2010s": np.std(tens['DELC14'])
        }

        results_list.append(sub_results)

        fig = plt.figure(figsize=(12, 5))
        gs = gridspec.GridSpec(2, 3)
        gs.update(wspace=0.3, hspace=0.35)

        xtr_subsplot = fig.add_subplot(gs[0:2, 1:3])

        plt.scatter(this_water_mass['LATITUDE'],this_water_mass['CTDPRS'], c=this_water_mass['DELC14'], vmin=-500, vmax=150)
        plt.ylim(6000, 0)
        plt.xlim(-90, 90)
        plt.xlabel('Latitude N')
        plt.ylabel('CTDPRS')
        plt.title(f'{ocean[i]} Ocean, {watermasses[k]},\u03C3$_\u03B8$ >={roe_min} & < {roe_max}')
        plt.colorbar(label = '\u0394$^1$$^4$C (\u2030)')

        xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])

        maxlat = 90
        minlat = -90
        max_lon = 180
        min_lon = -180

        map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=min_lon, urcrnrlon=max_lon)
        map.etopo()
        map.drawcoastlines()
        map.drawparallels(np.arange(-90, 90, 30), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
        map.drawmeridians(np.arange(-180, 180, 60), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)

        # grab its lats and lons
        lats = this_water_mass['LATITUDE']
        lons = this_water_mass['LONGITUDE']

        z, a = map(lons,  lats)
        map.scatter(z, a, marker='o', s = 3.5, color='yellow', edgecolor='yellow')

        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/{ocean[i]}_{watermasses[k]}.jpg', dpi=300, bbox_inches="tight")
        plt.close()


results2 = pd.DataFrame(results_list)
results = pd.concat([results1, results2])
results.to_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS.xlsx')


"""
I want to see the results over time 
"""
import seaborn as sns
colors2 = sns.color_palette("mako", 7)
colors2= list(reversed(colors2))


results = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS.xlsx')

"""
I want to see how the D14C for the Different Southern Ocean basins are changing over time. However, currently, 
the pot. density anomaly min and max are only set for the Southern OCean as a whole. Im just going to manually assign the values to the correct rows below. 
"""

results.loc[(results['Water Mass'] == 'Layer 10'), 'roe_min'] = 26.1
results.loc[(results['Water Mass'] == 'Layer 10'), 'roe_max'] = 26.4
results.loc[(results['Water Mass'] == 'Layer 11_AAIW'), 'roe_min'] = 26.4
results.loc[(results['Water Mass'] == 'Layer 11_AAIW'), 'roe_max'] = 26.9
results.loc[(results['Water Mass'] == 'Layer 16'), 'roe_min'] = 27.4
results.loc[(results['Water Mass'] == 'Layer 16'), 'roe_max'] = 36.8
results.loc[(results['Water Mass'] == 'Layers 12_13'), 'roe_min'] = 26.9
results.loc[(results['Water Mass'] == 'Layers 12_13'), 'roe_max'] = 27.1
results.loc[(results['Water Mass'] == 'Layers 14-15'), 'roe_min'] = 27.1
results.loc[(results['Water Mass'] == 'Layers 14-15'), 'roe_max'] = 27.4
results.loc[(results['Water Mass'] == 'Layers 1_9_Upper Ocean'), 'roe_min'] = 0
results.loc[(results['Water Mass'] == 'Layers 1_9_Upper Ocean'), 'roe_max'] = 26.1

# results.to_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS_EDITED.xlsx')

# better to make a function than repeating this for ages below.
def plotting_func(input1, sel_xticks=None, sel_yticks=None):
    subdf = results.loc[results['Ocean Region'] == input1].reset_index(drop=True)
    subdf = subdf.sort_values(by='roe_min')
    for i in range(0, len(subdf)):
        row = subdf.iloc[i]
        roe_max = row['roe_max']
        x = [1990, 2000, 2010]
        y = [row['DELC14_MEAN_1990s'],
             row['DELC14_MEAN_2000s'],
             row['DELC14_MEAN_2010s']]
        errbar = [row['DELC14_STD_1990s'],
                  row['DELC14_STD_2000s'],
                  row['DELC14_STD_2010s']]

        lab = row['Water Mass']
        plt.errorbar(x,y, errbar, label=f'\u03C3$_\u03B8$ {roe_max}', color=colors2[i])
        plt.title(f'{input1}')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.ylim(-250, 150)
        plt.scatter(x,y, color=colors2[i])
        if sel_xticks == 'off':
            plt.xticks([], [])
        if sel_yticks == 'off':
            plt.yticks([], [])

fig = plt.figure(1, figsize=(12, 9))
gs = gridspec.GridSpec(3, 3)
gs.update(wspace=.6, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
plotting_func('North Atlantic', sel_xticks='off')

xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
plotting_func('South Atlantic', sel_xticks='off')
plt.ylabel('\u0394$^1$$^4$C (\u2030)')

xtr_subsplot = fig.add_subplot(gs[2:3, 0:1])
plotting_func('Southern - Atlantic Sector')

xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plotting_func('North Pacific', sel_xticks='off', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
plotting_func('South Pacific', sel_xticks='off', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[2:3, 1:2])
plotting_func('Southern - Pacific Sector', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[1:2, 2:3])
plotting_func('Indian', sel_xticks='off', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[2:3, 2:3])
plotting_func('Southern - Indian Sector', sel_yticks='off')

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY.jpg', dpi=300, bbox_inches="tight")
