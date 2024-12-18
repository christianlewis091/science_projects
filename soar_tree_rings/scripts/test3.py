import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap


"""
MAPP OF ACC FRONTS
"""
# LOAD HYSPLOT DATA
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/easy_access2 - Copy.xlsx')
means_dataframe_100 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_2005_2006.xlsx')  # TODO ADD OTHER YEARS (not only 05-06)
# ADDING PROPER SITE NAMES FOR THE FOLLOWING LOOP TO READ
means_dataframe_100 = means_dataframe_100.merge(easy_access)

# SEE hysplit_make_plots_GNS.py
timemin = -(6*24)
means_dataframe_100 = means_dataframe_100.loc[means_dataframe_100['timestep'] > timemin]
sites = np.unique(means_dataframe_100['Site'])

# LOAD ACC FRONTS DATA
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
fronts = np.unique(acc_fronts['front_name'])

# fronts = ['PF','SAF','STF']
map = Basemap(llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='l')
# map = Basemap(projection='ortho',lon_0=-105,lat_0=-90,resolution='l')
map.drawmapboundary(fill_color='lightgrey')
map.fillcontinents(color='darkgrey')
map.drawcoastlines(linewidth=0.1)
# #
# PLOTTING THE ACC FRONTS
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#
#     chile_lat = this_one['latitude']
#     chile_lon = this_one['longitude']
#
#     z, a = map(list(chile_lon), list(chile_lat))
#
#     map.plot(z, a, color='black', label=f'{fronts[i]}')

# PLOTTING CHILEAN SITES
for i in range(0, len(sites)):
    site_mean_100 = means_dataframe_100.loc[means_dataframe_100['Site'] == str(sites[i])].reset_index(drop=True)
    y_mean, x_mean = (site_mean_100['y'], site_mean_100['x'])
    print(y_mean)
    print(x_mean)
    map.scatter(x_mean, y_mean, color='darkred', alpha=1)


plt.show()
