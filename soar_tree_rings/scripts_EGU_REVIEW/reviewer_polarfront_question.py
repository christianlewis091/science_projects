"""
Is our polar front from Orsi the most up to date? Lets compare with a polar front from Freeman and Lovenduski 2016.
According to Dr. Freeman "The Freeman and Lovenduski (2016) climatological PF location can be computed by averaging the
weekly PF locations publicly provided. To confirm this, the first sentence in Section 4 reads, "We investigate the
climatological position of the front by averaging weekly realizations over 2002–2014 (Figs. 4, 5)." In hindsight,
this could have also cited Fig. 6, as it is identical to those shown in Figs 4 and 5a."

First, lets compute the climatological location as she suggests, and then re-run the HYSPLIT scripts to see how much
difference it makes.
"""
import pandas as pd
import netCDF4 as nc
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import netCDF4 as nc
from pandas import read_csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.gridspec as gridspec
import time
import openpyxl
start_time = time.time()
import cartopy.crs as ccrs
import cartopy.feature as cf
from cmcrameri import cm
import matplotlib.colors as mcolors


file_path = "C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/data/Polar_Front_weekly.nc"

# read the file and make sure its in READ MODE so the file doesn't get corrupted...

# Open the NetCDF file in read mode
with nc.Dataset(file_path, mode="r") as ds:
    # print(ds)
    # print("Variables:", ds.variables.keys())  # Print available variables

    # Read variables correctly using 'ds', not 'nc'
    lon = ds.variables['longitude'][:]
    pfw = ds.variables['PFw'][:]
    time = ds.variables['time'][:]
    time_stamp = ds.variables['time_stamp'][:]

# Print shape of the data to confirm successful extraction
# print("Longitude shape:", lon.shape)
# print("PFw shape:", pfw.shape)
# print("Time shape:", time.shape)
# print("Time stamp shape:", time_stamp.shape)

"""
PFw, the varaible we're interested in, has shape 612vs1440, and there are 1440 longitudes. So we're going to average over the 612 dimension
"""

# x = np.matrix(np.arange(12).reshape((3, 4)))
# print(x)
# print()
# # we wnt the 0 axis.
# print(x.mean(0))
# print()
# print(x.mean(1))

pfw_mean = pfw.mean(0)


"""
ANIMATE THE DATA TO SEEIT CHANGING AND MAKE SURE ITS EXTRACTED REASONABLY
"""
# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 5))

# Initialize an empty plot
line, = ax.plot([], [], lw=2)
timestamp_text = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=12, color="red")  # Timestamp overlay

# Set axis labels
ax.set_xlabel("Longitude")
ax.set_ylabel("PFw (Latitude)")
ax.set_title("Polar Front Evolution Over Time")

# Set axis limits (adjust based on data range)
ax.set_xlim(lon.min(), lon.max())
ax.set_ylim(pfw.min(), pfw.max())

# Convert time to datetime (adjust origin if needed)
time_index = pd.to_datetime(time, unit="W", origin="2002-01-01")

ax.plot(lon, pfw_mean, color='red', label='Climatology (mean of weekly PFs)')
ax.legend()
# Function to update the plot for each frame
def update(frame):
    line.set_data(lon, pfw[frame, :])  # Update line data
    ax.set_title(f"Polar Front at {time_index[frame].strftime('%Y-%m-%d')}, Freeman and Lovenduski 2016")  # Update title
    return line, timestamp_text

# Create animation
ani = animation.FuncAnimation(fig, update, frames=len(time_index), interval=200, blit=True)

# # Show animation
# ani.save("C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/polar_front_animation.gif", writer="pillow", fps=10)

df = pd.DataFrame({"longitude": lon, "latitude": pfw_mean, "front_name": 'Freeman_PF'}) #.sort_values(by=['longitude'])
df.loc[(df['longitude'] > 180) & (df['front_name'] == "Freeman_PF"), 'longitude'] -= 360
df = df.sort_values(by=['longitude'])

# verify on a map it looks OK
plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
ax.set_global()  # Ensures the full globe fits within the plot area
ax.add_feature(cf.OCEAN)
ax.add_feature(cf.LAND, edgecolor='black')

# Add gridlines with labels
gl = ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=0.5)
gl.top_labels = False  # Hide labels at the top
gl.right_labels = False  # Hide labels on the right

latitudes = df['latitude'].values  # Convert to numpy array if necessary
longitudes = df['longitude'].values

# Plot the data, making sure to specify the correct CRS for input data
ax.plot(
    longitudes,
    latitudes,
    transform=ccrs.PlateCarree(), color='red')  # Data is in lat/lon format
    # linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
    # label=l1[i], color=c1[i])
plt.legend()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/freeman_pf.png',
            dpi=300, bbox_inches="tight")


# add the ORSI data
acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
acc_w_freeman = pd.concat([acc_fronts, df], ignore_index=True)

# rewrite the map to make sure it all still looks OK
plt.figure(figsize=(10, 10))
ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
ax.set_global()  # Ensures the full globe fits within the plot area
ax.add_feature(cf.OCEAN)
ax.add_feature(cf.LAND, edgecolor='black')

# Add gridlines with labels
gl = ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=0.5)
gl.top_labels = False  # Hide labels at the top
gl.right_labels = False  # Hide labels on the right

fronts = ['PF', 'SAF', 'STF', 'Boundary','Freeman_PF']
line_sys = ['solid', 'dashed', 'dashdot', 'solid','solid']
c1 = ['blue', 'black', 'black', 'black','red']
l1 = ['PF', 'SAF', 'STF', 'Boundary','PF (Freeman and Lovenduski, 2016)']
# Loop through each front and plot
for i in range(len(fronts)):
    this_one = acc_w_freeman.loc[acc_w_freeman['front_name'] == fronts[i]]
    latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
    longitudes = this_one['longitude'].values

    # Plot the data, making sure to specify the correct CRS for input data
    ax.plot(
        longitudes,
        latitudes,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=l1[i], color=c1[i])
plt.legend()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/PF_comparison.png',
            dpi=300, bbox_inches="tight")

acc_w_freeman.to_csv('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files/acc_w_freeman_FINAL.csv')


"""
RESTART RUNNING BLOCK 2!
"""
points = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/hysplit_heatmap/points_concat.xlsx')

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

    # Create a figure
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
    ax.set_global()  # Ensures the full globe fits within the plot area
    # First Subplot: Nitrate Map
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.LAND, edgecolor='black')

    fronts = ['Freeman_PF', 'SAF', 'STF', 'Boundary']
    line_sys = ['dotted', 'dashed', 'dashdot', 'solid']
    c1 = ['red', 'black', 'black', 'black']
    # Loop through each front and plot
    for i in range(len(fronts)):
        this_one = acc_w_freeman.loc[acc_w_freeman['front_name'] == fronts[i]]
        latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
        longitudes = this_one['longitude'].values

        # Plot the data, making sure to specify the correct CRS for input data
        ax.plot(
            longitudes,
            latitudes,
            transform=ccrs.PlateCarree(),  # Data is in lat/lon format
            linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
            label=fronts[i], color=c1[i])

    ax.scatter(
        results['x'].values,
        results['y'].values,
        c=results['heat'].values, cmap='coolwarm',  s=25, linewidth=0.0, vmin=0, vmax=32, alpha=0.9, transform=ccrs.PlateCarree())  # Data is in lat/lon format))

    # Show the plot
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/{locations[q]}_FREEMANPF.png',
                dpi=300, bbox_inches="tight")
    plt.close()

"""
THE CODE BLOCK ABOVE SHOWS THAT THE HEATMAPS STILL LOOK OK!
"""

"""
IMPORTANT! Below, the code is meant to run accoridng to the original name of the dataframe, "acc fronts"
It has been edited above to "acc_w_Freeman" to inlude the freeman et al., 2016 data. 
Below, I'm going to rename it to the orignal one, (to avoid making a lot of changes to he naming and cause bugs) 
but I'm going to select to EXLCUDE the PF that is NOT freeman. 
"""

acc_fronts = acc_w_freeman.loc[acc_w_freeman['front_name'] != 'PF']

"""
below carries on with repeat of HYSPLIT check Dec3 2024, but withs save locations altered. 
"""

reference = pd.DataFrame()
reference['x'] = points['x']  # SMOOTH ORSI TO POINTS LONGITUDES
#
# Iterate over each front
fronts = acc_fronts['front_name'].unique()
for front in fronts:
    # Extract latitude and longitude for the current front
    this_one = acc_fronts[acc_fronts['front_name'] == front]
    front_longitudes = this_one['longitude'].values
    front_latitudes = this_one['latitude'].values

    # Ensure the front data is sorted by longitude
    sorted_indices = np.argsort(front_longitudes)
    front_longitudes = front_longitudes[sorted_indices]
    front_latitudes = front_latitudes[sorted_indices]

    # Interpolate the front latitudes to match the longitudes of the data
    smoothed_latitudes = np.interp(reference['x'], front_longitudes, front_latitudes)

    # Add interpolated latitudes as a new column in the data
    reference[f'{front}_smoothed_LAT'] = smoothed_latitudes

    # Optional: Plot if required
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))

    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.LAND, edgecolor='black')
    ax.gridlines()
    ax.set_title(f'{front}')

    fronts = ['Freeman_PF', 'SAF', 'STF', 'Boundary']
    line_sys = ['dotted', 'dashed', 'dashdot', 'solid']

    # Loop through each front and plot
    for i in range(len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
        latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
        longitudes = this_one['longitude'].values

        # Plot the data, making sure to specify the correct CRS for input data
        ax.plot(
            longitudes,
            latitudes,
            transform=ccrs.PlateCarree(),  # Data is in lat/lon format
            linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
            label=fronts[i], color='black')

    ax.scatter(
        reference['x'],
        smoothed_latitudes,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=fronts[i], color='red')

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/{front}_FREEMANPF.png', dpi=300, bbox_inches="tight")
    plt.close()

# here is the dataframe of the smoothed fronts, on the sampled longitudes
reference.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/smoothed_fronts_sample_lons_FREEMANPF.xlsx')

"""
Merge the Reference's smoothed acc fronts fronts with sample longitudes
"""

reference = reference.sort_values(by=['x'])
points = points.sort_values(by=['x'])

points['STF_smoothed_LAT'] = reference['STF_smoothed_LAT']
points['SAF_smoothed_LAT'] = reference['SAF_smoothed_LAT']
points['Freeman_PF_smoothed_LAT'] = reference['Freeman_PF_smoothed_LAT']
points['Boundary_smoothed_LAT'] = reference['Boundary_smoothed_LAT']
points['ref_x'] = reference['x']
points['test'] = points['ref_x'] - reference['x'] # I need to assign latitude bands for the fronts, for each longitude. if the right bands have been assigned, the difference in longitudes will be 0
print(points['test'])

"""
NOW,
I WANT TO PUT THE DATA INTO BINS, OF FRONT, AND OCEAN ZONE
"""

points.loc[(points['y'] >= points['STF_smoothed_LAT']), 'Assigned Zone'] = 'STZ'
points.loc[(points['y'] >= points['SAF_smoothed_LAT']) & (points['y'] <= points['STF_smoothed_LAT']), 'Assigned Zone'] = 'SAZ'
points.loc[(points['y'] >= points['Freeman_PF_smoothed_LAT']) & (points['y'] <= points['SAF_smoothed_LAT']), 'Assigned Zone'] = 'Freeman PFZ'
points.loc[(points['y'] >= points['Boundary_smoothed_LAT']) & (points['y'] <= points['Freeman_PF_smoothed_LAT']), 'Assigned Zone'] = 'ASZ'
points.loc[(points['y'] <= points['Boundary_smoothed_LAT']), 'Assigned Zone'] = 'SIZ'

points.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/points_assigned_FREEMANPF.xlsx')

"""
Check the assignments work via a map
# """

fronts = ['Freeman_PF', 'SAF', 'STF', 'Boundary']
zones = np.unique(points['Assigned Zone'])
#
for g in range(0, len(zones)):
    df2 = points.loc[points['Assigned Zone'] == zones[g]]
    print(len(df2))

    # Optional: Plot if required
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))

    # First Subplot: Nitrate Map
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.LAND, edgecolor='black')
    ax.gridlines()

    fronts = np.unique(acc_fronts['front_name'])
    fronts = ['Freeman_PF', 'SAF', 'STF', 'Boundary']
    line_sys = ['dotted', 'dashed', 'dashdot', 'solid']
    ax.set_title(f'{zones[g]}')
    # Loop through each front and plot
    for i in range(len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
        latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
        longitudes = this_one['longitude'].values

        # Plot the data, making sure to specify the correct CRS for input data
        ax.plot(
            longitudes,
            latitudes,
            transform=ccrs.PlateCarree(),  # Data is in lat/lon format
            linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
            label=fronts[i], color='black')

        # Plot the HEATMAP on top of the ORSI lines
    ax.scatter(
        df2['x'].values,
        df2['y'].values, s=5, linewidth=0.5, vmin=0, vmax=32, alpha=0.9, transform=ccrs.PlateCarree())  # Data is in lat/lon format))

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/{zones[g]}_parsecheck_FREEMANPF.png', dpi=300, bbox_inches="tight")
    plt.close()

"""
PARSE CHECK WORKED!!!
"""

sites = np.unique(points['location'])
zones = np.unique(points['Assigned Zone'])

out1 = []
out2 = []
out3 = []

for i in range(0, len(sites)):
    this_site = points.loc[points['location'] == sites[i]]

    for u in range(0, len(zones)):
        how_many = this_site.loc[this_site['Assigned Zone'] == zones[u]]
        out1.append(sites[i])
        out2.append(zones[u])
        out3.append(len(how_many))
output1 = pd.DataFrame({"Site": out1, "Zone": out2, "Length": out3})
output1.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/hysplit_time_per_zone_usingpoints_FREEMANPF.xlsx')

#
# """
# Sara M. Fletcher mentioned in our group meeting on June 20, 2024 that it would be nice to have this graphically displayed rather than
# just as a table. Lets see if we can do that below.
# """
#
# import pandas as pd
# import matplotlib.pyplot as plt
# import numpy as np
# import seaborn as sns
# from cmcrameri import cm
#
# cmcrameri_colormaps = ["batlow",
#                        "batlowW",
#                        "batlowK",
#                        "glasgow",
#                        "lipari",
#                        "navia",
#                        "hawaii",
#                        "buda",
#                        "imola",
#                        "oslo",
#                        "grayC",
#                        "nuuk",
#                        "devon",
#                        "lajolla",
#                        "bamako",
#                        "davos",
#                        "bilbao",
#                        "lapaz",
#                        "acton",
#                        "turku",
#                        "tokyo",
#                        ]
#
# # Read the data from the Excel file
# df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/HYSPLIT_check_Dec3_2024/FINAL_OUTPUT_AND_GRAPHS/time_per_zone_usingpoints_edited_Dec3_2024.xlsx', sheet_name='New_Fixed_data', comment='#')
#
# # make the plot twice and edit
# for cmap_name in cmcrameri_colormaps:
#
#     blah = np.unique(df['Country'])
#     for h in range(0, len(blah)):
#
#         df1 = df.loc[df['Country'] == blah[h]]
#         # print(df)
#
#         df1 = df1.rename(columns={"STZ": "Subtropical Zone (STZ)",
#                                   "SAZ": "Subantarctic Zone (SAZ)",
#                                   "PF": "Polar Frontal Zone (PFZ)",
#                                   "ASZ": "Antarctic-Southern Zone (ASZ)",
#                                   "SIZ": "Seasonal Ice Zone (SIZ)"})
#
#         zones = ["Subtropical Zone (STZ)", "Subantarctic Zone (SAZ)", "Polar Frontal Zone (PFZ)", "Antarctic-Southern Zone (ASZ)", "Seasonal Ice Zone (SIZ)"]
#         # zone_trans = [0.2, 0.2, 1,1,1]
#         sites = df1['Site']
#
#         # Define the color palette
#         colors = getattr(cm, cmap_name)(np.linspace(.8, .2, len(zones)))
#
#         # Plotting
#         fig, ax = plt.subplots(figsize=(6, 8))
#
#         # Initialize the bottom array for the first stack
#         bottom = np.zeros(len(sites))
#
#         # Loop through each zone to create a stacked bar
#         for i, zone in enumerate(zones):
#             ax.bar(sites, df1[zone], bottom=bottom, label=zone, color=colors[i]) # , alpha=zone_trans[i]
#             bottom += df1[zone].values  # Update the bottom to include the current zone's height
#
#         # Add some text for labels, title, and custom x-axis tick labels, etc.
#         ax.set_xlabel('Site')
#         ax.set_ylabel('Percent')
#         ax.set_title(f'Percent of Back-Trajectory Spent in Each Zone')
#         ax.set_xticks(np.arange(len(sites)))
#         ax.set_xticklabels(sites, rotation=65, ha='right')
#         if h == 1:
#             ax.legend()
#         # Show the plot
#         plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_submission/Images_and_Figures/HYSPLIT/cmcrameri_colortesting/stackedbar_{blah[h]}_{cmap_name}.png", dpi=300, bbox_inches="tight")
#         plt.close()
#
#
#
#















