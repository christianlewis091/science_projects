import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from Pre_Processing_UniMagallanes import combine_Magallanes
import seaborn as sns
from intercomparison_math_1 import ansto, rrl, sio_nwt3, sio_nwt4, rrl_nwt3, rrl_nwt4, y1, y1_average, y1_1sigma, y2, y2_average, y2_1sigma, y3, y3_average, y3_1sigma, y4, y4_average, y4_1sigma
from A_heidelberg_intercomparison import xtot_bhd, ytot_bhd, ztot_bhd, xtot_heid, ytot_heid, ztot_heid, x1_bhd, data1, data2, data3, my_x_1986_1991, curve1, curve2, curve3, bhd_1986_1991_mean_smooth, bhd_1986_1991_mean_trend, heidelberg_1986_1991_mean_smooth, heidelberg_1986_1991_mean_trend
from A_heidelberg_intercomparison import my_x_1986_1991, my_x_1991_1994, my_x_2006_2016, my_x_2006_2009, my_x_2012_2016
from A_heidelberg_intercomparison import bhd_1991_1994_mean_trend, bhd_1991_1994_mean_smooth
from A_heidelberg_intercomparison import heidelberg_1991_1994_mean_trend, heidelberg_1991_1994_mean_smooth
from A_heidelberg_intercomparison import bhd_2006_2009_mean_trend, bhd_2006_2009_mean_smooth
from A_heidelberg_intercomparison import heidelberg_2006_2009_mean_trend, heidelberg_2006_2009_mean_smooth
from A_heidelberg_intercomparison import bhd_2012_2016_mean_trend, bhd_2012_2016_mean_smooth
from A_heidelberg_intercomparison import heidelberg_2012_2016_mean_trend, heidelberg_2012_2016_mean_smooth
from A_heidelberg_intercomparison import means, my_x_2006_2009_trimmed, my_x_2012_2016_trimmed
size1 = 5
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']


# <editor-fold desc="SIO v Rafter">
"""
SIO/LLNL V Rafter Plot
"""
fig = plt.figure(4, figsize=(16.1, 10))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=.5, hspace=.5)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.errorbar(rrl_nwt3['Decimal_date'], rrl_nwt3['D14C'], yerr=rrl_nwt3['D14C_err'], fmt='o', color=colors2[3], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT3')
plt.axhline(y=y3_average, color='black', linestyle='-')
plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=colors2[4], alpha=0.3)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis
plt.legend()

plt.ylim(30,55)

xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
plt.errorbar(rrl_nwt4['Decimal_date'], y4, yerr=rrl_nwt4['D14C_err'], fmt='o', color=colors2[4], ecolor='black', elinewidth=1, capsize=2, label='RRL NWT4')
plt.axhline(y=y4_average, color='black', linestyle='-')
plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=colors2[5], alpha=0.3)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.legend()
plt.ylim(-40,-24)
plt.xlabel('Date of Measurement', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
plt.ylim(30,55)
# plt.axhline(y=y3_average, color='black', linestyle='-')
# plt.axhspan((y3_average-y3_1sigma), (y3_average+y3_1sigma), facecolor=colors2[4], alpha=0.3)
plt.errorbar(sio_nwt3['Decimal_date'], y1, yerr=sio_nwt3['D14C_err'], fmt='X', color=colors[3], ecolor='black', elinewidth=1, capsize=2, label='LLNL NWT3')
plt.axhline(y=y1_average, color='black', linestyle='--')
plt.axhspan((y1_average-y1_1sigma), (y1_average+y1_1sigma), facecolor=colors[4], alpha=0.3)
plt.xlabel('Measurement #', fontsize=14)  # label the y axis
plt.legend()


xtr_subsplot = fig.add_subplot(gs[2:4, 2:4])
plt.ylim(-40,-24)
# plt.axhline(y=y4_average, color='black', linestyle='-')
# plt.axhspan((y4_average-y4_1sigma), (y4_average+y4_1sigma), facecolor=colors2[5], alpha=0.3)
plt.errorbar(sio_nwt4['Decimal_date'], y2, yerr=sio_nwt3['D14C_err'], fmt='X', color=colors[4], ecolor='black', elinewidth=1, capsize=2, label='LLNL NWT4')
plt.axhline(y=y2_average, color='black', linestyle='--')
plt.axhspan((y2_average-y2_1sigma), (y2_average+y2_1sigma), facecolor=colors[4], alpha=0.3)
plt.xlabel('Measurement #', fontsize=14)  # label the y axis
plt.legend()

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/dev_restructure/SIOLLNLvRRL.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="ANSTO v Rafter">
"""
ANSTO v RRL Plot
"""
plt.errorbar(rrl['Decimal_date'], rrl['D14C'], label='RRL', yerr=rrl['D14C_err'], fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(ansto['Decimal_date'], ansto['D14C'], label='ANSTO', yerr=ansto['D14C_err'], fmt='D', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/dev_restructure/ANSTOvRRL.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="Magallanes v RRL">
plt.errorbar(combine_Magallanes['Decimal_date'], combine_Magallanes['D14C_x'], label='RRL', yerr=combine_Magallanes['D14C_err_x'],
             fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.errorbar(combine_Magallanes['Decimal_date'], combine_Magallanes['D14C_y'], label='Uni Magallanes', yerr=combine_Magallanes['D14C_err_y'],
             fmt='D', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/dev_restructure/MagallanesvRRL.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: Broad Overview of all data">
"""
Figure 1. All the data together
"""
fig = plt.figure(1)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size1)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size1)
plt.legend()
plt.title('Baring Head and Cape Grim Data > 1980')
plt.xlim([1980, 2020])
plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/DEV_FirstDraft_figure1.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: Vizualization of Monte Carlo Smoothing Process">
"""
Figure 2. Visual Example of the randomization and smoothing process.
"""
fig = plt.figure(2)

plt.title('Visualization of Monte Carlo and CCGCRV Process: 1987-1991 BHD')
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x')
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^')
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's')
plt.plot(my_x_1986_1991, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(my_x_1986_1991, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(my_x_1986_1991, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
plt.plot(my_x_1986_1991, bhd_1986_1991_mean_smooth, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 180])
plt.legend()
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/DEV_FirstDraft_figure2.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
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
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
# plt.plot(xs, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
# plt.plot(xs, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
# plt.plot(xs, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
# plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.text(1990.75, 167.5, "B", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
plt.plot(my_x_1986_1991, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(my_x_1986_1991, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(my_x_1986_1991, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
# plt.plot(xs, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
plt.text(1991.5,135,'Date')
xtr_subsplot.set_yticklabels([])

xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.text(1990.75, 167.5, "C", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
plt.plot(my_x_1986_1991, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(my_x_1986_1991, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(my_x_1986_1991, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
plt.plot(my_x_1986_1991, means, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
# plt.plot(xs, means2, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
xtr_subsplot.set_yticklabels([])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.text(1990.75, 167.5, "D", fontsize=12)
plt.errorbar(xtot_bhd, ytot_bhd, label='CGO Data' , yerr=ztot_bhd, fmt='none', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color='black', s=size2)
plt.scatter(x1_bhd, data1, color = colors[0], label = 'Monte Carlo Iteration 1', alpha = 0.35, marker = 'x', s = size2)
plt.scatter(x1_bhd, data2, color = colors[1],  label = 'Monte Carlo Iteration 2', alpha = 0.35, marker = '^', s = size2)
plt.scatter(x1_bhd, data3, color = colors[2],  label = 'Monte Carlo Iteration 3', alpha = 0.35, marker = 's', s = size2)
plt.plot(my_x_1986_1991, curve1, color = colors[0], alpha = 0.35, linestyle = 'dotted')
plt.plot(my_x_1986_1991, curve2, color = colors[1], alpha = 0.35, linestyle = 'dashed')
plt.plot(my_x_1986_1991, curve3, color = colors[2], alpha = 0.35, linestyle = 'dashdot')
plt.plot(my_x_1986_1991, bhd_1986_1991_mean_smooth, color = 'red',  label = 'CCGCRV Smooth Values', alpha = 1, linestyle = 'solid')
plt.plot(my_x_1986_1991, bhd_1986_1991_mean_trend, color = 'blue',  label = 'CCGCRV Trend Values', alpha = 1, linestyle = 'solid')
plt.xlim([1989, 1991])
plt.ylim([140, 170])
plt.legend(loc=(1.04,0.5))
xtr_subsplot.set_yticklabels([])

plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/DEV_FirstDraft_figureS1.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: Old plot showing the smoothing of Heidelberg Data">
"""
Figure 3. A breakdown of the 4 periods of time that we test for the intercomparison,
and how the smooth and trend data compare for each.
"""
size2 = 15
# plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.5)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.5)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3], label = 'BHD CCGCRV Smooth Fit')
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3], label = 'BHD CCGCRV Trend Fit', linestyle = 'dashed')
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3], label = 'CGO CCGCRV Smooth Fit')
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3], label = 'CGO CCGCRV Trend Fit', linestyle = 'dashed')
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3], linestyle = 'dashed')
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3], linestyle = 'dashed')
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3], linestyle = 'dashed')
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3], linestyle = 'dashed')
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3], linestyle = 'dashed')
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3], linestyle = 'dashed')
plt.axvline(x = 1987, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 1991, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 1994, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2006, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2009, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2012, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.axvline(x = 2016, color = 'black', alpha = 0.2, linestyle = 'solid')
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.arrow(1994, 50, -6, 0,  fc="k", ec="k",head_width=0.05, head_length=0.1 )
plt.xlabel('Date', fontsize=14)  # label the y axis
# plt.ylim([0, 200])
# plt.xlim([1986, 2020])
# for presentation figure
plt.ylim([150, 175])
plt.xlim([1988, 1991])
# plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/DEV_FirstDraft_Figuretest2.png',
            dpi=300, bbox_inches="tight")
plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: 4 - Time Interval, Smooth Curve Fits">
fig = plt.figure(4, figsize=(10 ,3))
gs = gridspec.GridSpec(1, 8)
gs.update(wspace=1, hspace=0.1)
# Generate first panel

xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])


xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3], label='Baring Head CCGCRV Fit')
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3], label='Cape Grim CCGCRV Fit')
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
plt.legend(loc=(1.04,0.5))
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/DEV_FirstDraft_figure3a.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
# </editor-fold>

# <editor-fold desc="Heidelberg v Rafter: 4 - Time Interval, Trend Fits">
fig = plt.figure(4, figsize=(10 ,3))
gs = gridspec.GridSpec(1, 8)
gs.update(wspace=1, hspace=0.1)
# Generate first panel
# remember, the grid spec is rows, then columns

# print(type(my_x_1986_1991))
# print(type(np.array(my_x_1986_1991)))
# print(type(bhd_1986_1991_mean_smooth))

xtr_subsplot = fig.add_subplot(gs[0:1, 0:2])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1986_1991), bhd_1986_1991_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1986_1991), heidelberg_1986_1991_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1986_1991)), max(np.array(my_x_1986_1991))])
plt.ylim([min(bhd_1986_1991_mean_smooth), max(bhd_1986_1991_mean_smooth)])

plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis

xtr_subsplot = fig.add_subplot(gs[0:1, 2:4])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_1991_1994), bhd_1991_1994_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_1991_1994), heidelberg_1991_1994_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_1991_1994)), max(np.array(my_x_1991_1994))])
plt.ylim([min(bhd_1991_1994_mean_smooth), max(bhd_1991_1994_mean_smooth)])


xtr_subsplot = fig.add_subplot(gs[0:1, 4:6])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2006_2009_trimmed), bhd_2006_2009_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2006_2009_trimmed), heidelberg_2006_2009_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2006_2009_trimmed)), max(np.array(my_x_2006_2009_trimmed))])
plt.ylim([min(bhd_2006_2009_mean_smooth), max(bhd_2006_2009_mean_smooth)])

xtr_subsplot = fig.add_subplot(gs[0:1, 6:8])
# plot data for left panel
plt.scatter(xtot_bhd, ytot_bhd, marker='o', label='Rafter Baring Head Record (BHD)', color=colors[3], s=size2, alpha = 0.3)
plt.scatter(xtot_heid, ytot_heid, marker='x', label='Heidelberg Cape Grim Record (CGO)', color=colors2[3], s=size2, alpha = 0.3)
# plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_smooth, color=colors[3])
plt.plot(np.array(my_x_2012_2016_trimmed), bhd_2012_2016_mean_trend, color=colors[3])
# plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_smooth, color=colors2[3])
plt.plot(np.array(my_x_2012_2016_trimmed), heidelberg_2012_2016_mean_trend, color=colors2[3])
plt.xlim([min(np.array(my_x_2012_2016_trimmed)), max(np.array(my_x_2012_2016_trimmed))])
plt.ylim([min(bhd_2012_2016_mean_smooth), max(bhd_2012_2016_mean_smooth)])
# plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/DEV_FirstDraft_figure3b.png',
            dpi=300, bbox_inches="tight")
# plt.show()
plt.close()
# </editor-fold>

