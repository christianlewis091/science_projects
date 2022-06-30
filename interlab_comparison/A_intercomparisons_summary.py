"""
This file is meant to SUMMARIZE the conclusions found from the intercomparisons that I've done, and create a nice
figure for our future publication.

We have intercompared the following institutions so far with RRL and found the following offsets:
Heidelberg University: variable with time. We have a fixed pre and post AMS offset, and a smoothed offset.
                       In the future, we are going to use the fixed pre and post offset, where the Pre is ~1.8 and the
                       post is 0. You can find the results printed from each time interval of where BHD and CGO records
                       overlap towards the end of A_heidelberg_intercomparison.py.
                       Then, these offsets are applied to the data we have in the following files:
                       C_CapeGrim_cleanup.py
                       C_Maquarie_cleanup.py
                       C_NeumayerCleanup.py
                       The smoothed offsets are created in the individual files themselves because they require the
                       individual record's x-values to output results related to those x-values. To find a list of
                       the smoothed offsets through time, we are going to find the one written to the Cape Grim offset
                       excel sheet (CapeGrim_offset.xlsx).
SIO/LLNL: This result can be found by running Pre_Processing_SIO_LLNL.py:
          The OFFSET FOR LLNL is -2.5789633251115838 ± 1.258654216869433. (LLNL LOWER than RRL).
          This is fixed through time, and can be
          troublesome beacuse RRL's NWT3/4 data, LLNL/SIO's NWT3/4 data, and the samples it is used to correct all vary
          in time:
          RRL: 2013 - 2018
          LLNL: <2013
          Heather's measurements: 2009.

INSTAAR: This offset is going to be set to the value found in Turnbull et al., 2015
         INSTAAR is 1.4 pm 0.2 per mil LOWER than RRL.

ANSTO: ANSTO offset is zero as can be seen via the Pre_Processing_ANSTO.py

The goal of this files is to make a nice plot that can be used for the future paper.

"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

"""
To keep the speed high, I'm going to avoid pulling variables from previous codes that must import the time-expensive
monte carlo simulations.
"""

cgo = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\CapeGrim_offset.xlsx')
cgo = cgo.iloc[::5, :]
cgo_x = cgo['Decimal_date']
cgo_offset1 = cgo['offset1']           # Pre and post AMS offset ( Will be set to zero but still plotting as is for now)
cgo_offset1 = cgo_offset1 * -1         # currently the offset in the analysis is positive. This is bceause I am adding
                                       # it to the CGO data. But in reality, Heidelberg U's data is slightly LOWER.
                                       # so for the purposes of this plot. I'm flipping it.

cgo_offset1_err = cgo['offset1_err']
cgo_offset2 = cgo['offset2']           # Smoothed offset
cgo_offset2_err = cgo['offset2_err']

sio = -2.5789633251115838
sio_err = 1.258654216869433

instaar = 1.4
instaar_err = 0.2

ansto = 0
ansto_err = 0

xmin = 1987
xmax = 2015
plt.title('Offset Analyses Summary')




plt.axhspan(-.5, .5, color=colors2[4], alpha=0.2)                     # GGMT recommended intercomparability

plt.errorbar(cgo_x, cgo_offset1, label='Heidelberg University',      # Heidelberg University
             yerr=cgo_offset1_err, fmt='o', color='black',
             ecolor='black', elinewidth=1, capsize=2)
# SIO PARAMETERS
plt.errorbar(xmin, sio, label='SIO/LLNL', yerr=sio_err, fmt='D', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)
plt.axhspan((sio+sio_err), (sio-sio_err), color=colors2[3], alpha=0.2)  # SIO line since it's a set value at all dates.
plt.text(1990, -3.5, r'SIO/LLNL Offset Range 1sigma', fontsize=7.5)

#INSTAAR PARAMETERS
plt.errorbar(xmin, instaar, label='INSTAAR', yerr=instaar_err, fmt='^', color=colors2[5], ecolor=colors2[5], elinewidth=1, capsize=2)
plt.axhspan((instaar+instaar_err), (instaar-instaar_err), color=colors2[5], alpha=0.2)  # SIO line since it's a set value at all dates.
plt.text(1990, instaar, r'INSTAAR Offset Range 1sigma', fontsize=7.5)


plt.axhline(y=0, color="black", linestyle="--")                      # zero line
plt.text(1990, 0.35, r'GGMT Recommended Intercomparability', fontsize=7.5)

plt.xlim([xmin, xmax])
plt.ylim([-4,4])
plt.legend()
plt.xlabel('Date', fontsize=14)
plt.ylabel('Offset (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/quickplot3.png',
            dpi=300, bbox_inches="tight")

plt.close()





























