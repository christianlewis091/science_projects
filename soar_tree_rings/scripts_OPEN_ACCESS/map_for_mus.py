"""
Mus wants some advice about where to get air samples collected. I want to make a map of the NZ oceanic fronts
quickly
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap

# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
#
# maxlat = -30
# minlat = -90
# nz_max_lon = 200
# nz_min_lon = 100
# chile_max_lon = -55
# chile_min_lon = -85
# res = 'l'
#
# fig = plt.figure(figsize=(12, 12))
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# m = Basemap(projection='spstere', boundinglat=-30, lon_0=180, resolution='l')
#
# # Draw coastlines, countries, and parallels/meridians
# m.drawcoastlines()
# m.drawcountries()
# m.drawparallels(range(-90, 0, 10),labels=[False,True,True,False])
# m.drawmeridians(range(-180, 180, 30),labels=[True,False,False,True])
# m.drawmapboundary(fill_color='lightgrey')
# m.fillcontinents(color='darkgrey')
# m.drawcoastlines(linewidth=0.1)
# m.shadedrelief()
#
#
# for g in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[g]]
#     latitudes = this_one['latitude']
#     longitudes = this_one['longitude']
#     x, y = m(longitudes.values, latitudes.values)
#     m.plot(x, y, color='black', label=f'{fronts[g]}', linestyle=line_sys[g])
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/map_for_mus/map.png',
#             dpi=300, bbox_inches="tight")
#

"""
histogram of where sampling has happened in the past
"""

df = pd.read_excel(r'H:/Science/Datasets/SOE_BB_updateJan2024.xlsx', sheet_name='New values to use').dropna(subset='Latitude')

# Example data: replace this with your actual latitude data
latitudes = df['Latitude'].astype(float)  # Generating random latitudes for demonstration

# Define the bins (ranges of 5 degrees)
bins = np.arange(-90, 95, 5)  # From -90 to 90 with steps of 5

# Create the histogram
plt.hist(latitudes, bins=bins, edgecolor='black')

# Add labels and title
plt.xlabel('Latitude (degrees)')
plt.ylabel('Frequency')
plt.title('Histogram of Data by Latitude')
plt.xlim(-90, -30)

# Show the plot
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/map_for_mus/hist.png',
             dpi=300, bbox_inches="tight")








