"""
Data Quality Paper 1 = adding descriptors and flagging
Data Quality Ppaer 2 = looking at blanks and making plots
Data Quality Paper 3 = calculate residuals of secondary standards and making plots
Data Quality Paper 4 = this one = create a few figures that overlay different secondaries in a PUBLISHABLE figure.
"""
import pandas as pd
import numpy as np
import warnings
import xlsxwriter
from datetime import date
warnings.simplefilter(action='ignore')
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
today = date.today()
from drawing import *
import seaborn as sns
import statsmodels.api as sm

df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_3_output/df_with_residuals.csv')


"""
2 plots vertical
"""
fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(2, 1)
gs.update(wspace=0.1, hspace=0.3)

"""
We will make a plot of the carbonate's? Travertine , and the two corals
"""
#Travertine = 14047_2
#LAC1 = 41347_2
#LAA1 = 41347_3
rs = ['14047_2','41347_2','41347_3']
descrips = ['IAEA-C2 travertine','LAC1 Coral','LAA1 Coral']
colors = sns.color_palette("mako", len(rs))
colors2 = sns.color_palette("rocket", len(rs))
markers = ['o','s','D','*','^','<','>']

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])

for i in range(0, 3):
    subset = df.loc[df['New_R'] == rs[i]]
    plt.scatter(subset['TP'], subset['Residual'], alpha=0.5, label=descrips[i], marker=markers[i], color=colors[i])

plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
plt.ylabel(f'Residual (x-\u0078\u0305/1-\u03c3)')
plt.xlabel('TP, chronological lab identifier')
plt.fill_between(df['TP'], -1, 1, alpha=.05, color='black')
plt.fill_between(df['TP'], -2, 2, alpha=.05, color='black')
plt.title(f'Add Title Later')
plt.legend()

"""
Airs 
"""
rs = ['40430_1','40430_2']
descrips = ['BHD Ambient Air','BHD Spiked']

# plot structure
xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])


for i in range(0, 2):
    subset = df.loc[df['New_R'] == rs[i]]
    plt.scatter(subset['TP'], subset['Residual'], alpha=0.5, label=descrips[i], marker=markers[i], color=colors[i])

plt.axhline(y=0, color='black', linestyle='-', linewidth=1)
plt.ylabel(f'Residual (x-\u0078\u0305/1-\u03c3)')
plt.xlabel('TP, chronological lab identifier')
plt.fill_between(df['TP'], -1, 1, alpha=.05, color='black')
plt.fill_between(df['TP'], -2, 2, alpha=.05, color='black')
plt.title(f'Add Title Later')
plt.legend()

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/Fig.png', dpi=300, bbox_inches="tight")
plt.close()





"""
Airs 
"""


