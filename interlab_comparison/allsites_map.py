from matplotlib.patches import Polygon
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import seaborn as sns
import numpy as np

fig=plt.figure()
colors = sns.color_palette("rocket", 10)
colors2 = sns.color_palette("mako", 10)

# cmaps = {}
#
# gradient = np.linspace(0, 1, 256)
# gradient = np.vstack((gradient, gradient))
#
# cmaps = {}
# def plot_color_gradients(category, cmap_list):
#     # Create figure and adjust figure height to number of colormaps
#     nrows = len(cmap_list)
#     figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
#     fig, axs = plt.subplots(nrows=nrows + 1, figsize=(6.4, figh))
#     fig.subplots_adjust(top=1 - 0.35 / figh, bottom=0.15 / figh,
#                         left=0.2, right=0.99)
#     axs[0].set_title(f'{category} colormaps', fontsize=14)
#
#     for ax, name in zip(axs, cmap_list):
#         ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
#         ax.text(-0.01, 0.5, name, va='center', ha='right', fontsize=10,
#                 transform=ax.transAxes)
#
#     # Turn off *all* ticks & spines, not just the ones with colormaps.
#     for ax in axs:
#         ax.set_axis_off()
#
#     # Save colormap list for later.
#     cmaps[category] = cmap_list
#
#
# plot_color_gradients('Qualitative',
#                      ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
#                       'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
#                       'tab20c'])
#
# plt.close()
#

mpl.rcParams['pdf.fonttype'] = 3
mpl.rcParams['font.size'] = 7.5
size1 = 5

# CONVERT ALL LONS TO DEGREES EAST! (-1 * Lon WEST)
# Graven sites
samoa_y = -41  # S
samoa_x = -174
palmer_y = -64  # S
palmer_x = -64
pole_y = -90  # S
pole_x = 180  # W

# Heidelberg Sites
mcq_y = -54  # S
mcq_x = 158  # E
cgo_y = -40  # S
cgo_x = 144  # E
nmy_y = -70.65  # S
nmy_x = -8.2  # E

# DePolHolz Sites
s1_x = -70
s1_y = -18
s2_x = -70
s2_y = -33
s3_x = -70
s3_y = -40
s4_y = -53.749
s4_x = -70.97444

# our Monte Tarn
y = -53.749
x = -70.97444

# bhd v cgo
x1 = -41
y1 = 174
x2 = -40
y2 = 144

heidelberg_x = [mcq_x, cgo_x, nmy_x]
heidelberg_y = [mcq_y, cgo_y, nmy_y]
graven_x = [samoa_x, palmer_x, pole_x]
graven_y = [samoa_y, palmer_y, pole_y]
dph_x = [s1_x, s2_x, s3_x, s4_x]
dph_y = [s1_y, s2_y, s3_y, s4_y]
quickplot_x = [x1, x2]
quickplot_y = [y1, y2]

# SOAR Tree Ring Sites
df = pd.read_excel(r'H:\The Science\Datasets'
                   r'\SOARTreeRingData2022-02-01.xlsx')  # read in the Tree Ring data.
df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.
# chile['new_Lon'] = chile['Lon'] * -1
nz = df.loc[(df['Lon'] > 100)].reset_index(drop=True)
chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)].reset_index(drop=True)
chile['new_Lon'] = chile['Lon'] * -1

res = 'l'  # todo switch to i for intermediate
land = 'gray'
size1 = 35

fig = plt.figure()
map = Basemap(lat_0=-90, lon_0=170, resolution=res, projection='ortho')
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='white', linewidth=0.1)
map.fillcontinents(color=land, lake_color='gray')
map.drawcountries(linewidth=0.5)
map.drawcoastlines()
# a, b = map(chile_lon, chile_lat)
a, b = map(nz['Lon'], nz['Lat'])
c, d = map(chile['new_Lon'], chile['Lat'])
e, f = map(heidelberg_x, heidelberg_y)
g, h = map(graven_x, graven_y)
i, j = map(dph_x, dph_y)
map.scatter(a, b, marker='o',color='r', s = size1, label='SOAR Tree Rings', alpha = 1)
map.scatter(c, d, marker='o',color='r', s = size1)
map.scatter(i, j, marker='X',color='b', s = size1, label='University of Magallanes', alpha = 1)
map.scatter(e, f, marker='^',color='m', s = size1, label='University of Heidelberg, NaOH CO2 Measurements', alpha = 1)
map.scatter(g, h, marker='D',color='g', s = size1, label='SIO/LLNL, Flask CO2 Measurements', alpha = 1)

map.drawparallels(np.arange(-90.,120.,15.))
map.drawmeridians(np.arange(0.,360.,15.))
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05))

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/allsites_map4.png',
            dpi=300, bbox_inches="tight")
plt.close()


size1 = 100
fig = plt.figure()
map = Basemap(llcrnrlon=-85,llcrnrlat=-70,urcrnrlon=-60,urcrnrlat=20, resolution = 'l')
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='white', linewidth=0.1)
map.fillcontinents(color=land, lake_color='gray')
map.drawcountries(linewidth=0.5)
map.drawcoastlines()
a, b = map(nz['Lon'], nz['Lat'])
c, d = map(chile['new_Lon'], chile['Lat'])
e, f = map(heidelberg_x, heidelberg_y)
g, h = map(graven_x, graven_y)
i, j = map(dph_x, dph_y)
k, l = map(x, y)

map.scatter(i, j, marker='X',color='b', s = size1, label='University of Magallanes', alpha = 1)
map.scatter(k, l, marker='o',color='r', s = size1, label='RRL, Monte Tarn', alpha = 1)

map.drawparallels(np.arange(-90.,120.,30.))
map.drawmeridians(np.arange(0.,360.,60.))
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/reading_group_pres/Chilemap.png',
    dpi=300, bbox_inches="tight")
plt.close()


# bhd v cgo
y1 = -40.6833
x1 = 144.68
y2 = -41.4167
x2 = 174.8667  # bhd

size1 = 100
fig = plt.figure()
map = Basemap(llcrnrlon=140,llcrnrlat=-50,urcrnrlon=180,urcrnrlat=-30, resolution = 'l')
map.drawcoastlines(linewidth=0.5)
map.drawmapboundary(fill_color='white', linewidth=0.1)
map.fillcontinents(color=land, lake_color='gray')
map.drawcountries(linewidth=0.5)
map.drawcoastlines()
a, b = map(x1, y1)
c, d = map(x2, y2)

map.scatter(a, b, marker='X',color='b', s = size1, label='Cape Grim (UH)', alpha = 1)
map.scatter(c, d, marker='o',color='r', s = size1, label='Baring Head (RRL)', alpha = 1)

map.drawparallels(np.arange(-90.,120.,30.))
map.drawmeridians(np.arange(0.,360.,60.))
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/reading_group_pres/newmap.png',
    dpi=300, bbox_inches="tight")
plt.close()












































#
#
# fig = plt.figure()
#
# map = Basemap(lat_0=-90, lon_0=170, resolution=res, projection='ortho')
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.1)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries(linewidth=0.5)
# map.drawcoastlines()
# # a, b = map(chile_lon, chile_lat)
# maxlat = -30
# minlat = -60
# nz_max_lon = 180
# nz_min_lon = 160
# x1, y1 = map(nz_min_lon, maxlat)
# x2, y2 = map(nz_max_lon, maxlat)
# x3, y3 = map(nz_max_lon, minlat)
# x4, y4 = map(nz_min_lon, minlat)
# poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor="none", edgecolor='black',linewidth=1, alpha=1)
# plt.gca().add_patch(poly)
# a, b = map(nz['Lon'], nz['Lat'])
# c, d = map(chile['new_Lon'], chile['Lat'])
# e, f = map(heidelberg_x, heidelberg_y)
# g, h = map(graven_x, graven_y)
# # map.scatter(a, b, marker='o',color=colors[2], s = size1, label='SOAR Tree Rings')
# # map.scatter(c, d, marker='o',color=colors[2], s = size1)
# # map.scatter(e, f, marker='^',color='r', s = size1, label='University of Heidelberg, NaOH CO2 Measurements')
# # map.scatter(g, h, marker='D',color='b', s = size1, label='SIO/LLNL, Flask CO2 Measurements')
# # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
# #            ncol=2, borderaxespad=0.)
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/nz_map2.png',
#             dpi=300, bbox_inches="tight")
#
# plt.close()
#
# fig = plt.figure()
#
# map = Basemap(lat_0=-90, lon_0=170, resolution=res, projection='ortho')
# map.drawcoastlines(linewidth=0.5)
# map.drawmapboundary(fill_color='paleturquoise', linewidth=0.1)
# map.fillcontinents(color=land, lake_color='aqua')
# map.drawcountries(linewidth=0.5)
# map.drawcoastlines()
# # a, b = map(chile_lon, chile_lat)
# maxlat = -30
# minlat = -60
# nz_max_lon = 180
# nz_min_lon = 160
# x1, y1 = map(nz_min_lon, maxlat)
# x2, y2 = map(nz_max_lon, maxlat)
# x3, y3 = map(nz_max_lon, minlat)
# x4, y4 = map(nz_min_lon, minlat)
# poly = Polygon([(x1,y1),(x2,y2),(x3,y3),(x4,y4)], facecolor="none", edgecolor='black',linewidth=1, alpha=1)
# plt.gca().add_patch(poly)
# a, b = map(nz['Lon'], nz['Lat'])
# c, d = map(chile['new_Lon'], chile['Lat'])
# e, f = map(heidelberg_x, heidelberg_y)
# g, h = map(graven_x, graven_y)
#
# map.scatter(a, b, marker='o',color=colors[2], s = size1, label='SOAR Tree Rings')
# map.scatter(c, d, marker='o',color=colors[2], s = size1)
# # map.scatter(e, f, marker='^',color='r', s = size1, label='University of Heidelberg, NaOH CO2 Measurements')
# # map.scatter(g, h, marker='D',color='b', s = size1, label='SIO/LLNL, Flask CO2 Measurements')
# # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left',
# #            ncol=2, borderaxespad=0.)
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/nz_map3.png',
#             dpi=300, bbox_inches="tight")
#
# plt.close()
#
#
#


















