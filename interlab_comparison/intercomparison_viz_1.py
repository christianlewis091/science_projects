import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from colorspacious import cspace_converter
import pandas as pd
import seaborn as sns
from intercomparison_math_1 import ansto, rrl, sio_nwt3, sio_nwt4, rrl_nwt3, rrl_nwt4, rafter, magallanes, y1, y1_average, y1_1sigma, y2, y2_average, y2_1sigma, y3, y3_average, y3_1sigma, y4, y4_average, y4_1sigma
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']

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

plt.show()

# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/reading_group_pres/SIOLLNLvRRL.png',
#             dpi=300, bbox_inches="tight")
# plt.close()