import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from X_miller_curve_algorithm import ccgFilter
import time
import openpyxl
start_time = time.time()

"""
Block 1: Takes 262 seconds (4 minutes) to run
"""
# # READ IN SOME EXCEL DATA
# easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
# landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data//landfracresults.xlsx')
# points1 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2005_2006.xlsx')
# points2 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2010_2011.xlsx')
# points3 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2015_2016.xlsx')
# points4 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_2020_2021.xlsx')
# points = pd.concat([points1, points2, points3, points4])
# points = points.loc[points['starting_height'] == 100]
# # #
# points.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/points_concat.xlsx')
# elapsed_time_section_1 = time.time() - start_time
# print(f"Code section 1 took {elapsed_time_section_1} seconds")
#

"""
Block 2
"""
points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/points_concat.xlsx')
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
elapsed_time_section_1 = time.time() - start_time
locations = np.unique(points['location'])

for q in range(0, len(locations)):

    # filter by location
    midpoint_lat = []
    midpoint_lon = []
    loc_len = []
    name = []
    this_loc = points.loc[points['location'] == locations[q]]

    lons = np.linspace(-180, 180, 361)
    lats = np.linspace(-90,90, 181)

    for i in range(0, len(lons)-1):
        for j in range(0, len(lats)-1):
            midpoint_lon.append((lons[i]+lons[i+1])/2)
            midpoint_lat.append((lats[j]+lats[j+1])/2)

            subdata = this_loc.loc[(this_loc['x'] > lons[i]) & (this_loc['x'] <= lons[i+1]) &
                                   (this_loc['y'] > lats[j]) & (this_loc['y'] <= lats[j+1])]

            loc_len.append(len(subdata))
            name.append(locations[q])
            # print(f'{locations[q]}, {lons[i]}, {lats[j]}')

    results = pd.DataFrame({"location": name, "x": midpoint_lon, "y": midpoint_lat, "heat": loc_len})
    results = results.loc[results['heat'] != 0]

    fig = plt.figure(figsize=(4, 8))
    m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
    m.drawmapboundary(fill_color='lightgrey')
    m.fillcontinents(color='darkgrey')
    m.shadedrelief()
    m.drawcoastlines(linewidth=0.1)

    a, b = m(results['x'], results['y'])
    m.scatter(a, b, c=results['heat'], cmap='coolwarm', s=5, linewidth=0.5, vmin=0, vmax=32, alpha=0.5)

    fronts = np.unique(acc_fronts['front_name'])
    fronts = ['PF','SAF','STF','Boundary']
    line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']

    for g in range(0, len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[g]]
        latitudes = this_one['latitude']
        longitudes = this_one['longitude']
        x, y = m(longitudes.values, latitudes.values)
        m.plot(x, y, color='black', label=f'{fronts[g]}', linestyle=line_sys[g])
        plt.colorbar()

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/{locations[q]}_cbar.png',
            dpi=300, bbox_inches="tight")
#
#
"""
Recalculating the "Time Per Zone" using points, not means
"""
# n = 3 # set the amount of times the code will iterate (set to 10,000 once everything is final)
# cutoff = 667  # FFT filter cutoff
#
# # Do this for each front
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# # create a smoothed front
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     latitudes = this_one['latitude'].reset_index(drop=True)
#     longitudes = this_one['longitude'].reset_index(drop=True)
#     yerr = latitudes*.01
#
#     #dynamically name a variable
#     # GET SMOOTH VALUE: SET OUTPUT TO WHEREVER WE LAVE LONGUITUDE DATA FOR THE MEANS
#     smoothed = ccgFilter(longitudes, latitudes, cutoff).getSmoothValue(points['x'])
#     points[f'{fronts[i]}+smoothed'] = smoothed
#
# result_array = []
# for j in range(0, len(points)):
#     row = points.iloc[j]
#     # assign label based on latitude
#     if (row['y'] >= row['STF+smoothed']):
#         res = 'STZ'
#     elif (row['y'] >= row['Boundary+smoothed']) & (row['y'] <= row['PF+smoothed']):
#         res = 'ASZ'
#     elif (row['y'] >= row['PF+smoothed']) & (row['y'] <= row['SAF+smoothed']):
#         res = 'PFZ'
#     elif (row['y'] >= row['SAF+smoothed']) & (row['y'] <= row['STF+smoothed']):
#         res = 'SAZ'
#     elif (row['y'] <= row['Boundary+smoothed']):
#         res = 'SIZ'
#     else:
#         res = 'Error'
#
#     result_array.append(res)
#
# points['zones'] = result_array
# points.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/test.xlsx')
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/test.xlsx')
#
# zones = np.unique(points['zones'])
# sites = np.unique(points['location'])
#
# out1 = []
# out2 = []
# out3 = []
#
# for i in range(0, len(sites)):
#     this_site = points.loc[points['location'] == sites[i]]
#     for u in range(0, len(zones)):
#         how_many = this_site.loc[this_site['zones'] == zones[u]]
#         out1.append(sites[i])
#         out2.append(zones[u])
#         out3.append(len(how_many))
# output1 = pd.DataFrame({"Site": out1, "Zone": out2, "Length": out3})
# print(output1)
# output1.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/time_per_zone_usingpoints.xlsx')
#

"""
Sara M. Fletcher mentioned in our group meeting on June 20, 2024 that it would be nice to have this graphically displayed rather than
just as a table. Lets see if we can do that below. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read the data from the Excel file
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/time_per_zone_usingpoints_edited.xlsx', sheet_name='Summary')

df = df.rename(columns={"STZ": "Subtropical Zone",
                 "SAZ": "Subantarctic Zone",
                 "PFZ": "Polar Frontal Zone",
                 "ASZ": "Antarctic-Southern Zone",
                 "SIZ": "Sea Ice Zone"})

zones = ["Subtropical Zone", "Subantarctic Zone", "Polar Frontal Zone", "Antarctic-Southern Zone", "Sea Ice Zone"]
zone_trans = [0.2, 0.2, 1,1,1]
sites = df['Site']

# Define the color palette
colors = sns.color_palette("muted", len(zones))

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

# Initialize the bottom array for the first stack
bottom = np.zeros(len(sites))

# Loop through each zone to create a stacked bar
for i, zone in enumerate(zones):
    ax.bar(sites, df[zone], bottom=bottom, label=zone, color=colors[i], alpha=zone_trans[i])
    bottom += df[zone].values  # Update the bottom to include the current zone's height

# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Site')
ax.set_ylabel('Percent')
ax.set_title('Percent of Back-Trajectory Spent in Each Zone')
ax.set_xticks(np.arange(len(sites)))
ax.set_xticklabels(sites, rotation=45)
ax.legend()

# Show the plot
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/stackedbar.png', dpi=300, bbox_inches="tight")

plt.close()

