import pandas as pd
import seaborn as sns
from mpl_toolkits.basemap import Basemap


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
#
# # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
year = ['2005_2006', '2010_2011','2015_2016','2020_2021']
w = 1
a = 0.5
sizess = 10
# Loop through the codenames
for k in range(0, len(year)):
    points = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_{year[k]}.xlsx')

    # downsampling in time (only first 24 hours)
    points = points.loc[points['timestep'] > -24]

    # downsampling in altitudes (only taking 100m)
    points = points.loc[points['starting_height'] == 100]

    # downsampling in general: take every 4th point
    points = points[::4].reset_index(drop=True)

    # print(len(points))
    datas = []
    nums = []
    for i in range(0, len(points)):
        row = points.iloc[i]
        x = row['x']
        y = row['y']

        # assign if points are on land or not
        map = Basemap(llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='l')
        xpt, ypt = map(x, y) # convert to projection map
        result = map.is_land(xpt, ypt) # test is_land
        if result:
            datas.append(1)
        else:
            datas.append(0)
        percent = ((int(i)/len(points))*100)/4
        print(f'{year[k]}_{[i]}/{len(points)}, {percent}%')
    points['island'] = datas
    points.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_{year[k]}_oneday.xlsx')