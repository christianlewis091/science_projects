"""
The creation of this file was brought on by the meeting I had with Sara Fletcher and Erik Behrens at NIWA on
Feb 24, 2023.

The following ideas were brought up:
1. I can compare my records / 5-year latitdinally banded averages to Landschutzer's data, which is publicly available.
https://www.ncei.noaa.gov/access/ocean-carbon-acidification-data-system/oceans/SPCO2_1982_2015_ETH_SOM_FFN.html

2. We should de-trend the trends from the main plot (Plot 7).
3. Can look at average D14C through time, relative to atmosphere (Wannikov Style); this will look similar to Heather Graven's 2012 paper
4. Calculate the component of our trend that can be explained through temperature alone (temperature can explain a lot, cold water will absorb more gas and change the solubility). Start with the Sarmiento and Gruber Textbook.
5. We should be able to seperate the trends we see into two categories, components affected by 1) temperature and 2) upwelling.
6. Look at Erik's NEMO Model, binning two boxes for the Pacific, and two boxes for the Indian Ocean (don't locate by latitude!), and see in the model if mixed layer depth in summer vs winter; summer may be the growing season, but winter will have deeper mixed layer and more outgassing.
7. If you compare the climatological runs (which have no temperture effect) with the real variability, we can isolate the component that is due to temperature.
8. We can use an age tracer in the model to...
9. Setup a monthly meeting with these guys.

"""
# grab the import info from the netcdf example file
from soar_analysis4 import *
from netcdf_example import *
import numpy as np
import pandas as pd
# grab this function I need from another program
from soar_analysis4 import apply_time_bands
import scipy
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend

#import the netcdf landschutzer data
nc_f = 'H:/Science/Datasets/spco2_1982-2015_MPI_SOM-FFN_v2016.nc'

# Dataset is the class behavior to open the file
nc_fid = Dataset(nc_f, 'r')

# function pulled from import statement; tells you the info in the file
# nc_attrs, nc_dims, nc_vars = ncdump(nc_fid)

# have a look at the variable of interest
fgc02_smooth = nc_fid['fgco2_smoothed']
# print(fgc02_smooth)

# extract data
# compressed removes mask
# list conversion allows future indexing
lats = nc_fid.variables['lat'][:].compressed().tolist()  # extract/copy the data
lons = nc_fid.variables['lon'][:].compressed().tolist()
print(lons)
time = nc_fid.variables['time_bnds'][:]

time = time[:,1]

# the latitude bands I'm interested in are as follows, going on from analysis 4 (see lines 54 - 70).
# because the indeces are in 0.5 degrees, I'll expand the boundaries as follows:
b1_max = -37.5  # index =
b1_min = -45.5
b1_index_max = lats.index(b1_max)
b1_index_min = lats.index(b1_min)
# print(b1_index_min)
# print(b1_index_max)
#
b2_max = -44.5
b2_min = -50.5
b2_index_max = lats.index(b2_max)
b2_index_min = lats.index(b2_min)
#
#
b3_max = -49.5
b3_min = -55.5
b3_index_max = lats.index(b3_max)
b3_index_min = lats.index(b3_min)
#
b4_max = -59.5
b4_min = -80.5
b4_index_max = lats.index(b4_max)
b4_index_min = lats.index(b4_min)

# # indexing for Indian Ocean - feed for New Zealand
a = 120.5
b = 60.5
c = -30.5
lon_max = [a, a+20, a+40]
lon_min = [b, b+20, b+40]
# # indeixing for Pacific - feeds to Chile
lon_max2 = [a, a+20, a+40]
lon_min2 = [c, c+20, c+40]

# arrays for later
slope_arr = []
intercept_arr = []
r_arr = []
p_arr = []
std_arr = []
label_arr = []
lonlab1=[]
lonlab2 = []
lonlab3 = []
lonlab4=[]

for k in range(0, 3):
    lon_index_max = lons.index(lon_max[k])
    lon_index_min = lons.index(lon_min[k])
    lon_index_max2 = lons.index(lon_max2[k])
    lon_index_min2 = lons.index(lon_min2[k])

# #
    # # Now I want to index the netCDF data within these bands, and average them, and find their STD, and make a plot similar
    # # to plot 7.
    # # first I need to identify the indeces where these latitudes are...should I put the lats and lons into a dataframe? No.
    # # Index them, and average across the lats and lon's, then you plot the result over TIME.
    # # ls is for landschutzer
    # # I'm following indexing pattern here https://stackoverflow.com/questions/49762136/how-to-index-a-netcdf-file-very-quickly
    # # dis[:,lat_index,lon_index]
    #

    def indexing_data(min_lat, max_lat, min_lon, max_lon):
        # CREATE BAND1; using latitudes defined above
        data = fgc02_smooth[:, min_lat:max_lat, min_lon:max_lon]

        # see how the shape has changed
        # print(f"The shape of band1_ls after indexing is {np.shape(band1_ls)}")

        # and its still 3D
        # print(f"DIMENSIONS of band1_ls after indexing is {band1_ls.ndim}")
        # now let's average across the latitudes first

        # Average across LATITUDES
        data = np.ma.average(data, axis=1, keepdims=True)
        # print(f"After averaging across LATITUDES, the shape is {np.shape(band1_ls)}")

        # Average across LONGITUDES
        data = np.ma.average(data, axis=2, keepdims=True)
        # print(f"After averaging across LONGITUDES, the shape is {np.shape(band1_ls)}")

        # get rid of one dimension
        data = np.squeeze(data)

        return data

    # indexing for Indian Ocean - feed for New Zealand
    band1_ls = indexing_data(b1_index_min,b1_index_max, lon_index_min,lon_index_max)
    band2_ls = indexing_data(b2_index_min,b2_index_max, lon_index_min,lon_index_max)
    band3_ls = indexing_data(b3_index_min,b3_index_max, lon_index_min,lon_index_max)
    band4_ls = indexing_data(b4_index_min,b4_index_max, lon_index_min,lon_index_max)

    #TODO go back and fix these LONGITUDES (when I use Lons_min2, max2, the data gets weird; wrong lon's?)
    # indexing by lats and lon for Pacific feeding into Chile
    band1_ls2 = indexing_data(b1_index_min,b1_index_max, lon_index_min2,lon_index_max2)
    band2_ls2 = indexing_data(b2_index_min,b2_index_max, lon_index_min2,lon_index_max2)
    band3_ls2 = indexing_data(b3_index_min,b3_index_max, lon_index_min2,lon_index_max2)
    band4_ls2 = indexing_data(b4_index_min,b4_index_max, lon_index_min2,lon_index_max2)

    x = pd.DataFrame({"Time": time,
                      "Band1_NZ": band1_ls,
                      "Band2_NZ": band2_ls,
                      "Band3_NZ": band3_ls,
                      "Band4_NZ": band4_ls,
                      "Band1_CH": band1_ls2,
                      "Band2_CH": band2_ls2,
                      "Band3_CH": band3_ls2,
                      "Band4_CH": band4_ls2})

    # add the time back into years
    conversion = 31540000
    df_2['Landschutzer_time'] = (df_2['Decimal_date'] - 2000) * conversion
    x['Decimal_date'] = (x['Time']/conversion)+2000
    # print(x['Decimal_date'])


    # run that function
    x['Time_Bands'] = apply_time_bands(x)

    # grab the means of the lanschutzer data
    landschutz_means = x.groupby('Time_Bands').mean().reset_index()
    landschutz_std = x.groupby('Time_Bands').std().reset_index()


    """
    At this point, I can't compare the two datasets directly, because the x-values are not the same. How to solve this? 
    The old favorite - CCGCRV curve smoothing
    
    The function needs the following: 
    def monte_carlo_randomization_trend(x_init, fake_x, y_init, y_error, cutoff, n):  # explanation of arguments above
    """
    n = 10  # set the amount of times the code will iterate (set to 10,000 once everything is final)
    cutoff = 667  # FFT filter cutoff

    output_xs = np.linspace(1980, 2020, num=8)


    landschutz_band1_ch = monte_carlo_randomization_trend(landschutz_means['Decimal_date'], output_xs, landschutz_means['Band1_CH'], landschutz_std['Band1_CH'], cutoff, n)
    landschutz_band1_ch = landschutz_band1_ch[2]

    landschutz_band2_ch = monte_carlo_randomization_trend(landschutz_means['Decimal_date'], output_xs, landschutz_means['Band2_CH'], landschutz_std['Band2_CH'], cutoff, n)
    landschutz_band2_ch = landschutz_band2_ch[2]

    landschutz_band3_ch = monte_carlo_randomization_trend(landschutz_means['Decimal_date'], output_xs, landschutz_means['Band1_CH'], landschutz_std['Band1_CH'], cutoff, n)
    landschutz_band3_ch = landschutz_band3_ch[2]

    landschutz_band1_nz = monte_carlo_randomization_trend(landschutz_means['Decimal_date'], output_xs, landschutz_means['Band1_NZ'], landschutz_std['Band1_NZ'], cutoff, n)
    landschutz_band1_nz = landschutz_band1_nz[2]

    landschutz_band2_nz = monte_carlo_randomization_trend(landschutz_means['Decimal_date'], output_xs, landschutz_means['Band2_NZ'], landschutz_std['Band2_NZ'], cutoff, n)
    landschutz_band2_nz = landschutz_band2_nz[2]

    landschutz_band3_nz = monte_carlo_randomization_trend(landschutz_means['Decimal_date'], output_xs, landschutz_means['Band1_NZ'], landschutz_std['Band1_NZ'], cutoff, n)
    landschutz_band3_nz = landschutz_band3_nz[2]

    trees_band1_ch = monte_carlo_randomization_trend(means_ch1['Decimal_date'], output_xs, means_ch1['r2_diff_trend'], means_ch1['r2_diff_trend_errprop'], cutoff, n)
    trees_band1_ch = trees_band1_ch[2]

    trees_band2_ch = monte_carlo_randomization_trend(means_ch2['Decimal_date'], output_xs, means_ch2['r2_diff_trend'], means_ch2['r2_diff_trend_errprop'], cutoff, n)
    trees_band2_ch = trees_band2_ch[2]

    trees_band3_ch = monte_carlo_randomization_trend(means_ch3['Decimal_date'], output_xs, means_ch3['r2_diff_trend'], means_ch3['r2_diff_trend_errprop'], cutoff, n)
    trees_band3_ch = trees_band3_ch[2]

    trees_band1_nz = monte_carlo_randomization_trend(means_nz1['Decimal_date'], output_xs, means_nz1['r2_diff_trend'], means_nz1['r2_diff_trend_errprop'], cutoff, n)
    trees_band1_nz = trees_band1_nz[2]

    trees_band2_nz = monte_carlo_randomization_trend(means_nz2['Decimal_date'], output_xs, means_nz2['r2_diff_trend'], means_nz2['r2_diff_trend_errprop'], cutoff, n)
    trees_band2_nz = trees_band2_nz[2]

    trees_band3_nz = monte_carlo_randomization_trend(means_nz3['Decimal_date'], output_xs, means_nz3['r2_diff_trend'], means_nz3['r2_diff_trend_errprop'], cutoff, n)
    trees_band3_nz = trees_band3_nz[2]

    output_xs = pd.DataFrame({"output_xs": output_xs})
    ccgcrv_output = pd.DataFrame({"output_xs": output_xs['output_xs'],
                                  "landshutz_Band1_CH": landschutz_band1_ch['Means'],
                                  "landshutz_Band2_CH": landschutz_band2_ch['Means'],
                                  "landshutz_Band3_CH": landschutz_band3_ch['Means'],
                                  "landshutz_Band1_NZ": landschutz_band1_nz['Means'],
                                  "landshutz_Band2_NZ": landschutz_band2_nz['Means'],
                                  "landshutz_Band3_NZ": landschutz_band3_nz['Means'],
                                  "Trees_band1_CH": trees_band1_ch['Means'],
                                  "Trees_band2_CH": trees_band2_ch['Means'],
                                  "Trees_band3_CH": trees_band3_ch['Means'],
                                  "Trees_band1_NZ": trees_band1_nz['Means'],
                                  "Trees_band2_NZ": trees_band2_nz['Means'],
                                  "Trees_band3_NZ": trees_band3_nz['Means'],
                                  "landshutz_Band1_CH_std": landschutz_band1_ch['stdevs'],
                                  "landshutz_Band2_CH_std": landschutz_band2_ch['stdevs'],
                                  "landshutz_Band3_CH_std": landschutz_band3_ch['stdevs'],
                                  "landshutz_Band1_NZ_std": landschutz_band1_nz['stdevs'],
                                  "landshutz_Band2_NZ_std": landschutz_band2_nz['stdevs'],
                                  "landshutz_Band3_NZ_std": landschutz_band3_nz['stdevs'],
                                  "Trees_band1_CH_std": trees_band1_ch['stdevs'],
                                  "Trees_band2_CH_std": trees_band2_ch['stdevs'],
                                  "Trees_band3_CH_std": trees_band3_ch['stdevs'],
                                  "Trees_band1_NZ_std": trees_band1_nz['stdevs'],
                                  "Trees_band2_NZ_std": trees_band2_nz['stdevs'],
                                  "Trees_band3_NZ_std": trees_band3_nz['stdevs']})

    """
    Calculate the stats between each latitude band
    """

    label = ['Band 1, Chile', 'Band 2, Chile', 'Band 3, Chile', 'Band 1, New Zealand', 'Band 2, New Zealand', 'Band 3, New Zealand']
    items = [ccgcrv_output["landshutz_Band1_CH"], ccgcrv_output["landshutz_Band2_CH"], ccgcrv_output["landshutz_Band3_CH"], ccgcrv_output["landshutz_Band1_NZ"],ccgcrv_output["landshutz_Band2_NZ"],ccgcrv_output["landshutz_Band3_NZ"]]
    things = [ccgcrv_output["Trees_band1_CH"], ccgcrv_output["Trees_band2_CH"], ccgcrv_output["Trees_band3_CH"], ccgcrv_output["Trees_band1_NZ"],ccgcrv_output["Trees_band2_NZ"],ccgcrv_output["Trees_band3_NZ"]]

    for i in range(0, len(items)):
        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(items[i], things[i])

        label_arr.append(label[i])
        slope_arr.append(slope)
        intercept_arr.append(intercept)
        r_arr.append(r_value)
        p_arr.append(p_value)
        std_arr.append(std_err)
        lonlab1.append(lon_max[k])
        lonlab2.append(lon_min[k])
        lonlab3.append(lon_max2[k])
        lonlab4.append(lon_min2[k])

lolz = pd.DataFrame({ "Label": label_arr,
                     "CHile Lon Min": lonlab1,
                     "CHile Lon Max": lonlab2,
                     "NZ Lon Min": lonlab3,
                     "NZ Lon Max": lonlab4,
                     "Slope": slope_arr,
                     "Intercept": intercept_arr,
                     "R2": r_arr,
                     "Pvalue": p_arr,
                     "Std_err": std_arr})
#
print(lolz)
lolz.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/stats2.xlsx')

"""
The following two plots are the result of SOAR_ANALYSIS4 (see plot7) AND the landschutzer data indexed by latitude
and longitude (for NZ data, Landschutzer data is indexed by latitude and the INDIAN Ocean; for Chile data, the Pacific Ocean)
How do they compare to a high level?
"""
fig = plt.figure(figsize=(9, 9))
gs = gridspec.GridSpec(6, 4)
gs.update(wspace=.75, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.title(f"Chile Tree Ring Data, {b1_max} to {b1_min}", fontsize=11)
plt.plot(means_ch1['Decimal_date'], means_ch1['r2_diff_trend'], label='Tree Rings', color = a1)
plt.fill_between(means_ch1['Decimal_date'], (means_ch1['r2_diff_trend']+stds_ch1['r2_diff_trend']), (means_ch1['r2_diff_trend']-stds_ch1['r2_diff_trend']), alpha = 0.3, color = a1)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.title(f"Chile Tree Ring Data, {b2_max} to {b2_min}", fontsize=11)
plt.plot(means_ch2['Decimal_date'], means_ch2['r2_diff_trend'], label='Tree Rings', color = a3)
plt.fill_between(means_ch2['Decimal_date'], (means_ch2['r2_diff_trend']+stds_ch2['r2_diff_trend']), (means_ch2['r2_diff_trend']-stds_ch2['r2_diff_trend']), alpha = 0.3, color = a3)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - Reference]', color='black', fontsize=11)

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.title(f"Chile Tree Ring Data, {b3_max} to {b3_min}", fontsize=11)
plt.plot(means_ch3['Decimal_date'], means_ch3['r2_diff_trend'], label='Tree Rings', color = a5)
plt.fill_between(means_ch3['Decimal_date'], (means_ch3['r2_diff_trend']+stds_ch3['r2_diff_trend']), (means_ch3['r2_diff_trend']-stds_ch3['r2_diff_trend']), alpha = 0.3, color = a5)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.title(f"Lanschutzer Model, {b1_max} to {b1_min}", fontsize=11)
plt.plot(landschutz_means['Decimal_date'], landschutz_means['Band1_CH'], label='Model', color = a1)
plt.fill_between(landschutz_means['Decimal_date'], (landschutz_means['Band1_CH']+landschutz_std['Band1_CH']), (landschutz_means['Band1_CH']-landschutz_std['Band1_CH']), alpha = 0.3, color = a1)

xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.title(f"Lanschutzer Model, {b2_max} to {b2_min}", fontsize=11)
plt.plot(landschutz_means['Decimal_date'], landschutz_means['Band2_CH'], label='Model', color = a3)
plt.fill_between(landschutz_means['Decimal_date'], (landschutz_means['Band2_CH']+landschutz_std['Band2_CH']), (landschutz_means['Band2_CH']-landschutz_std['Band2_CH']), alpha = 0.3, color = a3)

xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.title(f"Lanschutzer Model, {b3_max} to {b3_min}", fontsize=11)
plt.plot(landschutz_means['Decimal_date'], landschutz_means['Band3_CH'], label='Model', color = a5)
plt.fill_between(landschutz_means['Decimal_date'], (landschutz_means['Band3_CH']+landschutz_std['Band3_CH']), (landschutz_means['Band3_CH']-landschutz_std['Band3_CH']), alpha = 0.3, color = a5)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/analysis6_chile.png',
            dpi=300, bbox_inches="tight")


# """
# NZ data vs model
# """
fig = plt.figure(figsize=(9, 9))
gs = gridspec.GridSpec(6, 4)
gs.update(wspace=.75, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.title(f"NZ Tree Ring Data, {b1_max} to {b1_min}", fontsize=11)
plt.plot(means_nz1['Decimal_date'], means_nz1['r2_diff_trend'], label='Tree Rings', color = a1)
plt.fill_between(means_nz1['Decimal_date'], (means_nz1['r2_diff_trend']+stds_nz1['r2_diff_trend']), (means_nz1['r2_diff_trend']-stds_nz1['r2_diff_trend']), alpha = 0.3, color = a1)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.title(f"NZ Tree Ring Data, {b2_max} to {b2_min}", fontsize=11)
plt.plot(means_nz2['Decimal_date'], means_nz2['r2_diff_trend'], label='Tree Rings', color = a3)
plt.fill_between(means_nz2['Decimal_date'], (means_nz2['r2_diff_trend']+stds_nz2['r2_diff_trend']), (means_nz2['r2_diff_trend']-stds_nz2['r2_diff_trend']), alpha = 0.3, color = a3)
plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030) [Sample - Reference]', color='black', fontsize=11)

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.title(f"NZ Tree Ring Data, {b3_max} to {b3_min}", fontsize=11)
plt.plot(means_nz3['Decimal_date'], means_nz3['r2_diff_trend'], label='Tree Rings', color = a5)
plt.fill_between(means_nz3['Decimal_date'], (means_nz3['r2_diff_trend']+stds_nz3['r2_diff_trend']), (means_nz3['r2_diff_trend']-stds_nz3['r2_diff_trend']), alpha = 0.3, color = a5)

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.title(f"Lanschutzer Model, {b1_max} to {b1_min}", fontsize=11)
plt.plot(landschutz_means['Decimal_date'], landschutz_means['Band1_NZ'], label='Model', color = a1)
plt.fill_between(landschutz_means['Decimal_date'], (landschutz_means['Band1_NZ']+landschutz_std['Band1_NZ']), (landschutz_means['Band1_NZ']-landschutz_std['Band1_NZ']), alpha = 0.3, color = a1)

xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.title(f"Lanschutzer Model, {b2_max} to {b2_min}", fontsize=11)
plt.plot(landschutz_means['Decimal_date'], landschutz_means['Band2_NZ'], label='Model', color = a3)
plt.fill_between(landschutz_means['Decimal_date'], (landschutz_means['Band2_NZ']+landschutz_std['Band2_NZ']), (landschutz_means['Band2_NZ']-landschutz_std['Band2_NZ']), alpha = 0.3, color = a3)

xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.title(f"Lanschutzer Model, {b3_max} to {b3_min}", fontsize=11)
plt.plot(landschutz_means['Decimal_date'], landschutz_means['Band3_NZ'], label='Model', color = a5)
plt.fill_between(landschutz_means['Decimal_date'], (landschutz_means['Band3_NZ']+landschutz_std['Band3_NZ']), (landschutz_means['Band3_NZ']-landschutz_std['Band3_NZ']), alpha = 0.3, color = a5)
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/analysis6_newzealand.png',
            dpi=300, bbox_inches="tight")

"""
Whats the result/comparability of my results and landschutzers after I relate them in time (using CCGCRV)
"""
fig = plt.figure(figsize=(9, 9))
gs = gridspec.GridSpec(6, 4)
gs.update(wspace=.75, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.scatter(ccgcrv_output["landshutz_Band1_CH"], ccgcrv_output["Trees_band1_CH"])
plt.xlabel('Landschutzer Data')
plt.ylabel('Tree Data')

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.scatter(ccgcrv_output["landshutz_Band2_CH"], ccgcrv_output["Trees_band2_CH"])
plt.xlabel('Landschutzer Data')
plt.ylabel('Tree Data')

xtr_subsplot = fig.add_subplot(gs[4:6, 0:2])
plt.scatter(ccgcrv_output["landshutz_Band3_CH"], ccgcrv_output["Trees_band3_CH"])
plt.xlabel('Landschutzer Data')
plt.ylabel('Tree Data')

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.scatter(ccgcrv_output["landshutz_Band1_NZ"], ccgcrv_output["Trees_band1_NZ"])
plt.xlabel('Landschutzer Data')
plt.ylabel('Tree Data')

xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.scatter(ccgcrv_output["landshutz_Band2_NZ"], ccgcrv_output["Trees_band2_NZ"])
plt.xlabel('Landschutzer Data')
plt.ylabel('Tree Data')

xtr_subsplot = fig.add_subplot(gs[4:6, 2:4])
plt.scatter(ccgcrv_output["landshutz_Band3_NZ"], ccgcrv_output["Trees_band3_NZ"])
plt.xlabel('Landschutzer Data')
plt.ylabel('Tree Data')

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/analysis6_scatter.png',
            dpi=300, bbox_inches="tight")




















