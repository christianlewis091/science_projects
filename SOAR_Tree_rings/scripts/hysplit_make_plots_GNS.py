from matplotlib import cbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid.inset_locator import inset_axes


colors = sns.color_palette("Paired")

"""
6/1/23: version 2 of this file that prepares the Hysplit output for plotting: 
Needs updating to do trajectories for everty site. Old version commented out below
"""
# We're still going to loop through each site using the codenames listed in the previous scripts as well
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
codenames = easy_access['Codename']
code = easy_access['Code']
lat = easy_access['NewLat']
lon = easy_access['ChileFixLon']

from matplotlib import cbook
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid.inset_locator import inset_axes
plt.rcParams.update({'font.size': 10})


colors = sns.color_palette("Paired")

"""
6/1/23: version 2 of this file that prepares the Hysplit output for plotting: 
Needs updating to do trajectories for everty site. Old version commented out below
"""
# We're still going to loop through each site using the codenames listed in the previous scripts as well
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
codenames = easy_access['Codename']
code = easy_access['Code']
lat = easy_access['NewLat']
lon = easy_access['ChileFixLon']

landfrac = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data//landfracresults.xlsx')

# # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
year = ['2005_2006', '2010_2011','2015_2016','2020_2021']
w = 1
a = 0.5
sizess = 10
# Should match the time that is in the is_land assignments or won't make sense. Currently that goes back to timestep -20.
timemin = -20
# Loop through the codenames
for k in range(0, len(year)):
    points = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_{year[k]}.xlsx')
    points = points.loc[points['timestep'] > timemin]

    # grab the means
    means_dataframe_10 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_10_{year[k]}.xlsx')
    means_dataframe_100 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_100_{year[k]}.xlsx')
    means_dataframe_200 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/means_dataframe_200_{year[k]}.xlsx')
    means_dataframe_10 = means_dataframe_10.loc[means_dataframe_10['timestep'] > timemin]
    means_dataframe_100 = means_dataframe_100.loc[means_dataframe_100['timestep'] > timemin]
    means_dataframe_200 = means_dataframe_200.loc[means_dataframe_200['timestep'] > timemin]


    for i in range(0, len(codenames)):
        # which region are we looking at?
        country_code = code[i]
        lat_i = lat[i]
        lon_i = lon[i]


        # here are the POINTS that we'll be plotting
        site_points = points.loc[points['location'] == codenames[i]]
        landfrac_site = landfrac.loc[landfrac['Codenames'] == codenames[i]]

        # isolate the different starting altitudes
        # only plot every 5th traj
        heights = np.unique(site_points['starting_height'])
        h1 = site_points.loc[site_points['starting_height'] == heights[0]][::w].reset_index(drop=True)
        h2 = site_points.loc[site_points['starting_height'] == heights[1]][::w].reset_index(drop=True)
        h3 = site_points.loc[site_points['starting_height'] == heights[2]][::w].reset_index(drop=True)

        # here are the means that we'll be plotting:
        site_mean_10 = means_dataframe_10.loc[means_dataframe_10['Codename'] == codenames[i]].reset_index(drop=True)
        site_mean_100 = means_dataframe_100.loc[means_dataframe_100['Codename'] == codenames[i]].reset_index(drop=True)
        site_mean_200 = means_dataframe_200.loc[means_dataframe_200['Codename'] == codenames[i]].reset_index(drop=True)


        fig = plt.figure(figsize=(4, 8))
        gs = gridspec.GridSpec(8, 4)
        gs.update(wspace=.25, hspace=0.6)

        # SUBPLOT 1
        xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
        plt.title(f'{codenames[i]}, {year[k]}, 20 hours')

        c = 60
        spread = 40
        if country_code == 'NZ':
            mapcorners = [170-spread, -70, 170+spread, 0]
            maxlat = mapcorners[3]
            minlat = mapcorners[1]
            maxlon = mapcorners[2]
            minlon = mapcorners[0]
        else:
            mapcorners = [-70-spread, -70, -70+spread, 0]
            maxlat = mapcorners[3]
            minlat = mapcorners[1]
            maxlon = mapcorners[2]
            minlon = mapcorners[0]


        # build the map
        map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, resolution='l')
        # map = Basemap(projection='ortho',lat_0=-90,lon_0=170,resolution='l')
        # map = Basemap(projection='spstere',boundinglat=-10,lon_0=90,resolution='l')
        map.drawmapboundary(fill_color='lightgrey')
        map.fillcontinents(color='darkgrey')
        map.drawcoastlines(linewidth=0.1)

        # PLOT TRAJECTORIES: NEED TO LOOP INTO OLD FILE NAMES
        # old_filenames = np.unique(h1['filename'])
        # for z in range(0, len(old_filenames)):
        #     this_file = h1.loc[h1['filename'] == old_filenames[z]]
        #
        #     # plot only data within the map-range to remove crappy extra annoying lines on plot
        #     this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
        #
        #     y, x = (this_file['y'], this_file['x'])
        #     map.plot(x, y, color=colors[0],label=str(heights[0]), alpha =a, linewidth=1)

        old_filenames = np.unique(h2['filename'])
        for z in range(0, len(old_filenames)):
            this_file = h2.loc[h2['filename'] == old_filenames[z]]

            # plot only data within the map-range to remove crappy extra annoying lines on plot
            this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]

            y, x = (this_file['y'], this_file['x'])
            map.plot(x, y, color=colors[1],label=str(heights[1]), alpha =a, linewidth=1)
        #
        # old_filenames = np.unique(h3['filename'])
        # for z in range(0, len(old_filenames)):
        #     this_file = h3.loc[h3['filename'] == old_filenames[z]]
        #
        #     # plot only data within the map-range to remove crappy extra annoying lines on plot
        #     this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
        #
        #     y, x = (this_file['y'], this_file['x'])
        #     map.plot(x, y, color=colors[4],label=str(heights[2]), alpha =a, linewidth=1)

        # add the means
        # y_mean, x_mean = (site_mean_10['y'], site_mean_10['x'])
        # map.plot(x_mean, y_mean, color=colors[1], alpha=1)
        y_mean, x_mean = (site_mean_100['y'], site_mean_100['x'])
        map.plot(x_mean, y_mean, color='darkred', alpha=1)
        # y_mean, x_mean = (site_mean_200['y'], site_mean_200['x'])
        # map.plot(x_mean, y_mean, color=colors[5], alpha=1)

        map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], linewidth=0.5)
        map.drawmeridians(np.arange(-180, 180, 40), labels=[1, 1, 0, 1], linewidth=0.5)

        # THE INNER PLOT!
        # inset_axes = inset_axes(xtr_subsplot,
        #                         width="45%", # width = 30% of parent_bbox
        #                         height=1, # height : 1 inch
        #                         loc=1)
        ax_ins = inset_axes(xtr_subsplot, width="45%",  height="45%", loc=1)
        # xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
        x = 4
        mapcorners = [lon_i-x, lat_i-x, lon_i+x, lat_i+x]
        maxlat = mapcorners[3]
        minlat = mapcorners[1]
        maxlon = mapcorners[2]
        minlon = mapcorners[0]

        # build the map
        map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, resolution='l', lon_0=-180)
        map.drawmapboundary(fill_color='white')
        map.fillcontinents(color='darkgrey')
        map.drawcoastlines(linewidth=0.1)

        # PLOT TRAJECTORIES: NEED TO LOOP INTO OLD FILE NAMES
        # old_filenames = np.unique(h1['filename'])
        # for z in range(0, len(old_filenames)):
        #     this_file = h1.loc[h1['filename'] == old_filenames[z]]
        #
        #     # plot only data within the map-range to remove crappy extra annoying lines on plot
        #     this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
        #
        #     y, x = (this_file['y'], this_file['x'])
        #     map.plot(x, y, color=colors[0],label=str(heights[0]), alpha =a, linewidth=.1)

        old_filenames = np.unique(h2['filename'])
        for z in range(0, len(old_filenames)):
            this_file = h2.loc[h2['filename'] == old_filenames[z]]

            # plot only data within the map-range to remove crappy extra annoying lines on plot
            this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]

            y, x = (this_file['y'], this_file['x'])
            map.plot(x, y, color=colors[1],label=str(heights[0]), alpha =a, linewidth=1)

        # old_filenames = np.unique(h3['filename'])
        # for z in range(0, len(old_filenames)):
        #     this_file = h3.loc[h3['filename'] == old_filenames[z]]
        #
        #     # plot only data within the map-range to remove crappy extra annoying lines on plot
        #     this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
        #
        #     y, x = (this_file['y'], this_file['x'])
        #     map.plot(x, y, color=colors[4],label=str(heights[0]), alpha =a, linewidth=.1)

        # add the means
        # y_mean, x_mean = (site_mean_10['y'], site_mean_10['x'])
        # map.plot(x_mean, y_mean, color=colors[1], alpha=1)
        y_mean, x_mean = (site_mean_100['y'], site_mean_100['x'])
        map.plot(x_mean, y_mean, color='darkred', alpha=1)
        # y_mean, x_mean = (site_mean_200['y'], site_mean_200['x'])
        # map.plot(x_mean, y_mean, color=colors[5], alpha=1)


        # map.drawparallels(np.arange(-90, 90, 2), labels=[True, False, False, False], linewidth=0.5)
        # map.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 0, 1], linewidth=0.5)

        # SECOND PLOT!
        xtr_subsplot = fig.add_subplot(gs[4:6, 0:4])
        plt.title('Altitude')
        # plt.plot(site_mean_10['timestep'], site_mean_10['z'] , color=colors[1], label=str(heights[0]))
        plt.plot(site_mean_100['timestep'], site_mean_100['z'] , color=colors[1], label=str(heights[1]))
        # plt.plot(site_mean_200['timestep'], site_mean_200['z'] , color=colors[5], label=str(heights[2]))
        plt.ylim(0, 2000)
        plt.xlim(-20,0)
        plt.xticks([], [])
        plt.legend()

        # Third plot!
        # Percentage of time OVER LAND?
        xtr_subsplot = fig.add_subplot(gs[6:8, 0:4])
        plt.title('Fraction on land')
        # plt.title('Percentage of time over land')
        plt.bar(landfrac_site['timestep'], landfrac_site['LandFrac'])
        plt.xlabel('Timestep')
        plt.xlim(-20,0)

        # plt.text(-19, 0.9, '[C]', fontweight="bold")
        # plt.text(-19.5, 2.1, '[B]', fontweight="bold")
        plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_plots/hrs20_{codenames[i]}_{year[k]}_Dec_to_Feb.png',
                    dpi=300, bbox_inches="tight")
        plt.close()
























#
#
#
#
#
#
# # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
# means_dataframe_10 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/means_dataframe_10.xlsx')
# means_dataframe_100 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/means_dataframe_100.xlsx')
# means_dataframe_200 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/means_dataframe_200.xlsx')
#
# # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
# points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/points.xlsx')
#
# w = 1
# a = 0.5
# sizess = 10
# # Loop through the codenames
# for i in range(0, len(codenames)):
#     # which region are we looking at?
#     country_code = code[i]
#     lat_i = lat[i]
#     lon_i = lon[i]
#
#     # here are the POINTS that we'll be plotting
#     site_points = points.loc[points['location'] == codenames[i]]
#
#     # isolate the different starting altitudes
#     # only plot every 5th traj
#     heights = np.unique(site_points['starting_height'])
#     h1 = site_points.loc[site_points['starting_height'] == heights[0]][::w].reset_index(drop=True)
#     h2 = site_points.loc[site_points['starting_height'] == heights[1]][::w].reset_index(drop=True)
#     h3 = site_points.loc[site_points['starting_height'] == heights[2]][::w].reset_index(drop=True)
#
#     # here are the means that we'll be plotting:
#     site_mean_10 = means_dataframe_10.loc[means_dataframe_10['Codename'] == codenames[i]].reset_index(drop=True)
#     site_mean_100 = means_dataframe_100.loc[means_dataframe_100['Codename'] == codenames[i]].reset_index(drop=True)
#     site_mean_200 = means_dataframe_200.loc[means_dataframe_200['Codename'] == codenames[i]].reset_index(drop=True)
#
#     fig = plt.figure(figsize=(6, 8))
#     gs = gridspec.GridSpec(6, 4)
#     gs.update(wspace=.25, hspace=0.35)
#
#     # SUBPLOT 1
#     xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
#     plt.title(f'{codenames[i]}')
#     mapcorners = [lon_i-60, -70, lon_i+20, -10]
#     # mapcorners = [-0, -70, 360, -10]
#     maxlat = mapcorners[3]
#     minlat = mapcorners[1]
#     maxlon = mapcorners[2]
#     minlon = mapcorners[0]
#
#     # build the map
#     map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, resolution='l', lon_0=-180)
#     map.drawmapboundary(fill_color='lightgrey')
#     map.fillcontinents(color='darkgrey')
#     map.drawcoastlines(linewidth=0.1)
#
#     # PLOT TRAJECTORIES: NEED TO LOOP INTO OLD FILE NAMES
#     old_filenames = np.unique(h1['filename'])
#     for z in range(0, len(old_filenames)):
#         this_file = h1.loc[h1['filename'] == old_filenames[z]]
#
#         # plot only data within the map-range to remove crappy extra annoying lines on plot
#         this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
#
#         y, x = (this_file['y'], this_file['x'])
#         map.plot(x, y, color=colors[0],label=str(heights[0]), alpha =a)
#
#     old_filenames = np.unique(h2['filename'])
#     for z in range(0, len(old_filenames)):
#         this_file = h2.loc[h2['filename'] == old_filenames[z]]
#
#         # plot only data within the map-range to remove crappy extra annoying lines on plot
#         this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
#
#         y, x = (this_file['y'], this_file['x'])
#         map.plot(x, y, color=colors[2],label=str(heights[0]), alpha =a)
#
#     old_filenames = np.unique(h3['filename'])
#     for z in range(0, len(old_filenames)):
#         this_file = h3.loc[h3['filename'] == old_filenames[z]]
#
#         # plot only data within the map-range to remove crappy extra annoying lines on plot
#         this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
#
#         y, x = (this_file['y'], this_file['x'])
#         map.plot(x, y, color=colors[4],label=str(heights[0]), alpha =a)
#
#     # add the means
#     y_mean, x_mean = (site_mean_10['y'], site_mean_10['x'])
#     map.plot(x_mean, y_mean, color=colors[1], alpha=1)
#     y_mean, x_mean = (site_mean_100['y'], site_mean_100['x'])
#     map.plot(x_mean, y_mean, color=colors[3], alpha=1)
#     y_mean, x_mean = (site_mean_200['y'], site_mean_200['x'])
#     map.plot(x_mean, y_mean, color=colors[5], alpha=1)
#
#     map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], linewidth=0.5)
#     map.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1], linewidth=0.5)
#
#     # THE INNER PLOT!
#     # inset_axes = inset_axes(xtr_subsplot,
#     #                         width="45%", # width = 30% of parent_bbox
#     #                         height=1, # height : 1 inch
#     #                         loc=1)
#     ax_ins = inset_axes(xtr_subsplot, width="45%",  height="45%", loc=2)
#     x = 2
#     mapcorners = [lon_i-x, lat_i-x, lon_i+x, lat_i+x]
#     maxlat = mapcorners[3]
#     minlat = mapcorners[1]
#     maxlon = mapcorners[2]
#     minlon = mapcorners[0]
#
#     # build the map
#     map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, resolution='l', lon_0=-180)
#     map.drawmapboundary(fill_color='white')
#     map.fillcontinents(color='darkgrey')
#     map.drawcoastlines(linewidth=0.1)
#
#     # PLOT TRAJECTORIES: NEED TO LOOP INTO OLD FILE NAMES
#     old_filenames = np.unique(h1['filename'])
#     for z in range(0, len(old_filenames)):
#         this_file = h1.loc[h1['filename'] == old_filenames[z]]
#
#         # plot only data within the map-range to remove crappy extra annoying lines on plot
#         this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
#
#         y, x = (this_file['y'], this_file['x'])
#         map.plot(x, y, color=colors[0],label=str(heights[0]), alpha =a)
#
#     old_filenames = np.unique(h2['filename'])
#     for z in range(0, len(old_filenames)):
#         this_file = h2.loc[h2['filename'] == old_filenames[z]]
#
#         # plot only data within the map-range to remove crappy extra annoying lines on plot
#         this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
#
#         y, x = (this_file['y'], this_file['x'])
#         map.plot(x, y, color=colors[2],label=str(heights[0]), alpha =a)
#
#     old_filenames = np.unique(h3['filename'])
#     for z in range(0, len(old_filenames)):
#         this_file = h3.loc[h3['filename'] == old_filenames[z]]
#
#         # plot only data within the map-range to remove crappy extra annoying lines on plot
#         this_file = this_file.loc[(this_file['x'] > minlon) & (this_file['x'] < maxlon)]
#
#         y, x = (this_file['y'], this_file['x'])
#         map.plot(x, y, color=colors[4],label=str(heights[0]), alpha =a)
#
#     # add the means
#     y_mean, x_mean = (site_mean_10['y'], site_mean_10['x'])
#     map.plot(x_mean, y_mean, color=colors[1], alpha=1)
#     y_mean, x_mean = (site_mean_100['y'], site_mean_100['x'])
#     map.plot(x_mean, y_mean, color=colors[3], alpha=1)
#     y_mean, x_mean = (site_mean_200['y'], site_mean_200['x'])
#     map.plot(x_mean, y_mean, color=colors[5], alpha=1)
#
#
#     map.drawparallels(np.arange(-90, 90, 2), labels=[True, False, False, False], linewidth=0.5)
#     map.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 0, 1], linewidth=0.5)
#
#
#     # SECOND PLOT!
#     xtr_subsplot = fig.add_subplot(gs[4:6, 0:4])
#     plt.plot(site_mean_10['timestep'], site_mean_10['z'] , color=colors[1], label=str(heights[0]))
#     plt.plot(site_mean_100['timestep'], site_mean_100['z'] , color=colors[3], label=str(heights[1]))
#     plt.plot(site_mean_200['timestep'], site_mean_200['z'] , color=colors[5], label=str(heights[2]))
#     plt.legend()
#
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/{codenames[i]}.png',
#                 dpi=300, bbox_inches="tight")
#
#     plt.close()
# #
#
#
#
#


















































# #Generate some nice colors
# seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']
# #            0sangre,   1neptune,  2pumpkin,  3clover,   4denim,    5cocoa,    6cumin,    7berry
# #Or try a color from seaborn
# colors=sns.color_palette("rocket",6)
# colors = ['','','peru','cadetblue','plum','','']
#
#
# # We're still going to loop through each site using the codenames listed in the previous scripts as well
# easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
# codenames = easy_access['Codename']
# code = easy_access['Code']
# lat = easy_access['NewLat']
# lon = easy_access['ChileFixLon']
#
# # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
# means_dataframe = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/means_dataframe.xlsx')
#
# # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
# # points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/points.xlsx')
#
# # Loop through the codenames
# for i in range(0, len(codenames)):
#     # which region are we looking at?
#     country_code = code[i]
#     lat_i = lat[i]
#     lon_i = lon[i]
#
#     # # here are the POINTS that we'll be plotting
#     # site_points = points.loc[points['location'] == codenames[i]]
#
#     # isolate the different starting altitudes
#     # only plot every 5th traj
#     # heights = np.unique(site_points['starting_height'])
#     # h1 = site_points.loc[site_points['starting_height'] == heights[0]][::5]
#     # h2 = site_points.loc[site_points['starting_height'] == heights[1]][::5]
#     # h3 = site_points.loc[site_points['starting_height'] == heights[2]][::5]
#
#     # here are the means that we'll be plotting:
#     site_means = means_dataframe.loc[means_dataframe['Codename'] == codenames[i]]
#
#     # Initialize the Figure
#     fig = plt.figure(figsize=(6, 8))
#     gs = gridspec.GridSpec(6, 4)
#     gs.update(wspace=.25, hspace=0.5)
#
#     # Initialize first subplot
#     xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
#
#     mapcorners = [lon_i-60, -80, lon_i+20, 0]
#     maxlat = mapcorners[3]
#     minlat = mapcorners[1]
#     maxlon = mapcorners[2]
#     minlon = mapcorners[0]
#
#     # build the map
#     map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, resolution='l', lon_0=-180)
#     map.drawmapboundary(fill_color='lightgrey')
#     map.fillcontinents(color='darkgrey')
#     map.drawcoastlines(linewidth=0.1)
#
#     # add the trajectories
#     # y, x = (h1['y'], h1['x'])
#     # map.scatter(x, y, marker='.', color=colors[2], s=1, label=str(heights[0]), alpha = 0.5)
#     # y, x = (h2['y'], h2['x'])
#     # map.scatter(x, y, marker='.', color=colors[3], s=1, label=str(heights[1]), alpha = 0.5)
#     # y, x = (h3['y'], h3['x'])
#     # map.scatter(x, y, marker='.', color=colors[4], s=1, label=str(heights[2]), alpha = 0.5)
#
#     # add the means
#     y_mean, x_mean = (site_means['y'], site_means['x'])
#     map.plot(x_mean, y_mean, marker='.', color='black', alpha=1)
#
#     map.drawparallels(np.arange(-90, 90, 20), labels=[True, False, False, False], linewidth=0.5)
#     map.drawmeridians(np.arange(-180, 180, 20), labels=[1, 1, 0, 1], linewidth=0.5)
#     plt.legend()
#
#     inset_axes = inset_axes(xtr_subsplot,
#                             width="45%", # width = 30% of parent_bbox
#                             height=1.5, # height : 1 inch
#                             loc=1)
#     # # Initialize second subplot (ZOOM IN)
#     # xtr_subsplot = fig.add_subplot(gs[0:4, 2:4])
#     #
#     # mapcorners = [lon_i-2, lat_i-2, lon_i+2, lat_i+2]
#     # maxlat = mapcorners[3]
#     # minlat = mapcorners[1]
#     # maxlon = mapcorners[2]
#     # minlon = mapcorners[0]
#     #
#     # # build the map
#     # map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=minlon, urcrnrlon=maxlon, resolution='l', lon_0=-180)
#     # map.drawmapboundary(fill_color='lightgrey')
#     # map.fillcontinents(color='darkgrey')
#     # map.drawcoastlines(linewidth=0.1)
#
#
#     # add the trajectories
#     # y, x = (h1['y'], h1['x'])
#     # map.scatter(x, y, marker='.', color=colors[2], s=1, label=str(heights[0]), alpha = 0.5)
#     # y, x = (h2['y'], h2['x'])
#     # map.scatter(x, y, marker='.', color=colors[3], s=1, label=str(heights[1]), alpha = 0.5)
#     # y, x = (h3['y'], h3['x'])
#     # map.scatter(x, y, marker='.', color=colors[4], s=1, label=str(heights[2]), alpha = 0.5)
#
#     # add the means
#     # y_mean, x_mean = (site_means['y'], site_means['x'])
#     # map.scatter(x_mean, y_mean, marker='.', color='black', alpha=1)
#
#     # map.drawparallels(np.arange(-90, 90, 2), labels=[True, False, False, False], linewidth=0.5)
#     # map.drawmeridians(np.arange(-180, 180, 2), labels=[1, 1, 0, 1], linewidth=0.5)
#     # plt.legend()
#
#     # Third subplot = altitudes
#     xtr_subsplot = fig.add_subplot(gs[4:6, 0:4])
#     # plt.plot(h1['timestep'], h1['z'] , color=colors[2], label=str(heights[0]))
#     # plt.plot(h2['timestep'], h2['z'] , color=colors[3], label=str(heights[1]))
#     # plt.plot(h3['timestep'], h3['z'] , color=colors[4], label=str(heights[2]))
#     # plt.legend()
#
#     plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/{codenames[i]}.png',
#                 dpi=300, bbox_inches="tight")
