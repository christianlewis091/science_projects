import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import cartopy.crs as ccrs
import cartopy.feature as cf
from cmcrameri import cm
import matplotlib.colors as mcolors
from shapely.geometry import Polygon

# df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_submission/Data_Files/GLODAP_smoothed_fronts_sample_lons.xlsx').sort_values(by='LONGITUDE')
#
# # rewrite the map to make sure it all still looks OK
# plt.figure(figsize=(10, 10))
# ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
# ax.set_global()  # Ensures the full globe fits within the plot area
# ax.add_feature(cf.OCEAN)
# ax.add_feature(cf.LAND, edgecolor='black')
#
# x = df['LONGITUDE'].values
# stf = df['STF_smoothed_LAT'].values
# saf = df['SAF_smoothed_LAT'].values
# pf = df['PF_smoothed_LAT'].values
# bound = df['Boundary_smoothed_LAT'].values
#
# ax.plot(x,stf, transform=ccrs.PlateCarree())
# ax.plot(x,saf, transform=ccrs.PlateCarree())
# ax.plot(x,pf, transform=ccrs.PlateCarree())
# ax.plot(x,bound, transform=ccrs.PlateCarree())
#
# # Fill between STF and SAF
# poly_coords = np.concatenate([
#     np.column_stack((x, saf)),
#     np.column_stack((x[::-1], stf[::-1]))
# ])
# poly = Polygon(poly_coords)
# ax.add_geometries([poly], crs=ccrs.PlateCarree(), facecolor=cm.batlow(0.2), edgecolor='none', alpha=0.6)
#
# plt.legend()
# plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf
from shapely.geometry import Polygon
import cmcrameri

# List all cmcrameri colormaps (excluding private ones)
cmaps = [m for m in dir(cmcrameri.cm) if not m.startswith('_') and callable(getattr(cmcrameri.cm, m))]

# Load and sort the data
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_submission/Data_Files/GLODAP_smoothed_fronts_sample_lons.xlsx').sort_values(by='LONGITUDE')
x = df['LONGITUDE'].values
front_names = ['STF_smoothed_LAT', 'SAF_smoothed_LAT', 'PF_smoothed_LAT', 'Boundary_smoothed_LAT']
front_labels = ['STF', 'SAF', 'PF', 'Boundary']
front_lats = [df[name].values for name in front_names]
n_zones = len(front_lats) - 1

# Loop over colormaps
for cmap_name in cmaps:
    cmap = getattr(cmcrameri.cm, cmap_name)

    # Create reversed colors for the zones
    front_colors = [cmap(i / n_zones) for i in range(n_zones)][::-1]

    # Create the map
    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
    ax.set_global()
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.LAND, edgecolor='black')

    # Plot the fronts
    for lat, label in zip(front_lats, front_labels):
        ax.plot(x, lat, transform=ccrs.PlateCarree(), label=label, color='black')

    # Fill between each pair of fronts
    for i in range(n_zones):
        lat1 = front_lats[i]
        lat2 = front_lats[i+1]

        poly_coords = np.concatenate([
            np.column_stack((x, lat1)),
            np.column_stack((x[::-1], lat2[::-1]))
        ])
        polygon = Polygon(poly_coords)

        ax.add_geometries([polygon], crs=ccrs.PlateCarree(),
                          facecolor=front_colors[i], edgecolor='none', alpha=0.6)

    plt.tight_layout()

    # Legend and title
    plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Images_and_Figures\HYSPLIT/fronts_fill_between/fronts_filled_in_{cmap_name}.png', dpi=300, bbox_inches="tight")
    plt.close()


























#
#
# fronts = ['PF', 'SAF', 'STF', 'Boundary','Freeman_PF']
# line_sys = ['solid', 'dashed', 'dashdot', 'dotted', 'solid']
# c1 = ['blue', 'black', 'black', 'black','red']
# # Loop through each front and plot
# for i in range(len(fronts)):
#     this_one = acc_w_freeman.loc[acc_w_freeman['front_name'] == fronts[i]]
#     latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
#     longitudes = this_one['longitude'].values
#
#     # Plot the data, making sure to specify the correct CRS for input data
#     ax.plot(
#         longitudes,
#         latitudes,
#         transform=ccrs.PlateCarree(),  # Data is in lat/lon format
#         linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
#         color=c1[i])
# plt.legend()
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/polar_front_question/PF_comparison.png',
#             dpi=300, bbox_inches="tight")








# Add gridlines with labels
# gl = ax.gridlines(draw_labels=True, linestyle="--", color="gray", alpha=0.5)
# gl.top_labels = False  # Hide labels at the top
# gl.right_labels = False  # Hide labels on the right