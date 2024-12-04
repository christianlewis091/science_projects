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
    plt.show()
    # plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/checking_results4/{title1}.png', dpi=300, bbox_inches="tight")
    # plt.close()


"""
CHECK THE SMOOTHED LATITIUDES FROM LINE 54-64
"""
def map2(x,y, title1):
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

    ax.scatter(
        x,
        y,
        transform=ccrs.PlateCarree(),  # Data is in lat/lon format
        linestyle=line_sys[i % len(line_sys)],  # Cycle through line styles
        label=fronts[i], color='red')

    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_submission/Images_and_Figures/GLODAP/{title1}.png', dpi=300, bbox_inches="tight")
    plt.close()

def map3(df, row, a, title1): # checking the data is in the right place fpr later
    # ADD FIGURE TO CHECK
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=-155, central_latitude=-90))
    ax.add_feature(cf.OCEAN)
    ax.add_feature(cf.LAND, edgecolor='black')
    ax.gridlines()

    fronts = np.unique(acc_fronts['front_name'])
    fronts = ['PF', 'SAF', 'STF', 'Boundary']
    line_sys = ['dotted', 'dashed', 'dashdot', 'solid']
    # ORSI FRONTS
    for q in range(len(fronts)):
        this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[q]]
        latitudes = this_one['latitude'].values  # Convert to numpy array if necessary
        longitudes = this_one['longitude'].values

        ax.plot(
            longitudes,
            latitudes,
            transform=ccrs.PlateCarree(),  # Data is in lat/lon format
            linestyle=line_sys[q % len(line_sys)],  # Cycle through line styles
            label=fronts[q], color='black')

    # MY SMOOTHED FRONTS
    # smoothed_lats = df[['STF_smoothed_LAT','SAF_smoothed_LAT','PF_smoothed_LAT','Boundary_smoothed_LAT']]
    ax.plot(df['LONGITUDE'],df['STF_smoothed_LAT'], transform=ccrs.PlateCarree(), label='STF_smoothed_LAT', color='red')
    ax.plot(df['LONGITUDE'],df['SAF_smoothed_LAT'], transform=ccrs.PlateCarree(), label='SAF_smoothed_LAT', color='red')
    ax.plot(df['LONGITUDE'],df['PF_smoothed_LAT'], transform=ccrs.PlateCarree(), label='PF_smoothed_LAT', color='red')
    ax.plot(df['LONGITUDE'],df['Boundary_smoothed_LAT'], transform=ccrs.PlateCarree(), label='Boundary_smoothed_LAT', color='red')

    sc = ax.scatter(row['LONGITUDE'], row['LATITUDE'], transform=ccrs.PlateCarree(), color='green')  # Data is in lat/lon format)
    plt.title(f'{a}')
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_GLODAP_check_Nov29_2024/checking_results4/{title1}.png', dpi=300, bbox_inches="tight")
    plt.close()


