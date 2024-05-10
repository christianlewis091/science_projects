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

        # radiocarbon mean data
        sub_results = {
            "Ocean Region": ocean[i],
            "Water Mass": watermasses[k],
            "DELC14_MEAN": np.average(this_water_mass['DELC14']),
            "DELC14_STD": np.std(this_water_mass['DELC14'])}
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

results = pd.DataFrame(results_list)
results.to_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS.xlsx')