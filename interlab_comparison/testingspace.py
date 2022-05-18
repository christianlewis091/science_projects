"""
https://matplotlib.org/basemap/users/examples.html
https://basemaptutorial.readthedocs.io/en/latest/first_map.html
"""

# import numpy as np
# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# from datetime import datetime
# # miller projection
# map = Basemap(projection='mill',lon_0=180)
# # plot coastlines, draw label meridians and parallels.
# map.drawcoastlines()
# map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
# map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
# # fill continents 'coral' (with zorder=0), color wet areas 'aqua'
# map.drawmapboundary(fill_color='aqua')
# map.fillcontinents(color='coral',lake_color='aqua')
# # shade the night areas, with alpha transparency so the
# # map shows through. Use current time in UTC.
# date = datetime.utcnow()
# # CS=map.nightshade(date)
# plt.title('Day/Night Map for %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))
# plt.show()

###########################################################################################

# from mpl_toolkits.basemap import Basemap
# import matplotlib.pyplot as plt
# import numpy as np
# # set up orthographic map projection with
# # perspective of satellite looking down at 50N, 100W.
# # use low resolution coastlines.
# map = Basemap(projection='ortho',lat_0=45,lon_0=-100,resolution='l')
# # draw coastlines, country boundaries, fill continents.
# map.drawcoastlines(linewidth=0.25)
# map.drawcountries(linewidth=0.25)
# map.fillcontinents(color='coral',lake_color='aqua')
# # draw the edge of the map projection region (the projection limb)
# map.drawmapboundary(fill_color='aqua')
# # draw lat/lon grid lines every 30 degrees.
# map.drawmeridians(np.arange(0,360,30))
# map.drawparallels(np.arange(-90,90,30))
# # make up some data on a regular lat/lon grid.
# nlats = 73; nlons = 145; delta = 2.*np.pi/(nlons-1)
# lats = (0.5*np.pi-delta*np.indices((nlats,nlons))[0,:,:])
# lons = (delta*np.indices((nlats,nlons))[1,:,:])
# wave = 0.75*(np.sin(2.*lats)**8*np.cos(4.*lons))
# mean = 0.5*np.cos(2.*lats)*((np.sin(2.*lats))**2 + 2.)
# # compute native map projection coordinates of lat/lon grid.
# x, y = map(lons*180./np.pi, lats*180./np.pi)
# # contour data over the map.
# cs = map.contour(x,y,wave+mean,15,linewidths=1.5)
# plt.title('contour lines over filled continent background')
# plt.show()

"""
another example
"""

# from mpl_toolkits.basemap import Basemap
# import numpy as np
# import matplotlib.pyplot as plt
# # create new figure, axes instances.
# fig=plt.figure()
# ax=fig.add_axes([0.1,0.1,0.8,0.8])
# # setup mercator map projection.
# m = Basemap(llcrnrlon=-100.,llcrnrlat=20.,urcrnrlon=20.,urcrnrlat=60., \
#             rsphere=(6378137.00,6356752.3142), \
#             resolution='l',projection='merc', \
#             lat_0=40.,lon_0=-20.,lat_ts=20.)
# # nylat, nylon are lat/lon of New York
# nylat = 40.78; nylon = -73.98
# # lonlat, lonlon are lat/lon of London.
# lonlat = 51.53; lonlon = 0.08
# # draw great circle route between NY and London
# m.drawgreatcircle(nylon,nylat,lonlon,lonlat,linewidth=2,color='b')
# m.drawcoastlines()
# m.fillcontinents()
# # draw parallels
# m.drawparallels(np.arange(10,90,20),labels=[1,1,0,1])
# # draw meridians
# m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
# ax.set_title('Great Circle from New York to London')
# plt.show()