import pysplit
import cartopy.crs as ccrs
import libproj-dev
import matplotlib.pyplot as plt


working_dir = r'C:/ProgramData/Microsoft/Windows/Start Menu/Programs/HYSPLIT'
storage_dir = r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output'
meteo_dir = r'H:/Science/Datasets/meterological_hysplit_data'
basename = 'colgate'
years = [2005]
months = [1]
hours = [11, 17, 23]
altitudes = [500, 1000, 1500]
location = (42.82, -75.54)
runtime = -120
#
pysplit.generate_bulktraj(basename, working_dir, storage_dir, meteo_dir,
                          years, months, hours, altitudes, location, runtime,
                          monthslice=slice(0, 32, 2), meteo_bookends=([3,4, 5], [1,2]),
                          get_reverse=True,get_clipped=True, hysplit="C:\ProgramData\Microsoft\Windows\Start Menu\Programs\HYSPLIT")

#
# trajgroup = pysplit.make_trajectorygroup(r'C:/trajectories/colgate/*feb*')

"""
Basemaps and MapDesign
----------------------
PySPLIT's ``MapDesign`` class uses the matplotlib Basemap toolkit to quickly
set up attractive maps.  The user is not restricted to using maps
produced from ``MapDesign``, however- any Basemap will serve in the section
below entitled 'Plotting ``Trajectory`` Paths.
Creating a basic cylindrical map using ``MapDesign``  only requires
``mapcorners``, a list of the lower-left longitude, lower-left latitude,
upper-right longitude, and upper-right latitude values.
The ``standard_pm``, a list of standard parallels and meridians,
may be passed as ``None``.
"""
# mapcorners =  [-150, 15, -50, 65]
# standard_pm = None
#
# bmap_params = pysplit.MapDesign(mapcorners, standard_pm)
#
# """
# Once the ``MapDesign`` is initialized it can be used to draw a map:
# """
# bmap = bmap_params.make_basemap()
#
# """
# Plotting ``Trajectory`` Paths
# -----------------------------
# For this example, we will color-code by initialization (t=0) altitude,
# (500, 1000, or 1500 m), which can be accessed via ``Trajectory.data.geometry``,
#  a ``GeoSeries`` of Shapely ``Point`` objects.
# We can store the trajectory color in ``Trajectory.trajcolor`` for convenience.
# """
# color_dict = {500.0 : 'blue',
#               1000.0 : 'orange',
#               1500.0 : 'black'}
#
# for traj in trajgroup:
#     altitude0 = traj.data.geometry.apply(lambda p: p.z)[0]
#     traj.trajcolor = color_dict[altitude0]
#
# """
# For display purposes, let's plot only every fifth ``Trajectory``.  The lats,
# lons are obtained by unpacking the ``Trajectory.Path``
# (Shapely ``LineString``) xy coordinates.
# """
# for traj in trajgroup[::5]:
#     bmap.plot(*traj.path.xy, c=traj.trajcolor, latlon=True, zorder=20)
#
# plt.show()
