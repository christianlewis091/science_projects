import pandas as pd
import seaborn as sns
import numpy as np

"""
Assign_is_land.py assigned a new column to all the "points" data. 
But, in order to plot or find out what % of time each trajectory spent over land, I need to figure out
an average for each time interval, for each site. 
"""

# UNCOMMENT BELOW IF YOU NEED TO RERUN
# year = ['2005_2006', '2010_2011','2015_2016','2020_2021']
# # I dont think we'll want to analyze % land for each ggroup of years individually, but rather as a whole. So I'm going to concat
# # the excel files together first
# df = pd.DataFrame()
# for k in range(0, len(year)):
#     points = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_{year[k]}_oneday.xlsx')
#
#     df = pd.concat([df, points])
#
# df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_island_allyears.xlsx')

"""
Now find the avearge % land for each timestep
"""
# READ IN DATA CREATED ABOVE
points = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/points_island_allyears.xlsx')

# READ IN DATA USED FOR AL THE OTHER HYSPLIT CODES
easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
codenames = easy_access['Codename']
code = easy_access['Code']
lat = easy_access['NewLat']
lon = easy_access['ChileFixLon']

code_array = []
step_array = []
results_array = []
for i in range(0, len(codenames)):

    # GRAB THE DATA FROM THE FIRST SITE
    site_points = points.loc[points['location'] == codenames[i]]

    # assign a variable of the timesteps to iterate over
    timesteps1 = np.unique(site_points['timestep'])

    for k in range(0, len(timesteps1)):
        # ENTER FIRST TIMESTEP
        this_step = site_points.loc[site_points['timestep'] == timesteps1[k]]

        # What is the lenght of this timestep? How many total values are there?
        length_step = int(len(this_step))

        # What is the sum of the values of "is_land" in that timestep?
        sums = np.sum(this_step['island'])

        # sum / length_step. If there are 10 timesteps, and allcross land, it will be 10/10 = 1, or 100%
        result1 = sums/length_step
        print(result1)

        code_array.append(codenames[i])
        step_array.append(timesteps1[k])
        results_array.append(result1)

results_now = pd.DataFrame({"Codenames": code_array, "timestep": step_array, "LandFrac": results_array})
results_now.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/landfracresults.xlsx')










# # We're still going to loop through each site using the codenames listed in the previous scripts as well
# easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/easy_access2.xlsx')
# codenames = easy_access['Codename']
# code = easy_access['Code']
# lat = easy_access['NewLat']
# lon = easy_access['ChileFixLon']
# #
# # # Read in the sheet that was made from the prvious script (hysplit_prepare_output.py)
# year = ['2005_2006', '2010_2011','2015_2016','2020_2021']