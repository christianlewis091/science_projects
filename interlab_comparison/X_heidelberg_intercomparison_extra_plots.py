import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

# the raw data for plotting
from heidelberg_intercomparison import xtot_bhd, ytot_bhd, ztot_bhd  # full dates, data, and measurements errors: BHD
from heidelberg_intercomparison import xtot_heid, ytot_heid, ztot_heid  # same as above, for Heidelberg
from heidelberg_intercomparison import x_combined, y_combined  # full baring head data with 1995-2005 removed.
# data (1, 2, 3, 4, 5) corresponds to time intervals (1987 - 1991, 1991 - 1994, 2006 - 2016, 2006 - 2009, 2012 - 2016)
from heidelberg_intercomparison import x1_bhd, y1_bhd, z1_bhd, \
    x2_bhd, y2_bhd, z2_bhd, \
    x3_bhd, y3_bhd, z3_bhd, \
    x4_bhd, y4_bhd, z4_bhd, \
    x5_bhd, y5_bhd, z5_bhd
from heidelberg_intercomparison import x1_heid, y1_heid, z1_heid, \
    x2_heid, y2_heid, z2_heid, \
    x3_heid, y3_heid, z3_heid, \
    x4_heid, y4_heid, z4_heid, \
    x5_heid, y5_heid, z5_heid
# x-dates that I specify for output of the Monte Carlo and CCGCRV smoothing Algorith, so I can directly compare data
from heidelberg_intercomparison import my_x_1986_1991, \
    my_x_1991_1994, \
    my_x_2006_2016, \
    my_x_2006_2009, \
    my_x_2012_2016
from heidelberg_intercomparison import baringhead_xtot_smoothed, \
    baringhead_ytot_smoothed, \
    heidelberg_xtot_smoothed, \
    heidelberg_ytot_smoothed
# simple monthyl mean curve smoothing to visualize the data
from heidelberg_intercomparison import x_ccgcv_bhd1, \
    y_ccgcv_bhd1, \
    x_ccgcv_bhd2, \
    y_ccgcv_bhd2, \
    x_ccgcv_bhd3, \
    y_ccgcv_bhd3, \
    x_ccgcv_bhd4, \
    y_ccgcv_bhd4, \
    x_ccgcv_bhd5, \
    y_ccgcv_bhd5, \
    x_ccgcv_heid1, x_ccgcv_heid2, x_ccgcv_heid3, x_ccgcv_heid4, x_ccgcv_heid5, \
    y_ccgcv_heid1, y_ccgcv_heid2, y_ccgcv_heid3, y_ccgcv_heid4, y_ccgcv_heid5, heidelberg_1986_1991_results_smooth, \
    summary

# example DataFrame that is output from the Monte Carlo Randomization, for a Supp Info, or presentation plot
# the first is the randomized data, the second is the randomized data put through the getSmoothValues()
from heidelberg_intercomparison import heidelberg_1986_1991_randoms_smooth, heidelberg_1986_1991_smoothcurves_smooth

# results from the smoothing using MonteCarlo analysis and CCGCRV getSmoothValue()
from heidelberg_intercomparison import bhd_1986_1991_mean_smooth, \
    bhd_1991_1994_mean_smooth, \
    bhd_2006_2016_mean_smooth, \
    bhd_2006_2009_mean_smooth, \
    bhd_2012_2016_mean_smooth
from heidelberg_intercomparison import heidelberg_1986_1991_mean_smooth, \
    heidelberg_1991_1994_mean_smooth, \
    heidelberg_2006_2016_mean_smooth, \
    heidelberg_2006_2009_mean_smooth, \
    heidelberg_2012_2016_mean_smooth
from heidelberg_intercomparison import bhd_1986_1991_stdevs_smooth, \
    bhd_1991_1994_stdevs_smooth, \
    bhd_2006_2016_stdevs_smooth, \
    bhd_2006_2009_stdevs_smooth, \
    bhd_2012_2016_stdevs_smooth
from heidelberg_intercomparison import heidelberg_1986_1991_stdevs_smooth, \
    heidelberg_1991_1994_stdevs_smooth, \
    heidelberg_2006_2016_stdevs_smooth, \
    heidelberg_2006_2009_stdevs_smooth, \
    heidelberg_2012_2016_stdevs_smooth

# results from the smoothing using MonteCarlo analysis and CCGCRV getTRENDValue()
from heidelberg_intercomparison import bhd_1986_1991_mean_trend, \
    bhd_1991_1994_mean_trend, \
    bhd_2006_2016_mean_trend, \
    bhd_2006_2009_mean_trend, \
    bhd_2012_2016_mean_trend
from heidelberg_intercomparison import heidelberg_1986_1991_mean_trend, \
    heidelberg_1991_1994_mean_trend, \
    heidelberg_2006_2016_mean_trend, \
    heidelberg_2006_2009_mean_trend, \
    heidelberg_2012_2016_mean_trend
from heidelberg_intercomparison import bhd_1986_1991_stdevs_trend, \
    bhd_1991_1994_stdevs_trend, \
    bhd_2006_2016_stdevs_trend, \
    bhd_2006_2009_stdevs_trend, \
    bhd_2012_2016_stdevs_trend
from heidelberg_intercomparison import heidelberg_1986_1991_stdevs_trend, \
    heidelberg_1991_1994_stdevs_trend, \
    heidelberg_2006_2016_stdevs_trend, \
    heidelberg_2006_2009_stdevs_trend, \
    heidelberg_2012_2016_stdevs_trend

# general plot parameters
colors = sns.color_palette("rocket", 3)
colors2 = sns.color_palette("mako", 3)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[1], s=size1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[1], s=size1)
plt.legend()
plt.title('All available data after 1980')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_1.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Smoothing of the whole dataset, just for visual analysis
"""
fig = plt.figure(3)
plt.scatter(xtot_bhd, ytot_bhd, label='Baring Head Record > 1980', color=colors[1], s=size1, alpha = 0.3, marker='o',)
plt.scatter(xtot_heid, ytot_heid, label='Heidelberg Cape Grim Record', color=colors2[1], s=size1, alpha = 0.3, marker='x',)
plt.plot(baringhead_xtot_smoothed, baringhead_ytot_smoothed, label='Baring Head Record > 1980', color=colors[1])
plt.plot(heidelberg_xtot_smoothed, heidelberg_ytot_smoothed, label='Heidelberg Cape Grim Record', color=colors2[1])
# plt.legend()
plt.title('Whole Dataset Smoothed with Monthly Means')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_2.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
After removal of data between 1994 and 2006
"""
fig = plt.figure(2)
plt.scatter(x_combined, y_combined, label='BHD', color=colors[1], s=size1, marker='o')
plt.scatter(xtot_heid, ytot_heid, label='CGO', color=colors2[1], s=size1, marker='x')
plt.legend()
plt.title('Rafter Measurements from 1994-2006 removed')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_3.png',
            dpi=300, bbox_inches="tight")
plt.close()

# """
# #Prepare multipanel plot for the two time periods
# """

fig = plt.figure(4, figsize=(10, 5))
gs = gridspec.GridSpec(4, 8)
gs.update(wspace=1, hspace=0.25)
# Generate first panel
# remember, the grid spec is rows, then columns
size2 = 20
xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
# plot data for left panel
plt.scatter(x1_bhd, y1_bhd, label='BHD', color=colors[1], s=size2, marker='o')
plt.scatter(x2_bhd, y2_bhd, color=colors[1], s=size2, marker= 'o')
plt.scatter(x1_heid, y1_heid, label='CGO', color=colors2[1], s=size2, marker='x')
plt.scatter(x2_heid, y2_heid, color=colors2[1], s=size2, marker='x')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.title('1986 - 1994')
plt.xlim([1987, 1994])
plt.ylim([120, 190])
plt.xlabel('Date')
plt.legend()

# Generate second panel
xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
plt.scatter(x3_bhd, y3_bhd, color=colors[1], s=size2, label='BHD', marker='o')
plt.scatter(x3_heid, y3_heid, color=colors2[1], s=size2, label='CGO', marker='x')
plt.title('2006 - 2016')
plt.xlim([2006, 2016])
plt.ylim([20, 65])
plt.xlabel('Date')
plt.legend()
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_4.png',
            dpi=300, bbox_inches="tight")

plt.close()
"""
How does it look after a simple curve smoothing (BEFORE doing Monte Carlo)
"""

fig = plt.figure(5, figsize=(10, 5))
gs = gridspec.GridSpec(4, 8)
gs.update(wspace=1, hspace=0.25)

# Generate first panel
# remember, the grid spec is rows, then columns

xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
# plot data for left panel
plt.scatter(x1_bhd, y1_bhd, label='BHD', color=colors[1], s=size2, alpha=0.3, marker='o')
plt.scatter(x2_bhd, y2_bhd, color=colors[1], s=size2, alpha=0.3, marker='o')
plt.plot(x_ccgcv_bhd1, y_ccgcv_bhd1, label='BHD - Smoothed Monthly Means', color=colors[1])
plt.plot(x_ccgcv_bhd2, y_ccgcv_bhd2, color=colors[1])

plt.scatter(x1_heid, y1_heid, label='CGO', color=colors2[1], s = size2, alpha = 0.3, marker='x')
plt.scatter(x2_heid, y2_heid, color=colors2[1], s = size2, alpha = 0.3, marker= 'x')
plt.plot(x_ccgcv_heid1, y_ccgcv_heid1, label='CGO - Smoothed Monthly Means', color=colors2[1])
plt.plot(x_ccgcv_heid2, y_ccgcv_heid2, color=colors2[1])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.title('1986 - 1994')
plt.xlim([1987, 1994])
plt.ylim([120, 190])
plt.xlabel('Date')
plt.legend(fontsize=7)

# Generate second panel
xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
plt.scatter(x3_bhd, y3_bhd, color=colors[1], s=size2, label='BHD', alpha=0.3, marker = 'o')
plt.scatter(x3_heid, y3_heid, color=colors2[1], s=size2, label='Heidelberg Cape Grim Record', alpha=0.3, marker='x')

plt.plot(x_ccgcv_bhd3, y_ccgcv_bhd3, color=colors[1], label='BHD - Smoothed Monthly Means')
plt.plot(x_ccgcv_heid3,  y_ccgcv_heid3, color=colors2[1], label='CGO - Smoothed Monthly Means')
plt.legend(fontsize=7)
plt.title('2006 - 2016')
plt.xlim([2006, 2016])
plt.ylim([20, 65])
plt.xlabel('Date')
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_5.png',
            dpi=300, bbox_inches="tight")

plt.close()


"""
Visual example of the randomization process
"""
print(x1_bhd)
print(y1_bhd)
print(heidelberg_1986_1991_randoms_smooth)
r1 = heidelberg_1986_1991_randoms_smooth.iloc[1]
r2 = heidelberg_1986_1991_randoms_smooth.iloc[2]
r3 = heidelberg_1986_1991_randoms_smooth.iloc[3]
r4 = heidelberg_1986_1991_randoms_smooth.iloc[4]
r5 = heidelberg_1986_1991_randoms_smooth.iloc[5]
r6 = heidelberg_1986_1991_randoms_smooth.iloc[6]

curve1 = heidelberg_1986_1991_smoothcurves_smooth.iloc[1]
curve2 = heidelberg_1986_1991_smoothcurves_smooth.iloc[2]
curve3 = heidelberg_1986_1991_smoothcurves_smooth.iloc[3]
curve4 = heidelberg_1986_1991_smoothcurves_smooth.iloc[4]
curve5 = heidelberg_1986_1991_smoothcurves_smooth.iloc[5]
curve6 = heidelberg_1986_1991_smoothcurves_smooth.iloc[6]
xs = summary['my_xs']

fig = plt.figure(6)
plt.errorbar(xtot_heid, ytot_heid, yerr=ztot_heid, fmt='x', color=colors[1], ecolor='black', elinewidth=1, capsize=2, label='CGO Data', alpha=0.3)
plt.scatter(x1_heid, r1, marker = '*', color = 'black', s = size2, label = 'Randomization Iteration 1')
plt.legend()
plt.title('Visualization of Randomization Process')
plt.xlim([1987, 1991])
plt.ylim([140, 190])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_6.png',
            dpi=300, bbox_inches="tight")
plt.legend()
plt.close
# #
fig = plt.figure(7)
plt.errorbar(xtot_heid, ytot_heid, yerr=ztot_heid, fmt='x', color=colors[1], ecolor='black', elinewidth=1, capsize=2, label='CGO Data', alpha=0.3)
plt.scatter(x1_heid, r1, marker = '*', color = 'black', s = size2, label = 'Randomization Iteration 1')
plt.plot(xs, curve1, color = 'black', label = 'Randomization Iteration 1 Smooth Curve Fit')

plt.legend()
plt.title('Visualization of Randomization Process')
plt.xlim([1987, 1991])
plt.ylim([140, 190])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_7.png',
            dpi=300, bbox_inches="tight")
plt.close()

fig = plt.figure(8)
plt.errorbar(xtot_heid, ytot_heid, yerr=ztot_heid, fmt='x', color=colors[1], ecolor='black', elinewidth=1, capsize=2, label='CGO Data', alpha=0.3)
plt.scatter(x1_heid, r1, marker = '*', color = 'black', s = size2, label = 'Randomization Iteration 1')
plt.plot(xs, curve1, color = 'black', label = 'Randomization Iteration 1 Smooth Curve Fit')
plt.scatter(x1_heid, r2, color = 'dodgerblue', s = size2, label='Randomization Iteration 2')
plt.plot(xs, curve2, color = 'dodgerblue', label = 'Randomization Iteration 2 Smooth Curve Fit')
plt.legend()
plt.title('Visualization of Randomization Process')
plt.xlim([1987, 1991])
plt.ylim([140, 190])
plt.xlabel('Date', fontsize=14)
plt.legend()
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_8.png',
            dpi=300, bbox_inches="tight")
plt.close()
#
colors3 = sns.color_palette("mako", 6)
fig = plt.figure(9)
plt.errorbar(xtot_heid, ytot_heid, yerr=ztot_heid, fmt='x', color=colors[1], ecolor='black', elinewidth=1, capsize=2, label='CGO Data', alpha=0.3)

plt.plot(xs, curve1, color = colors3[0], label = 'Randomization Iteration 1 Smooth Curve Fit', alpha = 0.3)
plt.plot(xs, curve2, color = colors3[1],  label = 'Randomization Iteration 2 Smooth Curve Fit', alpha = 0.3)
plt.plot(xs, curve3, color = colors3[2],  label = 'Randomization Iteration 2 Smooth Curve Fit', alpha = 0.3)
plt.plot(xs, curve4, color = colors3[3],  label = 'Randomization Iteration 2 Smooth Curve Fit', alpha = 0.3)
plt.plot(xs, curve5, color =colors3[4],  label = 'Randomization Iteration 2 Smooth Curve Fit', alpha = 0.3)
plt.plot(xs, heidelberg_1986_1991_mean_smooth, color = 'black', label = 'MEAN of smooth curve fits')
plt.legend()
plt.title('Visualization of Randomization Process')
plt.xlim([1987, 1991])
plt.ylim([140, 190])
plt.xlabel('Date', fontsize=14)
plt.legend()
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_9.png',
#             dpi=300, bbox_inches="tight")
plt.show()
plt.close()
#

"""
Smoothed vs Trended Curve for Part 1 and Part 2
"""
#
# fig = plt.figure(5, figsize=(10, 5))
# gs = gridspec.GridSpec(4, 8)
# gs.update(wspace=1, hspace=0.25)
#
# # Generate first panel
# # remember, the grid spec is rows, then columns
#
# xtr_subsplot = fig.add_subplot(gs[0:5, 0:5])
#
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_1986_1991['x'], bhd_1986_1991_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1991_1994['x'], bhd_1991_1994_mean_smooth, label='BHD 1991-1994 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1986_1991['x'], heidelberg_1986_1991_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors2[1])
# plt.plot(my_x_1991_1994['x'], heidelberg_1991_1994_mean_smooth, label='BHD 1991-1994 Mean Smoothed', color=colors2[1])
# plt.xlim([1987, 1994])
# plt.ylim([120, 190])
#
# plt.title('1987 - 1992')
# plt.legend(fontsize = 8)
# plt.xlabel('Date', fontsize=14)
# # Generate second panel
# xtr_subsplot = fig.add_subplot(gs[0:5, 5:10])
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_2006_2016['x'], bhd_2006_2016_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors[1])
# plt.plot(my_x_2006_2016['x'], heidelberg_2006_2016_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors2[1])
#
# plt.title('2006 - 2016')
# plt.xlim([2006, 2016])
# plt.ylim([20, 65])
# plt.legend(fontsize = 8)
# plt.xlabel('Date', fontsize=14)
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_10.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Same as above but the TRENDS this time versus the SMOOTHS
# """
#
# fig = plt.figure(5, figsize=(10, 5))
# gs = gridspec.GridSpec(4, 8)
# gs.update(wspace=1, hspace=0.25)
#
# # Generate first panel
# # remember, the grid spec is rows, then columns
#
# xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
#
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_1986_1991['x'], bhd_1986_1991_mean_trend, label='BHD 1986-1991 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1991_1994['x'], bhd_1991_1994_mean_trend, label='BHD 1991-1994 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1986_1991['x'], heidelberg_1986_1991_mean_trend, label='BHD 1986-1991 Mean Smoothed', color=colors2[1])
# plt.plot(my_x_1991_1994['x'], heidelberg_1991_1994_mean_trend, label='BHD 1991-1994 Mean Smoothed', color=colors2[1])
# plt.xlim([1987, 1994])
# plt.ylim([120, 190])
#
# plt.title('1987 - 1992')
# plt.legend(fontsize = 8)
# plt.xlabel('Date', fontsize=14)
# # Generate second panel
# xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_2006_2016['x'], bhd_2006_2016_mean_trend, label='BHD 1986-1991 Mean Trend', color=colors[1])
# plt.plot(my_x_2006_2016['x'], heidelberg_2006_2016_mean_trend, label='BHD 1986-1991 Mean Trend', color=colors2[1])
#
# plt.title('2006 - 2016')
# plt.xlim([2006, 2016])
# plt.ylim([20, 65])
# plt.legend(fontsize = 8)
# plt.xlabel('Date', fontsize=14)
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_11.png',
#             dpi=300, bbox_inches="tight")
# plt.close()

"""
Combination of the last 2 Figures
"""
# Figure template
#
# fig, axs = plt.subplots(2, 2)
# axs[0, 0].plot(x, y)
# axs[0, 0].set_title('Axis [0, 0]')
# axs[0, 1].plot(x, y, 'tab:orange')
# axs[0, 1].set_title('Axis [0, 1]')
# axs[1, 0].plot(x, -y, 'tab:green')
# axs[1, 0].set_title('Axis [1, 0]')
# axs[1, 1].plot(x, -y, 'tab:red')
# axs[1, 1].set_title('Axis [1, 1]')

# for ax in axs.flat:
#     ax.set(xlabel='x-label', ylabel='y-label')
#
# # Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#     ax.label_outer()

# fig, axs = plt.subplots(2, 2)
#
# axs[0, 0].scatter(x1_bhd, y1_bhd, marker='o', color=colors[1], s=size1, alpha = 0.3)
# axs[0, 0].scatter(x2_bhd, y2_bhd, marker='o', color=colors[1], s=size1, alpha = 0.3)
# axs[0, 0].scatter(x1_heid, y1_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# axs[0, 0].scatter(x2_heid, y2_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# axs[0, 0].plot(my_x_1986_1991['x'], bhd_1986_1991_mean_smooth, label='BHD Mean', color=colors[1])
# axs[0, 0].plot(my_x_1991_1994['x'], bhd_1991_1994_mean_smooth, color=colors[1])
# axs[0, 0].plot(my_x_1986_1991['x'], heidelberg_1986_1991_mean_smooth, label='CGO Mean', color=colors2[1])
# axs[0, 0].plot(my_x_1991_1994['x'], heidelberg_1991_1994_mean_smooth, color=colors2[1])
#
# axs[0, 1].scatter(x3_bhd, y3_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# axs[0, 1].scatter(x3_heid, y3_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# axs[0, 1].plot(my_x_2006_2016['x'], bhd_2006_2016_mean_smooth, color=colors[1])
# axs[0, 1].plot(my_x_2006_2016['x'], heidelberg_2006_2016_mean_smooth,  color=colors2[1])
#
# axs[1, 0].scatter(x1_bhd, y1_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# axs[1, 0].scatter(x2_bhd, y2_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# axs[1, 0].scatter(x1_heid, y1_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# axs[1, 0].scatter(x2_heid, y2_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# axs[1, 0].plot(my_x_1986_1991['x'], bhd_1986_1991_mean_trend,  color=colors[1])
# axs[1, 0].plot(my_x_1991_1994['x'], bhd_1991_1994_mean_trend, color=colors[1])
# axs[1, 0].plot(my_x_1986_1991['x'], heidelberg_1986_1991_mean_trend, color=colors2[1])
# axs[1, 0].plot(my_x_1991_1994['x'], heidelberg_1991_1994_mean_trend, color=colors2[1])
#
# axs[1, 1].scatter(x3_bhd, y3_bhd, marker='o',  color=colors[1], s=size1, alpha = 0.3)
# axs[1, 1].scatter(x3_heid, y3_heid, marker='x',  color=colors2[1], s=size1, alpha = 0.3)
# axs[1, 1].plot(my_x_2006_2016['x'], bhd_2006_2016_mean_trend, color=colors[1])
# axs[1, 1].plot(my_x_2006_2016['x'], heidelberg_2006_2016_mean_trend, color=colors2[1])
#
# axs[0, 0].set_title('1987 - 1994, CCGCRV Smoothed')
# axs[0, 1].set_title('2006 - 2016, CCGCRV Smoothed')
# axs[1, 0].set_title('1987 - 1994, CCGCRV Trend')
# axs[1, 1].set_title('2006 - 2016, CCGCRV Trend')
# axs[0, 0].legend()
# for ax in axs.flat:
#     ax.set(xlabel='Date', ylabel='\u0394$^1$$^4$CO$_2$ (\u2030)')
#
# # Hide x labels and tick labels for top plots and y ticks for right plots.
# for ax in axs.flat:
#     ax.label_outer()
#
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_12.png')
# plt.close()
#















#
#
#
#
#
# fig = plt.figure(5, figsize=(10, 5))
# gs = gridspec.GridSpec(4, 8)
# gs.update(wspace=1, hspace=0.25)
#
# # Generate first panel
# # remember, the grid spec is rows, then columns
#
# xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_1986_1991['x'], bhd_1986_1991_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1991_1994['x'], bhd_1991_1994_mean_smooth, label='BHD 1991-1994 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1986_1991['x'], heidelberg_1986_1991_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors2[1])
# plt.plot(my_x_1991_1994['x'], heidelberg_1991_1994_mean_smooth, label='BHD 1991-1994 Mean Smoothed', color=colors2[1])
# plt.xlim([1987, 1994])
# plt.ylim([120, 190])
# plt.title('1987 - 1994')
# plt.legend(fontsize = 8)
#
# # Generate second panel
# xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_2006_2016['x'], bhd_2006_2016_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors[1])
# plt.plot(my_x_2006_2016['x'], heidelberg_2006_2016_mean_smooth, label='BHD 1986-1991 Mean Smoothed', color=colors2[1])
# plt.title('2006 - 2016')
# plt.xlim([2006, 2016])
# plt.ylim([20, 65])
# plt.legend(fontsize = 8)
#
# # Generate 3rd panel
# xtr_subsplot = fig.add_subplot(gs[4:8, 0:4])
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_1986_1991['x'], bhd_1986_1991_mean_trend, label='BHD 1986-1991 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1991_1994['x'], bhd_1991_1994_mean_trend, label='BHD 1991-1994 Mean Smoothed', color=colors[1])
# plt.plot(my_x_1986_1991['x'], heidelberg_1986_1991_mean_trend, label='BHD 1986-1991 Mean Smoothed', color=colors2[1])
# plt.plot(my_x_1991_1994['x'], heidelberg_1991_1994_mean_trend, label='BHD 1991-1994 Mean Smoothed', color=colors2[1])
# plt.xlim([1987, 1994])
# plt.ylim([120, 190])
# plt.title('1987 - 1994')
# plt.legend(fontsize = 8)
# plt.xlabel('Date', fontsize=14)
#
# # Generate 4th panel
# xtr_subsplot = fig.add_subplot(gs[4:8, 4:8])
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='BHD', color=colors[1], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, marker='x', label='CGO', color=colors2[1], s=size1, alpha = 0.3)
# plt.plot(my_x_2006_2016['x'], bhd_2006_2016_mean_trend, label='BHD 1986-1991 Mean Trend', color=colors[1])
# plt.plot(my_x_2006_2016['x'], heidelberg_2006_2016_mean_trend, label='BHD 1986-1991 Mean Trend', color=colors2[1])
#
# plt.title('2006 - 2016')
# plt.xlim([2006, 2016])
# plt.ylim([20, 65])
# plt.legend(fontsize = 8)
# plt.xlabel('Date', fontsize=14)
# # plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
# #             'radiocarbon_intercomparison/plots/cleanedFigs_11.png',
# #             dpi=300, bbox_inches="tight")
# # plt.close()
#
# plt.show()