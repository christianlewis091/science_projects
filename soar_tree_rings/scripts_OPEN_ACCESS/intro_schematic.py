import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap
from X_miller_curve_algorithm import ccgFilter

"""
create the data to plot
"""


# acc_fronts = pd.read_csv(r'H:\Science\Datasets\ACC_fronts\csv\antarctic_circumpolar_current_fronts.csv')
# values = list(np.arange(-180, 181, 0.5))
# n = 3 # set the amount of times the code will iterate (set to 10,000 once everything is final)
# cutoff = 667  # FFT filter cutoff
#
# # Do this for each front
# fronts = np.unique(acc_fronts['front_name'])
# fronts = ['PF','SAF','STF','Boundary']
# line_sys = ['dotted','dashed','dashdot','solid','dotted','dashed','dashdot']
#
# res = pd.DataFrame()
# # create a smoothed front
# for i in range(0, len(fronts)):
#     this_one = acc_fronts.loc[acc_fronts['front_name'] == fronts[i]]
#     latitudes = this_one['latitude'].reset_index(drop=True)
#     longitudes = this_one['longitude'].reset_index(drop=True)
#     yerr = latitudes*.01
#
#     #dynamically name a variable
#     # GET SMOOTH VALUE: SET OUTPUT TO WHEREVER WE LAVE LONGUITUDE DATA FOR THE MEANS
#     smoothed = ccgFilter(longitudes, latitudes, cutoff).getSmoothValue(values)
#     smoothed = pd.DataFrame({"smoothed_vals": smoothed, "lons": values})
#     smoothed['front'] = fronts[i]
#     res = pd.concat([res, smoothed], ignore_index=True)

# res.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_intro_schematic/test.xlsx')

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_intro_schematic/test.xlsx')

PF = df.loc[df['front'] == 'PF']
SAF = df.loc[df['front'] == 'SAF']
STF = df.loc[df['front'] == 'STF']
Bound = df.loc[df['front'] == 'Boundary']

PF_x = PF['smoothed_vals']
SAF_x = SAF['smoothed_vals']
STF_x = STF['smoothed_vals']
Bound_x = Bound['smoothed_vals']

PF_y = PF['lons']
SAF_y = SAF['lons']
STF_y = STF['lons']
Bound_y = Bound['lons']


fronts = ['PF','SAF','STF','Boundary']

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='ortho',lon_0=-150,lat_0=-90,resolution='l')
m.drawmapboundary(fill_color='lightgrey')
m.fillcontinents(color='darkgrey')
# m.shadedrelief()
m.drawcoastlines(linewidth=0.1)

c, d = m(STF_y, STF_x)
m.plot(c, d, color='lightcoral')

c, d = m(SAF_y, SAF_x)
m.plot(c, d, color='peru')

a, b = m(PF_y, PF_x)
m.plot(a, b, color='skyblue')

c, d = m(Bound_y, Bound_x)
m.plot(c, d, color='dodgerblue')

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_intro_schematic/fig.png',
            dpi=300, bbox_inches="tight")


























