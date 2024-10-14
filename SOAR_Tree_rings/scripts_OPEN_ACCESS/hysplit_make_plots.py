"""
This file is created october 5, 2023. Trynig to replot the hypsplit data a bit more simply now that I hvae more knowledge.

"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec

# READ IN SOME EXCEL DATA
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
# landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data//landfracresults.xlsx')
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# points1 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2005_2006.xlsx')
# points2 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2010_2011.xlsx')
# points3 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2015_2016.xlsx')
# points4 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2020_2021.xlsx')
# points = pd.concat([points1, points2, points3, points4])
# points.to_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_make_plots/points_concat.csv')
points = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_make_plots/points_concat.csv')
# we only want trajectories that launch at 100m
points = points.loc[points['starting_height'] == 100]

#JCT Comment: how many runs are there explicity:count
count1 = points.loc[points['location'] == 'Nikau']
count1 = np.unique(count1['filename'])
print('Count')
print(len(count1))
print()
#clarify some acc fronts stuff
fronts = np.unique(acc_fronts['front_name'])
fronts = ['PF','SAF','STF','Boundary']
line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
size1 = 5
means_concat = pd.DataFrame()
for i in range(0, len(easy_access)):
    row = easy_access.iloc[i]
    country_code = row['Code']
    codename = row['Codename']
    sitename = row['Site']
    this_site_points = points.loc[points['location'] == codename]

    fig = plt.figure(figsize=(4, 8))
    m = Basemap(projection='cyl', resolution='c', llcrnrlat=-90, urcrnrlat=0, llcrnrlon=-180, urcrnrlon=180)
    m.drawmapboundary(fill_color='lightgrey')
    m.fillcontinents(color='darkgrey')
    m.shadedrelief()
    m.drawcoastlines(linewidth=0.1)

    lats = this_site_points['y']
    lons = this_site_points['x']
    a, b = m(lons, lats)
    m.scatter(a, b, color='dodgerblue', s=size1)

    # find the mean trajectory at every time-point.
    site_mean = this_site_points.groupby('timestep').mean()
    site_mean['location'] = sitename
    means_concat = pd.concat([means_concat, site_mean])
    lats = site_mean['y']
    lons = site_mean['x']
    a, b = m(lons, lats)
    m.scatter(a, b, color='red', s=size1)

    for q in range(0, len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[q]]
        latitudes = this_one['latitude']
        longitudes = this_one['longitude']
        x, y = m(longitudes.values, latitudes.values)
        m.plot(x, y, color='black', label=f'{fronts[q]}', linestyle=line_sys[q])

    m.drawparallels(np.arange(-90, 90, 10), labels=[True, False, False, False], fontsize=7, linewidth=0.5)
    m.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
    plt.title(f'{codename}')
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_make_plots/{codename}.png',
                dpi=300, bbox_inches="tight")
    plt.close()


    fig = plt.figure(figsize=(4, 8))
    m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
    m.drawmapboundary(fill_color='lightgrey')
    m.fillcontinents(color='darkgrey')
    m.shadedrelief()
    m.drawcoastlines(linewidth=0.1)

    lats = this_site_points['y']
    lons = this_site_points['x']
    a, b = m(lons, lats)
    m.scatter(a, b, color='dodgerblue', s=size1)

    # find the mean trajectory at every time-point.
    site_mean = this_site_points.groupby('timestep').mean()
    lats = site_mean['y']
    lons = site_mean['x']
    a, b = m(lons, lats)
    m.scatter(a, b, color='red', s=size1)

    for q in range(0, len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[q]]
        latitudes = this_one['latitude']
        longitudes = this_one['longitude']
        x, y = m(longitudes.values, latitudes.values)
        m.plot(x, y, color='black', label=f'{fronts[q]}', linestyle=line_sys[q])


    m.drawmeridians(np.arange(-180, 180, 10), labels=[1, 1, 0, 1], fontsize=7, linewidth=0.5)
    plt.title(f'{codename}')
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_make_plots/{codename}_orthographic.png',
                dpi=300, bbox_inches="tight")
    plt.close()

means_concat.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_make_plots/means_concat.xlsx')



