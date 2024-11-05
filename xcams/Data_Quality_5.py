"""
A quick discussion of beam currents to add to the paper...following on Haydens masters thesis\
tw 3345
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogFormatter

# read in AMS Submission output
df = pd.read_excel(r'I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3300-3349/TW3345/export.xlsx').dropna(subset='F_corrected_normed')

# read in OUTFILE
currents = pd.read_excel(r'I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3300-3349/TW3345/currents.xlsx')

# simplify the columns
currents = currents[['run','position','TP#','12CLEcurr']].rename(columns={"TP#":'TP'})

# merge
df = currents.merge(df, on='TP', how='outer')

bhdamb = df.loc[df['Job::R'] == '40430/1'].reset_index(drop=True)

# going to hard-code this for simplicity:
x = np.unique(bhdamb['wtgraph'])
print(x)
p0 = bhdamb.loc[bhdamb['wtgraph'] == x[0]]
p1 = bhdamb.loc[bhdamb['wtgraph'] == x[1]]
p2 = bhdamb.loc[bhdamb['wtgraph'] == x[2]]
p3 = bhdamb.loc[bhdamb['wtgraph'] == x[3]]
p4 = bhdamb.loc[bhdamb['wtgraph'] == x[4]]
p5 = bhdamb.loc[bhdamb['wtgraph'] == x[5]]
p6 = bhdamb.loc[bhdamb['wtgraph'] == x[6]]
p7 = bhdamb.loc[bhdamb['wtgraph'] == x[7]]
p8 = bhdamb.loc[bhdamb['wtgraph'] == x[8]]
p9 = bhdamb.loc[bhdamb['wtgraph'] == x[9]]
p10 = bhdamb.loc[bhdamb['wtgraph'] == x[10]]
p11 = bhdamb.loc[bhdamb['wtgraph'] == x[11]]
p12 = bhdamb.loc[bhdamb['wtgraph'] == x[12]]

# reconcatonate in order of mass, large to small
bhdamb_1 = pd.concat([p12, p11, p10, p9, p8, p7, p6, p5, p4, p3, p2, p1, p0]).reset_index(drop=True)
bhdamb_1['rotation_number_edit'] = bhdamb_1.index
bhdamb_1.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_5_output/data_for_plot_ordered.xlsx')

bhdamb_1 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_5_output/data_for_plot_ordered_edited.xlsx', comment='#')

plt.figure()

# Set logarithmic scale for y-axis
plt.yscale('log')
plt.axvline(x=77, color='black', linestyle='-', alpha=0.05)
plt.ylim(5, 150)
plt.title('Example Currents from BHDAmb Test Wheel')
plt.scatter(bhdamb_1['rotation_number_edit'], bhdamb_1['12CLEcurr'], c=bhdamb_1['wtgraph'])
plt.gca().yaxis.set_major_formatter(LogFormatter())
plt.xticks([], [])
plt.ylabel(r'he$^{12}$C$^+$ ($\mu$Amp)')


plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_5_output/currents.png', dpi=300, bbox_inches="tight")

plt.close()

# print(np.unique(bhdamb['wtgraph']))