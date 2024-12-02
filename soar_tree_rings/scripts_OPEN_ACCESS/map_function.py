import pandas as pd
import numpy as np
from X_miller_curve_algorithm import ccgFilter
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt


acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')

def map1(df, var,title1):
    # Create a figure
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))

    # First Subplot: Nitrate Map
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.LAND, edgecolor='black')
    ax.gridlines()
    ax.set_title(f'{title1}')

    fronts = np.unique(acc_fronts['front_name'])
    fronts = ['PF', 'SAF', 'STF', 'Boundary']
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

    # add the nitrate and 14C data
    dfn = df.loc[df[f'{var}'] > -999]
    latitudes_data = dfn['LATITUDE'].values
    longitudes_data = dfn['LONGITUDE'].values
    nitrate_data = dfn[f'{var}'].values
    sc = ax.scatter(
        longitudes_data,
        latitudes_data,
        c=nitrate_data,
        cmap='coolwarm',
        transform=ccrs.PlateCarree())  # Data is in lat/lon format)
    cb = plt.colorbar(sc, ax=ax, orientation='vertical', pad=0.05, label='Nitrate (\u03BCM)')
    # Show the plot

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/checking_results/{title1}.png', dpi=300, bbox_inches="tight")


