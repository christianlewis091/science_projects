import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.gridspec as gridspec
import time
import openpyxl
start_time = time.time()
import cartopy.crs as ccrs
import cartopy.feature as cf

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
# #

"""
Block 2
"""
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/points_concat.xlsx')
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
#
# locations = np.unique(points['location'])
#
# for q in range(0, len(locations)):
#
#     # filter by location
#     midpoint_lat = []
#     midpoint_lon = []
#     loc_len = []
#     name = []
#     this_loc = points.loc[points['location'] == locations[q]]
#
#     lons = np.linspace(-180, 180, 361)
#     lats = np.linspace(-90,90, 181)
#
#     for i in range(0, len(lons)-1):
#         for j in range(0, len(lats)-1):
#             midpoint_lon.append((lons[i]+lons[i+1])/2)
#             midpoint_lat.append((lats[j]+lats[j+1])/2)
#
#             subdata = this_loc.loc[(this_loc['x'] > lons[i]) & (this_loc['x'] <= lons[i+1]) &
#                                    (this_loc['y'] > lats[j]) & (this_loc['y'] <= lats[j+1])]
#
#             loc_len.append(len(subdata))
#             name.append(locations[q])
#             # print(f'{locations[q]}, {lons[i]}, {lats[j]}')
#
#     results = pd.DataFrame({"location": name, "x": midpoint_lon, "y": midpoint_lat, "heat": loc_len})
#     results = results.loc[results['heat'] != 0]
#
#     # Create a figure
#     plt.figure(figsize=(10, 10))
#     ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
#
#     # First Subplot: Nitrate Map
#     ax.add_feature(cf.OCEAN)
#     ax.add_feature(cf.LAND, edgecolor='black')
#     ax.gridlines()
#
#     fronts = np.unique(acc_fronts['front_name'])
#     fronts = ['PF', 'SAF', 'STF', 'Boundary']
#     line_sys = ['dotted', 'dashed', 'dashdot', 'solid']
#
#     # Loop through each front and plot
#     for i in range(len(fronts)):
#         this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#         latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
#         longitudes = this_one['longitude'].values
#
#         # Plot the data, making sure to specify the correct CRS for input data
#         ax.plot(
#             longitudes,
#             latitudes,
#             transform=ccrs.PlateCarree(),  # Data is in lat/lon format
#             linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
#             label=fronts[i], color='black')
#
#         # Plot the HEATMAP on top of the ORSI lines
#     ax.scatter(
#         results['x'].values,
#         results['y'].values,
#         c=results['heat'].values, cmap='coolwarm', s=5, linewidth=0.5, vmin=0, vmax=32, alpha=0.9, transform=ccrs.PlateCarree())  # Data is in lat/lon format))
#
#     # Show the plot
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/{locations[q]}.png',
#                 dpi=300, bbox_inches="tight")
# # #
"""
THE CODE BLOCK ABOVE SHOWS THAT THE HEATMAPS STILL LOOK OK!
"""

"""
Smooth the ORSI cruves to match longitudes of our data
"""

# reference = pd.DataFrame()
# reference['x'] = points['x']  # SMOOTH ORSI TO POINTS LONGITUDES
#
# # Iterate over each front
# fronts = acc_fronts['front_name'].unique()
# for front in fronts:
#     # Extract latitude and longitude for the current front
#     this_one = acc_fronts[acc_fronts['front_name'] == front]
#     front_longitudes = this_one['longitude'].values
#     front_latitudes = this_one['latitude'].values
#
#     # Ensure the front data is sorted by longitude
#     sorted_indices = np.argsort(front_longitudes)
#     front_longitudes = front_longitudes[sorted_indices]
#     front_latitudes = front_latitudes[sorted_indices]
#
#     # Interpolate the front latitudes to match the longitudes of the data
#     smoothed_latitudes = np.interp(reference['x'], front_longitudes, front_latitudes)
#
#     # Add interpolated latitudes as a new column in the data
#     reference[f'{front}_smoothed_LAT'] = smoothed_latitudes
#
#     # Optional: Plot if required
#     plt.figure(figsize=(10, 10))
#     ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
#
#     # First Subplot: Nitrate Map
#     ax.add_feature(cf.OCEAN)
#     ax.add_feature(cf.LAND, edgecolor='black')
#     ax.gridlines()
#     ax.set_title(f'{front}')
#
#     fronts = np.unique(acc_fronts['front_name'])
#     fronts = ['PF', 'SAF', 'STF', 'Boundary']
#     line_sys = ['dotted', 'dashed', 'dashdot', 'solid']
#
#     # Loop through each front and plot
#     for i in range(len(fronts)):
#         this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#         latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
#         longitudes = this_one['longitude'].values
#
#         # Plot the data, making sure to specify the correct CRS for input data
#         ax.plot(
#             longitudes,
#             latitudes,
#             transform=ccrs.PlateCarree(),  # Data is in lat/lon format
#             linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
#             label=fronts[i], color='black')
#
#     ax.scatter(
#         reference['x'],
#         smoothed_latitudes,
#         transform=ccrs.PlateCarree(),  # Data is in lat/lon format
#         linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
#         label=fronts[i], color='red')
#
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/{front}.png', dpi=300, bbox_inches="tight")
#     plt.close()
#
# # here is the dataframe of the smoothed fronts, on the sampled longitudes
# reference.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/smoothed_fronts_sample_lons.xlsx')

"""
Merge the Reference's smoothed ORSU fronts with sample longitudes
"""
# import pandas as pd
# reference = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/smoothed_fronts_sample_lons.xlsx')
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/points_concat.xlsx')
#
# reference = reference.sort_values(by=['x'])
# points = points.sort_values(by=['x'])
#
# points['STF_smoothed_LAT'] = reference['STF_smoothed_LAT']
# points['SAF_smoothed_LAT'] = reference['SAF_smoothed_LAT']
# points['PF_smoothed_LAT'] = reference['PF_smoothed_LAT']
# points['Boundary_smoothed_LAT'] = reference['Boundary_smoothed_LAT']
# points['ref_x'] = reference['x']
# points['test'] = points['ref_x'] - reference['x'] # I need to assign latitude bands for the fronts, for each longitude. if the right bands have been assigned, the difference in longitudes will be 0
# print(points['test'])
#
# """
# NOW,
# I WANT TO PUT THE DATA INTO BINS, OF FRONT, AND OCEAN ZONE
# """
#
# points.loc[(points['y'] >= points['STF_smoothed_LAT']), 'Assigned Zone'] = 'STZ'
# points.loc[(points['y'] >= points['SAF_smoothed_LAT']) & (points['y'] <= points['STF_smoothed_LAT']), 'Assigned Zone'] = 'SAZ'
# points.loc[(points['y'] >= points['PF_smoothed_LAT']) & (points['y'] <= points['SAF_smoothed_LAT']), 'Assigned Zone'] = 'PF'
# points.loc[(points['y'] >= points['Boundary_smoothed_LAT']) & (points['y'] <= points['PF_smoothed_LAT']), 'Assigned Zone'] = 'ASZ'
# points.loc[(points['y'] <= points['Boundary_smoothed_LAT']), 'Assigned Zone'] = 'SIZ'
#
# points.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/points_assigned.xlsx')

"""
Check the assignments work via a map
# """
#
# import pandas as pd
# import numpy as np
# import cartopy.crs as ccrs
# import cartopy.feature as cf
# import matplotlib.pyplot as plt
#
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/points_assigned.xlsx')
# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# #
# fronts = ['PF', 'SAF', 'STF', 'Boundary']
# zones = np.unique(points['Assigned Zone'])
# #
# for g in range(0, len(zones)):
#     df2 = points.loc[points['Assigned Zone'] == zones[g]]
#     print(len(df2))
#
#     # Optional: Plot if required
#     plt.figure(figsize=(10, 10))
#     ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
#
#     # First Subplot: Nitrate Map
#     ax.add_feature(cf.OCEAN)
#     ax.add_feature(cf.LAND, edgecolor='black')
#     ax.gridlines()
#
#     fronts = np.unique(acc_fronts['front_name'])
#     fronts = ['PF', 'SAF', 'STF', 'Boundary']
#     line_sys = ['dotted', 'dashed', 'dashdot', 'solid']
#     ax.set_title(f'{zones[g]}')
#     # Loop through each front and plot
#     for i in range(len(fronts)):
#         this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#         latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
#         longitudes = this_one['longitude'].values
#
#         # Plot the data, making sure to specify the correct CRS for input data
#         ax.plot(
#             longitudes,
#             latitudes,
#             transform=ccrs.PlateCarree(),  # Data is in lat/lon format
#             linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
#             label=fronts[i], color='black')
#
#         # Plot the HEATMAP on top of the ORSI lines
#     ax.scatter(
#         df2['x'].values,
#         df2['y'].values, s=5, linewidth=0.5, vmin=0, vmax=32, alpha=0.9, transform=ccrs.PlateCarree())  # Data is in lat/lon format))
#
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/{zones[g]}_parsecheck.png', dpi=300, bbox_inches="tight")
#     plt.close()

"""
PARSE CHECK WORKED!!!
"""
# import pandas as pd
# import numpy as np
# import cartopy.crs as ccrs
# import cartopy.feature as cf
# import matplotlib.pyplot as plt
#
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/points_assigned.xlsx')
# sites = np.unique(points['location'])
# zones = np.unique(points['Assigned Zone'])
#
# out1 = []
# out2 = []
# out3 = []
#
# for i in range(0, len(sites)):
#     this_site = points.loc[points['location'] == sites[i]]
#
#     for u in range(0, len(zones)):
#         how_many = this_site.loc[this_site['Assigned Zone'] == zones[u]]
#         out1.append(sites[i])
#         out2.append(zones[u])
#         out3.append(len(how_many))
# output1 = pd.DataFrame({"Site": out1, "Zone": out2, "Length": out3})
# output1.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/time_per_zone_usingpoints.xlsx')


"""
Sara M. Fletcher mentioned in our group meeting on June 20, 2024 that it would be nice to have this graphically displayed rather than
just as a table. Lets see if we can do that below. 
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Read the data from the Excel file
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/time_per_zone_usingpoints_edited_Dec3_2024.xlsx', sheet_name='New_Fixed_data', comment='#')

# make the plot twice and edit

blah = np.unique(df['Country'])
for h in range(0, len(blah)):

    df1 = df.loc[df['Country'] == blah[h]]
    # print(df)

    df1 = df1.rename(columns={"STZ": "Subtropical Zone (STZ)",
                              "SAZ": "Subantarctic Zone (SAZ)",
                              "PF": "Polar Frontal Zone (PFZ)",
                              "ASZ": "Antarctic-Southern Zone (ASZ)",
                              "SIZ": "Seasonal Ice Zone (SIZ)"})

    zones = ["Subtropical Zone (STZ)", "Subantarctic Zone (SAZ)", "Polar Frontal Zone (PFZ)", "Antarctic-Southern Zone (ASZ)", "Seasonal Ice Zone (SIZ)"]
    zone_trans = [0.2, 0.2, 1,1,1]
    sites = df1['Site']

    # Define the color palette
    colors = sns.color_palette("muted", len(zones))

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 8))

    # Initialize the bottom array for the first stack
    bottom = np.zeros(len(sites))

    # Loop through each zone to create a stacked bar
    for i, zone in enumerate(zones):
        ax.bar(sites, df1[zone], bottom=bottom, label=zone, color=colors[i], alpha=zone_trans[i])
        bottom += df1[zone].values  # Update the bottom to include the current zone's height

    # Add some text for labels, title, and custom x-axis tick labels, etc.
    ax.set_xlabel('Site')
    ax.set_ylabel('Percent')
    ax.set_title('Percent of Back-Trajectory Spent in Each Zone')
    ax.set_xticks(np.arange(len(sites)))
    ax.set_xticklabels(sites, rotation=65, ha='right')
    if h == 1:
        ax.legend()
    # Show the plot
    plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/stackedbar_{blah[h]}.png", dpi=300, bbox_inches="tight")

plt.close()

























# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
#
# # Read the data from the Excel file
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/points_assigned.xlsx')
#
#
# blah = np.unique(df['Country'])
# for h in range(0, len(blah)):
#
#     df1 = df.loc[df['Country'] == blah[h]]
#     # print(df)
#
#     df1 = df1.rename(columns={"STZ": "Subtropical Zone (STZ)",
#                               "SAZ": "Subantarctic Zone (SAZ)",
#                               "PFZ": "Polar Frontal Zone (PFZ)",
#                               "ASZ": "Antarctic-Southern Zone (ASZ)",
#                               "SIZ": "Seasonal Ice Zone (SIZ)"})
#
#     zones = ["Subtropical Zone (STZ)", "Subantarctic Zone (SAZ)", "Polar Frontal Zone (PFZ)", "Antarctic-Southern Zone (ASZ)", "Seasonal Ice Zone (SIZ)"]
#     zone_trans = [0.2, 0.2, 1,1,1]
#     sites = df1['Site']
#
#     # Define the color palette
#     colors = sns.color_palette("muted", len(zones))
#
#     # Plotting
#     fig, ax = plt.subplots(figsize=(6, 8))
#
#     # Initialize the bottom array for the first stack
#     bottom = np.zeros(len(sites))
#
#     # Loop through each zone to create a stacked bar
#     for i, zone in enumerate(zones):
#         ax.bar(sites, df1[zone], bottom=bottom, label=zone, color=colors[i], alpha=zone_trans[i])
#         bottom += df1[zone].values  # Update the bottom to include the current zone's height
#
#     # Add some text for labels, title, and custom x-axis tick labels, etc.
#     ax.set_xlabel('Site')
#     ax.set_ylabel('Percent')
#     ax.set_title('Percent of Back-Trajectory Spent in Each Zone')
#     ax.set_xticks(np.arange(len(sites)))
#     ax.set_xticklabels(sites, rotation=65, ha='right')
#     if h == 1:
#         ax.legend()
#     # Show the plot
#     plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/stackedbar_{blah[h]}.png", dpi=300, bbox_inches="tight")
#
# plt.close()





