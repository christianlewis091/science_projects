import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import pandas as pd
import numpy as np
from heidelberg_intercomparison import xtot_bhd, ytot_bhd, ztot_bhd  # full datasets from the file
from heidelberg_intercomparison import xtot_heid, ytot_heid  # full datasets from the file
from heidelberg_intercomparison import x1_bhd, x2_bhd, x3_bhd  # bhds data broken up into different chunks
from heidelberg_intercomparison import y1_bhd, y2_bhd, y3_bhd  # bhds data broken up into different chunks
from heidelberg_intercomparison import x1_heid, x2_heid, x3_heid  # heid data broken up into different chunks
from heidelberg_intercomparison import y1_heid, y2_heid, y3_heid  # heid data broken up into different chunks
from heidelberg_intercomparison import x_combined, y_combined
from heidelberg_intercomparison import x_ccgcv_bhd1, y_ccgcv_bhd1
from heidelberg_intercomparison import x_ccgcv_bhd2, y_ccgcv_bhd2
from heidelberg_intercomparison import x_ccgcv_bhd3, y_ccgcv_bhd3
from heidelberg_intercomparison import x_ccgcv_heid1, y_ccgcv_heid1
from heidelberg_intercomparison import x_ccgcv_heid2, y_ccgcv_heid2
from heidelberg_intercomparison import x_ccgcv_heid3, y_ccgcv_heid3
from heidelberg_intercomparison import baringhead_xtot_smoothed, baringhead_ytot_smoothed, heidelberg_xtot_smoothed, heidelberg_ytot_smoothed
from heidelberg_intercomparison import monte_it1, monte_it2, monte_it3, monte_it4, monte_it5, my_x_1986_1991_arr, means
from heidelberg_intercomparison import randos1, randos2, randos3, randos4, randos5
from heidelberg_intercomparison import bhd_1986_1991_mean, bhd_1991_1994_mean, bhd_2006_2016_mean
from heidelberg_intercomparison import heidelberg_1986_1991_mean, heidelberg_1991_1994_mean, heidelberg_2006_2016_mean
from heidelberg_intercomparison import my_x_1986_1991, my_x_1991_1994, my_x_2006_2016, my_x_2006_2009, my_x_2012_2016, \
    bhd_2006_2009_mean, heidelberg_2006_2009_mean, bhd_2012_2016_mean, heidelberg_2012_2016_mean



import matplotlib.gridspec as gridspec
# TODO finish importing variables from the other sheet. organize plots. put them into power point.
# TODO do two year averages?
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

# """
# Figure 1. All the data together
# """
# # matplotlib.pyplot.scatter(x, y, s=None, c=None, marker=None, cmap=None, norm=None, vmin=None, vmax=None, alpha=None, linewidths=None, *, edgecolors=None, plotnonfinite=False, data=None, **kwargs)[source]
# fig = plt.figure(1)
# plt.scatter(xtot_bhd, ytot_bhd, label='Baring Head Record > 1980', color=colors[3], s=size1)
# plt.scatter(xtot_heid, ytot_heid, label='Heidelberg Cape Grim Record', color=colors2[3], s=size1)
# plt.legend()
# plt.title('All available data after 1980')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_1.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
# """
# After removal of data between 1994 and 2006
# """
# fig = plt.figure(2)
# plt.scatter(x_combined, y_combined, label='Baring Head Record > 1980', color=colors[3], s=size1)
# plt.scatter(xtot_heid, ytot_heid, label='Heidelberg Cape Grim Record', color=colors2[3], s=size1)
# plt.legend()
# plt.title('Rafter Measurements from 1994-2006 removed')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_2.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# Smoothing of the whole dataset, just for visual analysis
# """
# fig = plt.figure(3)
# plt.scatter(xtot_bhd, ytot_bhd, label='Baring Head Record > 1980', color=colors[3], s=size1, alpha = 0.3)
# plt.scatter(xtot_heid, ytot_heid, label='Heidelberg Cape Grim Record', color=colors2[3], s=size1, alpha = 0.3)
# plt.plot(baringhead_xtot_smoothed, baringhead_ytot_smoothed, label='Baring Head Record > 1980', color=colors[3])
# plt.plot(heidelberg_xtot_smoothed, heidelberg_ytot_smoothed, label='Heidelberg Cape Grim Record', color=colors2[3])
# # plt.legend()
# plt.title('Rafter Measurements from 1994-2006 removed')
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_2.1.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
# """
# #Prepare multipanel plot for the two time periods
# """
#
# fig = plt.figure(4, figsize=(10, 5))
# gs = gridspec.GridSpec(4, 8)
# gs.update(wspace=1, hspace=0.25)
#
# # Generate first panel
# # remember, the grid spec is rows, then columns
#
# xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
# # plot data for left panel
# plt.scatter(x1_bhd, y1_bhd, label='Baring Head Record', color=colors[3], s=size1)
# plt.scatter(x2_bhd, y2_bhd, color=colors[3], s=size1)
# plt.scatter(x1_heid, y1_heid, label='Heidelberg Cape Grim Record', color=colors2[3], s=size1)
# plt.scatter(x2_heid, y2_heid, color=colors2[3], s=size1)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.title('1986 - 1994')
# plt.xlim([1987, 1994])
# plt.ylim([0, 200])
# plt.xlabel('Date')
#
# # Generate second panel
# xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
# plt.scatter(x3_bhd, y3_bhd, color=colors[3], s=size1, label='Baring Head Record')
# plt.scatter(x3_heid, y3_heid, color=colors2[3], s=size1, label='Heidelberg Cape Grim Record')
# plt.title('2006 - 2016')
# plt.xlim([2006, 2016])
# plt.ylim([0, 200])
# plt.xlabel('Date')
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_3.png',
#             dpi=300, bbox_inches="tight")
# #
#
# """
# How does it look after a simple curve smoothing (BEFORE doing Monte Carlo)
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
# # plot data for left panel
# plt.scatter(x1_bhd, y1_bhd, label='Baring Head Record', color=colors[3], s=size1, alpha=0.3)
# plt.scatter(x2_bhd, y2_bhd, color=colors[3], s=size1, alpha=0.3)
# plt.plot(x_ccgcv_bhd1, y_ccgcv_bhd1, label='Baring Head Record - Smoothed Monthly Means', color=colors[3])
# plt.plot(x_ccgcv_bhd2, y_ccgcv_bhd2, color=colors[3])
#
# plt.scatter(x1_heid, y1_heid, label='Heidelberg Cape Grim Record', color=colors2[3], s = size1, alpha = 0.3)
# plt.scatter(x2_heid, y2_heid, color=colors2[3], s = size1, alpha = 0.3)
# plt.plot(x_ccgcv_heid1, y_ccgcv_heid1, label='Heidelberg Cape Grim Record - Smoothed Monthly Means', color=colors2[3])
# plt.plot(x_ccgcv_heid2, y_ccgcv_heid2, color=colors2[3])
#
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.title('1986 - 1994')
# plt.xlim([1987, 1994])
# plt.ylim([0, 200])
# plt.xlabel('Date')
# plt.legend(fontsize=7)
#
# # Generate second panel
# xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
# plt.scatter(x3_bhd, y3_bhd, color=colors[3], s=size1, label='Baring Head Record', alpha=0.3)
# plt.scatter(x3_heid, y3_heid, color=colors2[3], s=size1, label='Heidelberg Cape Grim Record', alpha=0.3)
#
# plt.plot(x_ccgcv_bhd3, y_ccgcv_bhd3, color=colors[3], label='Baring Head Record - Smoothed Monthly Means')
# plt.plot(x_ccgcv_heid3,  y_ccgcv_heid3, color=colors2[3], label='Heidelberg Cape Grim Record - Smoothed Monthly Means')
# plt.legend(fontsize=7)
# plt.title('2006 - 2016')
# plt.xlim([2006, 2016])
# plt.ylim([0, 200])
# plt.xlabel('Date')
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_4_667daycut.png',
#             dpi=300, bbox_inches="tight")
# #
# #
# """
# Visual example of the randomization process
# """
# fig = plt.figure(6)
# plt.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt = 'o',color=colors[3], ecolor='black', elinewidth = 1, capsize=2, label='Original Baring Data', alpha = 0.3)
# # plt.scatter(x1_bhd, randos5, color='dodgerblue', s=25, label='Randomization 1', edgecolor='black', alpha = 0.3)
# plt.plot(my_x_1986_1991_arr, monte_it5, color='dodgerblue', alpha = 0.3)
# # plt.scatter(x1_bhd, randos4, color=colors[0], s=25, label='Randomization 1', edgecolor='black')
# plt.plot(my_x_1986_1991_arr, monte_it4, color=colors[4], alpha = 0.3)
# plt.plot(my_x_1986_1991_arr, monte_it3, color=colors[2], alpha = 0.3)
# plt.plot(my_x_1986_1991_arr, monte_it2, color=colors[1], alpha = 0.3)
# plt.plot(my_x_1986_1991_arr, monte_it1, color=colors[0], alpha = 0.3)
# plt.plot(my_x_1986_1991_arr, monte_it1, color=colors[0], alpha = 0.3)
#
# plt.plot(my_x_1986_1991_arr, means, color='black', label = 'Mean of CCGCRV Smoothed Data')
# plt.legend()
# plt.title('Visualization of Randomization Process')
# plt.xlim([1987, 1992])
# plt.ylim([140, 190])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_monte_explain6.png',
#             dpi=300, bbox_inches="tight")
# plt.legend()
print(my_x_1991_1994)
print(bhd_1991_1994_mean)

"""
Plots after the Monte Carlo and Smoothing: 
"""

fig = plt.figure(5, figsize=(10, 5))
gs = gridspec.GridSpec(4, 8)
gs.update(wspace=1, hspace=0.25)

# Generate first panel
# remember, the grid spec is rows, then columns

xtr_subsplot = fig.add_subplot(gs[0:4, 0:4])
# plot data for left panel
plt.scatter(x1_bhd, y1_bhd, label='Baring Head Record', color=colors[3], s=size1, alpha=0.3)
plt.scatter(x2_bhd, y2_bhd, color=colors[3], s=size1, alpha=0.3)
plt.plot(my_x_1986_1991, bhd_1986_1991_mean, color=colors[3], label='BHD Post-Monte Carlo Analysis Mean')
plt.plot(my_x_1991_1994, bhd_1991_1994_mean, color=colors[3])

plt.scatter(x1_heid, y1_heid, label='Heidelberg Cape Grim Record', color=colors2[3], s = size1, alpha = 0.3)
plt.scatter(x2_heid, y2_heid, color=colors2[3], s = size1, alpha = 0.3)
plt.plot(my_x_1986_1991, heidelberg_1986_1991_mean, color=colors2[3], label='CGO Post-Monte Carlo Analysis Mean')
plt.plot(my_x_1991_1994, heidelberg_1991_1994_mean, color=colors2[3])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.title('1986 - 1994')
plt.xlim([1987, 1994])
plt.ylim([120, 190])
plt.xlabel('Date')
plt.legend(fontsize=7)

# Generate second panel
xtr_subsplot = fig.add_subplot(gs[0:4, 4:8])
plt.scatter(x3_bhd, y3_bhd, color=colors[3], s=size1, label='Baring Head Record', alpha=0.3)
plt.scatter(x3_heid, y3_heid, color=colors2[3], s=size1, label='Heidelberg Cape Grim Record', alpha=0.3)
plt.plot(my_x_2006_2009, bhd_2006_2009_mean, color=colors[3], label='BHD Post-Monte Carlo Analysis Mean')
plt.plot(my_x_2006_2009, heidelberg_2006_2009_mean, color=colors2[3], label='Heidelberg Post-Monte Carlo Analysis Mean')
plt.plot(my_x_2012_2016, bhd_2012_2016_mean, color=colors[3], label='BHD Post-Monte Carlo Analysis Mean')
plt.plot(my_x_2012_2016, heidelberg_2012_2016_mean, color=colors2[3], label='Heidelberg Post-Monte Carlo Analysis Mean')
plt.legend(fontsize=7)
plt.title('2006 - 2016')
plt.xlim([2006, 2016])
plt.ylim([20, 65])
plt.xlabel('Date')
plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
            'radiocarbon_intercomparison/plots/cleanedFigs_8_trendvalue.png',
            dpi=300, bbox_inches="tight")












































#
# """
# Visaul example of monte carlo smoothing
# """
#
# fig = plt.figure(6)
# plt.scatter(xtot_bhd, ytot_bhd, label='Baring Head Record > 1980', color=colors[3], s=size1, alpha = 0.3)
# plt.plot(my_x_1986_1991_arr, monte_it2, color=colors[1])
# plt.plot(my_x_1986_1991_arr, monte_it3, color=colors[2])
# plt.plot(my_x_1986_1991_arr, monte_it4, color=colors[4])
# plt.plot(my_x_1986_1991_arr, monte_it5, color=colors[5])
# plt.title('Visualization of Monte Carlo Process')
# plt.xlim([1987, 1992])
# plt.ylim([140, 190])
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison/plots/cleanedFigs_6.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
