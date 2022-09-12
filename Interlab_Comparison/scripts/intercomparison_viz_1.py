# <editor-fold desc="Import Statements">
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from Pre_Processing_UniMagallanes import combine_Magallanes
from intercomparison_math_1_SUPERCEDED import flaskvn
import seaborn as sns
from intercomparison_math_2_scipy import ansto, rrl, sio_nwt3, sio_nwt4, rrl_nwt3, rrl_nwt4, y1, y1_average, y1_1sigma, y2, y2_average, y2_1sigma, y3, y3_average, y3_1sigma, y4, y4_average, y4_1sigma
from intercomparison_math_2_scipy import naoh1, flask1, naoh_means1, flask_means1, naoh_means2, flask_means2, fake_x1, fake_x2, naoh2, flask2
from colors_set import *
import pandas as pd
size1 = 5


"""

SIO/LLNL V Rafter Plot



"""
fig = plt.figure(4, figsize=(16.1, 10))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=.35, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.errorbar(rrl_nwt3['Decimal_date'], rrl_nwt3['D14C'], yerr=rrl_nwt3['D14C_err'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='RRL NWT3')
plt.axhline(y=y3_average, color='black', linestyle='-')
plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=farbe_bhd, alpha=0.3)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030) [NWT3]', fontsize=14)  # label the y axis
# plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis
plt.title('RRL')
# plt.legend()

plt.ylim(30,55)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(rrl_nwt4['Decimal_date'], y4, yerr=rrl_nwt4['D14C_err'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='RRL NWT4')
plt.axhline(y=y4_average, color='black', linestyle='-')
plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=farbe_bhd, alpha=0.3)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030) [NWT4]', fontsize=14)  # label the y axis
# plt.legend()
plt.ylim(-40,-24)
plt.xlabel('Date', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.ylim(30,55)
# plt.axhline(y=y3_average, color='black', linestyle='-')
# plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=colors2[4], alpha=0.3)
plt.errorbar(sio_nwt3['Decimal_date'], y1, yerr=sio_nwt3['D14C_err'], fmt='D', color=farbe_sio, ecolor=farbe_sio, elinewidth=1, capsize=2, label='LLNL NWT3')
plt.axhline(y=y1_average, color='black', linestyle='solid')
plt.axhspan((y1_average-y1_1sigma), (y1_average+y1_1sigma), facecolor=farbe_sio, alpha=0.3)
plt.title('SIO/LLNL')
# plt.xlabel('Measurement #', fontsize=14)  # label the y axis
# plt.legend()


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.ylim(-40,-24)
# plt.axhline(y=y4_average, color='black', linestyle='-')
# plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=colors2[5], alpha=0.3)
plt.errorbar(sio_nwt4['Decimal_date'], y2, yerr=sio_nwt3['D14C_err'], fmt='D', color=farbe_sio, ecolor=farbe_sio, elinewidth=1, capsize=2, label='LLNL NWT4')
plt.axhline(y=y2_average, color='black', linestyle='solid')
plt.axhspan((y2_average-y2_1sigma), (y2_average+y2_1sigma), facecolor=farbe_sio, alpha=0.3)
plt.xlabel('Measurement #', fontsize=14)  # label the y axis
# plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/SIOLLNLvRRL.png',
            dpi=300, bbox_inches="tight")
plt.close()

from intercomparison_math_2_scipy import y1_fm, y1_average_fm, y1_1sigma_fm, y2_fm, y2_average_fm, y2_1sigma_fm, y3_fm, y3_average_fm, y3_1sigma_fm, y4_fm, y4_average_fm, y4_1sigma_fm

fig = plt.figure(4, figsize=(16.1, 10))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=.35, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.title('RRL')
plt.errorbar(rrl_nwt3['Decimal_date'], rrl_nwt3['FM'], yerr=rrl_nwt3['FM_err'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='RRL NWT3')
plt.axhline(y=y3_average_fm, color='black', linestyle='-')
plt.axhspan((y3_average_fm-y3_1sigma_fm), (y3_average_fm+y3_1sigma_fm), facecolor=farbe_bhd, alpha=0.3)
plt.ylabel('FM [NWT3]', fontsize=14)  # label the y axis
# plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis
# plt.legend()
plt.ylim(1.035,1.065)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(rrl_nwt4['Decimal_date'], y4_fm, yerr=rrl_nwt4['FM_err'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='RRL NWT4')
plt.axhline(y=y4_average_fm, color='black', linestyle='-')
plt.axhspan((y4_average_fm-y4_1sigma_fm), (y4_average_fm+y4_1sigma_fm), facecolor=farbe_bhd, alpha=0.3)
plt.ylabel('FM [NWT4]', fontsize=14)  # label the y axis
plt.legend()
plt.ylim(0.965, 0.985)
plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# plt.ylim(30,55)
# plt.axhline(y=y3_average, color='black', linestyle='-')
# plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=colors2[4], alpha=0.3)
plt.title('SIO/LLNL')
plt.errorbar(sio_nwt3['Decimal_date'], y1_fm, yerr=sio_nwt3['FM_err'], fmt='D', color=farbe_sio, ecolor=farbe_sio, elinewidth=1, capsize=2, label='LLNL NWT3')
plt.axhline(y=y1_average_fm, color='black', linestyle='solid')
plt.axhspan((y1_average_fm-y1_1sigma_fm), (y1_average_fm+y1_1sigma_fm), facecolor=farbe_sio, alpha=0.3)
# plt.xlabel('Measurement #', fontsize=14)  # label the y axis
# plt.legend()
plt.ylim(1.035,1.065)


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
# plt.ylim(-40,-24)
# plt.axhline(y=y4_average, color='black', linestyle='-')
# plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=colors2[5], alpha=0.3)
plt.errorbar(sio_nwt4['Decimal_date'], y2_fm, yerr=sio_nwt3['FM_err'], fmt='D', color=farbe_sio, ecolor=farbe_sio, elinewidth=1, capsize=2, label='LLNL NWT4')
plt.axhline(y=y2_average_fm, color='black', linestyle='solid')
plt.axhspan((y2_average_fm-y2_1sigma_fm), (y2_average_fm+y2_1sigma_fm), facecolor=farbe_sio, alpha=0.3)
plt.xlabel('Measurement #', fontsize=14)  # label the y axis
# plt.legend()
plt.ylim(0.965, 0.985)

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/SIOLLNLvRRL_FM.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="ANSTO v Rafter">
"""


ANSTO v RRL Plot


"""

fig = plt.figure(1, figsize=(10,5))
gs = gridspec.GridSpec(1, 2)
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.errorbar(rrl['Decimal_date'], rrl['D14C'], label='RRL', yerr=rrl['D14C_err'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2)
plt.errorbar(ansto['Decimal_date'], ansto['D14C'], label='ANSTO', yerr=ansto['D14C_err'], fmt='^', color=farbe_ansto, ecolor=farbe_ansto, elinewidth=1, capsize=2)
plt.legend()
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plt.errorbar(combine_Magallanes['Decimal_date'], combine_Magallanes['D14C_x'], label='RRL', yerr=combine_Magallanes['D14C_err_x'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2)
plt.errorbar(combine_Magallanes['Decimal_date'], combine_Magallanes['D14C_y'], label='Uni Magallanes', yerr=combine_Magallanes['D14C_err_y'], fmt='s', color=farbe_maga, ecolor=farbe_maga, elinewidth=1, capsize=2)
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/Magallanes_Ansto_comb.png',
            dpi=300, bbox_inches="tight")
plt.close()


fig = plt.figure(1, figsize=(5,5))
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.errorbar(rrl['Decimal_date'], rrl['D14C'], label='RRL', yerr=rrl['D14C_err'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2)
plt.errorbar(ansto['Decimal_date'], ansto['D14C'], label='ANSTO', yerr=ansto['D14C_err'], fmt='^', color=farbe_ansto, ecolor=farbe_ansto, elinewidth=1, capsize=2)
# plt.legend()
# xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
# plt.errorbar(combine_Magallanes['Decimal_date'], combine_Magallanes['D14C_x'], label='RRL', yerr=combine_Magallanes['D14C_err_x'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2)
# plt.errorbar(combine_Magallanes['Decimal_date'], combine_Magallanes['D14C_y'], label='Uni Magallanes', yerr=combine_Magallanes['D14C_err_y'], fmt='s', color=farbe_maga, ecolor=farbe_maga, elinewidth=1, capsize=2)
# plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/ANSTOvRRL.png',
            dpi=300, bbox_inches="tight")
plt.close()


# </editor-fold>

from heidelberg_intercomparison_wD14C import xtot_bhd, ytot_bhd, ztot_bhd, xtot_heid, ytot_heid, ztot_heid, x1_bhd, data1, data2, data3, my_x_1986_1991, curve1, curve2, curve3, bhd_1986_1991_mean_smooth, bhd_1986_1991_mean_trend, heidelberg_1986_1991_mean_smooth, heidelberg_1986_1991_mean_trend
from heidelberg_intercomparison_wD14C import my_x_1986_1991, my_x_1991_1994, my_x_2006_2016, my_x_2006_2009, my_x_2012_2016
from heidelberg_intercomparison_wD14C import bhd_1991_1994_mean_trend, bhd_1991_1994_mean_smooth
from heidelberg_intercomparison_wD14C import heidelberg_1991_1994_mean_trend, heidelberg_1991_1994_mean_smooth
from heidelberg_intercomparison_wD14C import bhd_2006_2009_mean_trend, bhd_2006_2009_mean_smooth
from heidelberg_intercomparison_wD14C import heidelberg_2006_2009_mean_trend, heidelberg_2006_2009_mean_smooth
from heidelberg_intercomparison_wD14C import bhd_2012_2016_mean_trend, bhd_2012_2016_mean_smooth
from heidelberg_intercomparison_wD14C import heidelberg_2012_2016_mean_trend, heidelberg_2012_2016_mean_smooth
from heidelberg_intercomparison_wD14C import means, my_x_2006_2009_trimmed, my_x_2012_2016_trimmed

# <editor-fold desc="Heidelberg v Rafter: Broad Overview of all data">
"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Radiocarbon Lab' + '\n' ' - Baring Head, New Zealand [BHD]', color=farbe_bhd, s=size1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg University' + '\n' ' - Cape Grim, Tasmania [CGO]', color=farbe_heid, s=size1)
plt.legend()
plt.title('Available Data for Uni Heidelberg and Rafter Radiocarbon Lab Intercomparison')
plt.xlim([1985, 2020])
plt.ylim([0, 220])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/DEV_FirstDraft_figure1.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Figure 3. A breakdown of the 4 periods of time that we test for the intercomparison,
and how the smooth and trend data compare for each.
"""
size2 = 15
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Radiocarbon Lab' + '\n' ' - Baring Head, New Zealand [BHD]', color=farbe_bhd, s=size1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg University' + '\n' ' - Cape Grim, Tasmania [CGO]', color=farbe_heid, s=size1)
plt.axvspan(1987, 1991, facecolor='black', alpha=0.1)
plt.axvspan(1991, 1994, facecolor='black', alpha=0.1)
plt.axvspan(2006, 2009, facecolor='black', alpha=0.1)
plt.axvspan(2012, 2016, facecolor='black', alpha=0.1)

plt.axvline(x = 1987, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 1991, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 1994, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2006, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2009, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2012, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2016, color = 'black', alpha = 0.2, linestyle = 'solid')
# plt.text(1988, 0, "1", fontsize=8)
# plt.text(1991, 0, "2", fontsize=8)
# plt.text(2007, 0, "3", fontsize=8)
# plt.text(2011, 0, "4", fontsize=8)
# plt.text(1980, 0, "Time Interval:", fontsize=8)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.arrow(1994, 50, -6, 0,  fc="k", ec="k",head_width=0.05, head_length=0.1 )
plt.xlabel('Date', fontsize=14)  # label the y axis
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/new_test.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: Vizualization of Monte Carlo Smoothing Process">
# """
# Figure 2. Visual Example of the randomization and smoothing process.
# """
# fig = plt.figure(2)
#
# plt.title('Visualization of Monte Carlo and CCGCRV Process: 1987-1991 BHD')
# plt.errorbar(xtot_bhd, ytot_bhd, label='BHD Data' , yerr=ztot_bhd, fmt='o', color=viz1, ecolor=viz1, elinewidth=1, capsize=2)
# plt.scatter(x1_bhd, data1, color = c1, label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x')
# plt.scatter(x1_bhd, data2, color = c2,  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^')
# plt.scatter(x1_bhd, data3, color = c3,  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's')
# plt.plot(my_x_1986_1991, curve1, color = c1, alpha = 0.35, linestyle = 'dotted')
# plt.plot(my_x_1986_1991, curve2, color = c2, alpha = 0.35, linestyle = 'dashed')
# plt.plot(my_x_1986_1991, curve3, color = c3, alpha = 0.35, linestyle = 'dashdot')
# plt.plot(my_x_1986_1991, bhd_1986_1991_mean_smooth, color = smoothviz,  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'dashed')
# plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = trendviz,  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
# plt.xlim([1989, 1990])
# plt.ylim([140, 160])
# plt.legend()
# plt.xlabel('Date', fontsize=14)
# plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/DEV_FirstDraft_figure2.png',
#             dpi=300, bbox_inches="tight")
# # plt.show()
# plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: Monte Carlo Vizualization, second edition">
"""
Figure S1. Visual Example of the randomization and smoothing process, broken into 4 panels.
"""
fig = plt.figure(4, figsize=(10,3))
gs = gridspec.GridSpec(1, 8)
gs.update(wspace=1, hspace=0.1)
# Generate first panel
# remember, the grid spec is rows, then columns
size2 = 15
xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
# plot data for left panel
plt.text(1990.75, 167.5, "A", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='BHD Data' , yerr=ztot_bhd, fmt='none', color=viz1, ecolor=viz1, elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=viz1, s=size2)
# plt.scatter(x1_bhd, data1, color = c1, label = 'Monte Carlo Iteration 1', alpha = beta, marker = 'x', s = size2)
# plt.scatter(x1_bhd, data2, color = c2,  label = 'Monte Carlo Iteration 2', alpha = beta, marker = '^', s = size2)
# plt.scatter(x1_bhd, data3, color = c3,  label = 'Monte Carlo Iteration 3', alpha = beta, marker = 's', s = size2)
# plt.plot(my_x_1986_1991, curve1, color = c1, alpha = 0.35, linestyle = 'dotted')
# plt.plot(my_x_1986_1991, curve2, color = c2, alpha = 0.35, linestyle = 'dashed')
# plt.plot(my_x_1986_1991, curve3, color = c3, alpha = 0.35, linestyle = 'dashdot')
# plt.plot(my_x_1986_1991, means, color = smoothviz,  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = trendviz,  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
# plt.title('Step 0: Data', fontdict=None, loc='center', pad=None)
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])
xtr_subsplot.set_yticklabels([])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.text(1990.75, 167.5, "B", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='BHD Data' , yerr=ztot_bhd, fmt='none', color=viz1, ecolor=viz1, elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=viz1, s=size2)
plt.scatter(x1_bhd, data1, color = c1, label = 'Monte Carlo Iteration 1', alpha =beta, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = c2,  label = 'Monte Carlo Iteration 2', alpha = beta, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = c3,  label = 'Monte Carlo Iteration 3', alpha = beta, marker = 's', s = size2)
# plt.title('Step 1: Randomize Data within 1-sigma normal dist.',  fontdict=None, loc='center', pad=None)
# plt.plot(my_x_1986_1991, curve1, color = c1, alpha = beta, linestyle = 'dotted')
# plt.plot(my_x_1986_1991, curve2, color = c2, alpha = beta, linestyle = 'dashed')
# plt.plot(my_x_1986_1991, curve3, color = c3, alpha = beta, linestyle = 'dashdot')
# plt.plot(my_x_1986_1991, means, color = smoothviz,  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = trendviz,  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])
xtr_subsplot.set_yticklabels([])

xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.text(1990.75, 167.5, "C", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='BHD Data' , yerr=ztot_bhd, fmt='none', color=viz1, ecolor=viz1, elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=viz1, s=size2)
plt.scatter(x1_bhd, data1, color = c1, label = 'Monte Carlo Iteration 1', alpha = beta, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = c2,  label = 'Monte Carlo Iteration 2', alpha = beta, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = c3,  label = 'Monte Carlo Iteration 3', alpha = beta, marker = 's', s = size2)
plt.plot(my_x_1986_1991, curve1, color = c1_line, alpha = beta, linestyle = 'dotted')
plt.plot(my_x_1986_1991, curve2, color = c2_line, alpha = beta, linestyle = 'dashed')
plt.plot(my_x_1986_1991, curve3, color = c3_line, alpha = beta, linestyle = 'dashdot')
# plt.title('Step 2: Apply CCGCRV algoritm to randomized data',  fontdict=None, loc='center', pad=None)
# plt.plot(my_x_1986_1991, means, color = smoothviz,  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'dashed')
# plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = trendviz,  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])
xtr_subsplot.set_yticklabels([])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.text(1990.75, 167.5, "D", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='BHD Data' , yerr=ztot_bhd, fmt='none', color=viz1, ecolor=viz1, elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=viz1, s=size2)
plt.scatter(x1_bhd, data1, color = c1, label = 'Monte Carlo Iteration 1', alpha = beta, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = c2,  label = 'Monte Carlo Iteration 2', alpha = beta, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = c3,  label = 'Monte Carlo Iteration 3', alpha = beta, marker = 's', s = size2)
plt.plot(my_x_1986_1991, curve1, color = c1_line, alpha = beta, linestyle = 'dotted')
plt.plot(my_x_1986_1991, curve2, color = c2_line, alpha = beta, linestyle = 'dashed')
plt.plot(my_x_1986_1991, curve3, color = c3_line, alpha = beta, linestyle = 'dashdot')
plt.plot(my_x_1986_1991, means, color = smoothviz,  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'dashed')
# plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = trendviz,  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'dashdot')
# plt.title('Step 3: Find mean of CCGCRV curves',  fontdict=None, loc='center', pad=None)
plt.xlim([xmin, xmax])
plt.ylim([ymin, ymax])
# plt.legend(loc=(1.04,0.5))
# plt.legend(loc=(-1,-1))
xtr_subsplot.set_yticklabels([])

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/DEV_FirstDraft_figureS1.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>


# <editor-fold desc="Heidelberg v Rafter: 4 - Time Interval, Smooth Curve Fits">
fig = plt.figure(4, figsize=(10,5))
gs = gridspec.GridSpec(4, 8)
gs.update(wspace=1.2, hspace=0.5)
# Generate first panel

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# plot data for left panel
plt.title('CCGCRV Smooth')
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=farbe_bhd)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=farbe_heid, linestyle = 'dashed')
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=farbe_bhd)
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=farbe_heid, linestyle = 'dashed')
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=farbe_bhd)
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=farbe_heid, linestyle = 'dashed')
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[0:2, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=farbe_bhd, label='Baring Head CCGCRV Fit')
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=farbe_heid, label='Cape Grim CCGCRV Fit', linestyle = 'dashed')
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
# plt.legend(loc=(1.04,0.5))
plt.xticks([])


xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
# plot data for left panel
plt.title('CCGCRV Trend')
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])


xtr_subsplot = fig.add_subplot(gs[2:4, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])

xtr_subsplot = fig.add_subplot(gs[2:4, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
# plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/DEV_FirstDraft_figure3b_D14C.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
# </editor-fold>

"""
The next block re-imports the same results but from the other intercomparison file for plotting in FM. 
"""
from heidelberg_intercomparison_wFM import xtot_bhd, ytot_bhd, ztot_bhd, xtot_heid, ytot_heid, ztot_heid, x1_bhd, data1, data2, data3, my_x_1986_1991, curve1, curve2, curve3, bhd_1986_1991_mean_smooth, bhd_1986_1991_mean_trend, heidelberg_1986_1991_mean_smooth, heidelberg_1986_1991_mean_trend
from heidelberg_intercomparison_wFM import my_x_1986_1991, my_x_1991_1994, my_x_2006_2016, my_x_2006_2009, my_x_2012_2016
from heidelberg_intercomparison_wFM import bhd_1991_1994_mean_trend, bhd_1991_1994_mean_smooth
from heidelberg_intercomparison_wFM import heidelberg_1991_1994_mean_trend, heidelberg_1991_1994_mean_smooth
from heidelberg_intercomparison_wFM import bhd_2006_2009_mean_trend, bhd_2006_2009_mean_smooth
from heidelberg_intercomparison_wFM import heidelberg_2006_2009_mean_trend, heidelberg_2006_2009_mean_smooth
from heidelberg_intercomparison_wFM import bhd_2012_2016_mean_trend, bhd_2012_2016_mean_smooth
from heidelberg_intercomparison_wFM import heidelberg_2012_2016_mean_trend, heidelberg_2012_2016_mean_smooth
from heidelberg_intercomparison_wFM import means, my_x_2006_2009_trimmed, my_x_2012_2016_trimmed

# <editor-fold desc="Heidelberg v Rafter: Broad Overview of all data">
"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size1)
plt.legend()
plt.title('Baring Head and Cape Grim Data > 1980')
plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('FM', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/DEV_FirstDraft_figure1_FM.png',
            dpi=300, bbox_inches="tight")
plt.close()


# <editor-fold desc="Heidelberg v Rafter: 4 - Time Interval, Smooth Curve Fits">
fig = plt.figure(4, figsize=(10,5))
gs = gridspec.GridSpec(4, 8)
gs.update(wspace=1.2, hspace=0.5)
# Generate first panel

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
# plot data for left panel
plt.title('CCGCRV Smooth')
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=farbe_bhd)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=farbe_heid, linestyle = 'dashed')
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])
plt.ylabel('FM', fontsize=14)  # label the y axis
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=farbe_bhd)
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=farbe_heid, linestyle = 'dashed')
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=farbe_bhd)
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=farbe_heid, linestyle = 'dashed')
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[0:2, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=farbe_bhd, label='Baring Head CCGCRV Fit')
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=farbe_heid, label='Cape Grim CCGCRV Fit', linestyle = 'dashed')
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
# plt.legend(loc=(1.04,0.5))
plt.xticks([])

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
# plot data for left panel
plt.title('CCGCRV Trend')
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])

plt.ylabel('FM', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])


xtr_subsplot = fig.add_subplot(gs[2:4, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=farbe_heid, linestyle = 'dashed')
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])

xtr_subsplot = fig.add_subplot(gs[2:4, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=farbe_bhd, s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=farbe_heid, s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=farbe_bhd)
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=farbe_heid,linestyle = 'dashed')
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
# plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/DEV_FirstDraft_figure3b_FM.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
# </editor-fold>

# <editor-fold desc="Flask v NaOH Intercomparison">
"""
Flask V NaOH Plot
"""

plt.errorbar(flaskvn['Decimal_date'], flaskvn['D14C_flask'], yerr=flaskvn['D14C_err_flask'], fmt='o', color=farbe_bhd, ecolor='black', elinewidth=1, capsize=2, label='Flask')
plt.errorbar(flaskvn['Decimal_date'], flaskvn['D14C_NaOH'], yerr=flaskvn['D14C_err_NaOH'], fmt='o', color=farbe_bhd, ecolor='black', elinewidth=1, capsize=2, label='NaOH')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis
plt.legend()
plt.close()

fig = plt.figure(1, figsize=(10,5))
gs = gridspec.GridSpec(1, 2)
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.errorbar(naoh1['DEC_DECAY_CORR'], naoh1['DELTA14C'], yerr=naoh1['DELTA14C_ERR'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='NaOH', alpha = 0.5)
plt.errorbar(flask1['DEC_DECAY_CORR'], flask1['DELTA14C'], yerr=flask1['DELTA14C_ERR'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='Flask', alpha = 0.5)
plt.plot(fake_x1, naoh_means1, color=farbe_bhd, label='NaOH')
plt.plot(fake_x1, flask_means1,color=farbe_bhd, label='Flask')
plt.xlim(min(flask1['DEC_DECAY_CORR']), max(naoh1['DEC_DECAY_CORR']))
plt.ylim(150, 230)
plt.legend()
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plt.errorbar(naoh2['DEC_DECAY_CORR'], naoh2['DELTA14C'], yerr=naoh2['DELTA14C_ERR'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='NaOH', alpha = 0.5)
plt.errorbar(flask2['DEC_DECAY_CORR'], flask2['DELTA14C'], yerr=flask2['DELTA14C_ERR'], fmt='o', color=farbe_bhd, ecolor=farbe_bhd, elinewidth=1, capsize=2, label='Flask', alpha = 0.5)
plt.plot(fake_x2, naoh_means2, color=farbe_bhd, label='NaOH')
plt.plot(fake_x2, flask_means2, color=farbe_bhd, label='Flask')
plt.xlim(min(flask2['DEC_DECAY_CORR']), max(flask2['DEC_DECAY_CORR']))
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/FlaskvNaOH.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>



df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Interlab_Comparison\output\Results_table_for_pub.xlsx')  # import data

D14C = df.loc[(df['Parameter Used'] == 'D14C')]
sns.barplot(x=D14C['Time Period'], y=D14C['Result'],  palette="Blues_d")
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/Final_Results_D14C.png',
            dpi=300, bbox_inches="tight")
plt.close()

FM = df.loc[(df['Parameter Used'] == 'FM')]
sns.barplot(x=FM['Time Period'], y=FM['Result'],  palette="Blues_d")
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/Final_Results_FM.png',
            dpi=300, bbox_inches="tight")
plt.close()


