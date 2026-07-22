"""
I want a map of bottom water oxygen content in Doubtful Sound
#efefdb land
#97b6e1 sea
https://nbviewer.org/github/jsimkins2/geog473-673/blob/master/Python/Cartopy_tutorial.ipynb

"""
import pandas as pd
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cf
from matplotlib.patches import Rectangle
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# https://ctroupin.github.io/posts/2019-09-02-fine-coast/

# Load the data
df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/EOI_MAP/df2.xlsx')

# Create the main figure and axes
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

cent_lat = -45.439382903965516
cent_lon = 167.13170189947658
ax.set_extent([166.7, 167.3, -45.6, -45], crs=ccrs.PlateCarree())

# Add a background color for the ocean (main map)
ax.add_patch(Rectangle(
    (166.7, -45.6),  # Bottom-left corner of the extent
    167.3 - 166.7,  # Width
    -45 - (-45.6),  # Height
    facecolor="#97b6e1",
    transform=ccrs.PlateCarree(),
    zorder=0))

# Add GSHHS land features (main map)
land = cf.GSHHSFeature(scale="f", levels=[1], facecolor="#efefdb")  # Land color matches inset
ax.add_feature(land, zorder=1)

cbaxes = inset_axes(ax, width="30%", height="3%", loc=3)
# Create scatter plot for oxygen content
scatter = ax.scatter(df['Lon'], df['Lat'], c=df['bottom_ox'], cmap="inferno", s=100, edgecolor="k")

# Add colorbar to the inset axes
plt.colorbar(scatter, cax=cbaxes, ticks=[0, 7], orientation='horizontal')

"""
Add an inset
"""
axins = inset_axes(ax, width="30%", height="30%", loc="upper left",
                   axes_class=cartopy.mpl.geoaxes.GeoAxes,
                   axes_kwargs=dict(map_projection=cartopy.crs.PlateCarree()))
axins.set_extent([165.6, 179, -47.5, -34.4], crs=ccrs.PlateCarree())

land2 = cf.GSHHSFeature(scale="i", levels=[1], facecolor="#efefdb")  # Land color matches inset
axins.add_feature(land2, zorder=1)

axins.add_patch(Rectangle(
    (166.7, -45.6),
    167.3 - 166.7,
    -45 - (-45.6),
    facecolor="none",
    edgecolor="red",
    linewidth=5,
    transform=ccrs.PlateCarree(),
    zorder=3
))

axins.add_feature(cartopy.feature.COASTLINE)
plt.show()

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/EOI_MAP/main2.png', dpi=300, bbox_inches="tight")
#
#
#
















