import pandas as pd
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import seaborn as sns

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/FINAL_merged.xlsx').dropna(subset='DepSM')
df['fileName'] = df['FileName']
# for each location / sound
locations = np.unique(df['ctdSampleLocation'])
colors2 = sns.color_palette("mako", 20)
colors2 = list(reversed(colors2))
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D','o', '^', '8', 's', 'p', '*', 'X', 'D']

# doubtful sound giving problems: have a lookski. Has too maby
dbt = df.loc[df['ctdSampleLocation'] == 'DBT']
print(len(np.unique(dbt['fileName'])))
# dbt.to_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_2023_CTD_Data_Concat/dbt.xlsx')

# loop through and create plots
for k in range(0, len(locations)):

    # for each location we'll have a new figure
    fig = plt.figure(figsize=(10,5))
    gs = gridspec.GridSpec(3, 5)
    gs.update(wspace=0.1, hspace=0.1)
    surf = 10

    location1 = df.loc[df['ctdSampleLocation'] == locations[k]].sort_values(by=['longitude'])
    print(locations[k])
    # grab each station within the "sound" subloop
    stations = np.unique(location1['fileName'])  # each filename comes from a differnet CTD cast

    # FIRST PLOT, SURFACE TEMPERATURE
    xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
    plt.ylim(surf, 0)
    plt.ylabel('Depth (m)')
    plt.xticks([], [])
    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])
        depth = stn1['DepSM']
        pottemp = stn1['Potemp090C']
        plt.plot(pottemp, depth, color=colors2[i])

        # add a scatter point to help differentite the stations
        last_row = stn1.iloc[-1]
        plt.scatter(last_row['Potemp090C'], last_row['DepSM'], color=colors2[i], marker=markers[i])

    # SECOND PLOT, SUBSURFACE TEMPERATURE
    xtr_subsplot = fig.add_subplot(gs[1:3, 0:1])
    plt.ylim(500, surf)
    plt.ylabel('Depth (m)')
    plt.xlabel('Potemp090C')

    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])

        # extract the variables
        depth = stn1['DepSM']
        pottemp = stn1['Potemp090C']
        plt.plot(pottemp, depth, color=colors2[i])

        # add a scatter point to help differentite the stations
        last_row = stn1.iloc[-1]
        plt.scatter(last_row['Potemp090C'], last_row['DepSM'], color=colors2[i], marker=markers[i])


    # THIRD PLOT, SURFACE SALINITY
    xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
    plt.ylim(surf, 0)
    plt.yticks([], [])
    plt.xticks([], [])
    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])
        # extract the variables
        depth = stn1['DepSM']
        sal = stn1['Sal00']
        plt.plot(sal, depth, color=colors2[i])

        # add a scatter point to help differentite the stations
        last_row = stn1.iloc[-1]
        plt.scatter(last_row['Sal00'], last_row['DepSM'], color=colors2[i], marker=markers[i])

    # 4th PLOT, SUBSURFACE SALINITY
    xtr_subsplot = fig.add_subplot(gs[1:3, 1:2])
    plt.ylim(500, surf)
    plt.yticks([], [])
    plt.xlabel('Sal00')
    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])

        # extract the variables
        depth = stn1['DepSM']
        sal = stn1['Sal00']
        plt.plot(sal, depth, color=colors2[i])

        # add a scatter point to help differentite the stations
        last_row = stn1.iloc[-1]
        plt.scatter(last_row['Sal00'], last_row['DepSM'], color=colors2[i], marker=markers[i])

    # 5th PLOT, SURFACE Oxygen
    xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])
    plt.ylim(surf, 0)
    plt.yticks([], [])
    plt.xticks([], [])
    plt.xlim(0,120)

    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])
        stn1 = stn1.loc[stn1['Sbeox0PS'] >= 0]
        # extract the variables
        depth = stn1['DepSM']
        ox = stn1['Sbeox0PS']
        plt.plot(ox, depth, color=colors2[i])

        # add a scatter point to help differentite the stations
        last_row = stn1.iloc[-1]
        plt.scatter(last_row['Sbeox0PS'], last_row['DepSM'], color=colors2[i], marker=markers[i])

    # 6th PLOT, SUBSURFACE Oxygen
    xtr_subsplot = fig.add_subplot(gs[1:3, 2:3])
    plt.ylim(500, surf)
    plt.xlim(0,120)
    plt.yticks([], [])
    plt.xlabel('Sbeox0PS')
    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])
        stn1 = stn1.loc[stn1['Sbeox0PS'] >= 0]
        depth = stn1['DepSM']
        ox = stn1['Sbeox0PS']
        plt.plot(ox, depth, color=colors2[i])

        # add a scatter point to help differentite the stations
        last_row = stn1.iloc[-1]
        plt.scatter(last_row['Sbeox0PS'], last_row['DepSM'], color=colors2[i], marker=markers[i])


    """
    BELOW IS THE MAP
    """
    xtr_subsplot = fig.add_subplot(gs[0:3, 3:5])
    plt.title(f'{locations[k]}; contains both 2022 and 2023 data, not visually distinguished!')
    maxlat = -45.0
    minlat = -46
    nz_max_lon = 167.25
    nz_min_lon = 166.25
    res = 'i'
    map = Basemap(llcrnrlat=minlat, urcrnrlat=maxlat, llcrnrlon=nz_min_lon, urcrnrlon=nz_max_lon, resolution=res)
    map.drawparallels(np.arange(-90, 90, 0.25), labels=[False, True, True, False], linewidth=0.5)
    map.drawmeridians(np.arange(-180, 180, 0.25), labels=[True, False, False, True], linewidth=0.5)
    # map.drawmapboundary(fill_color='lightgrey')
    # map.fillcontinents(color='darkgrey')
    map.drawcoastlines(linewidth=0.1)
    map.shadedrelief()

    for i in range(0, len(stations)):
        print(stations[i])
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])
        lat = np.unique(stn1['latitude'])
        lon = np.unique(stn1['longitude'])
        x, y = map(lon, lat)
        x = x[0] # some of the DBT stations had weird errors where the lon showed up twice: [167.0944685 167.0944685]
        print(x)
        print(y)
        map.scatter(x, y, edgecolor='black', color=colors2[i], marker=markers[i])

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_Field_Season_Figures/{locations[k]}_new',
                dpi=300, bbox_inches="tight")
    plt.close()






























