import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import LogFormatter
import plotly.express as px

# here is the data from Jacob's analysis sheet
rcm10_data = pd.read_excel(r'I:/C14Data/Graphite/RCM10/Wheel data/RCMX_Analysis.xlsx', sheet_name='RCMX Data')

# here are the currents...
tw3504 = pd.read_excel(r'I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3500-3549/TW3504/TW3504_p1.xlsx')
tw3509 = pd.read_excel(r'I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3500-3549/TW3509/TW3509_1.xlsx')
tw3514 = pd.read_excel(r'I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3500-3549/TW3514/TW3514_2.xlsx')
tw3518 = pd.read_excel(r'I:/XCAMS/3_measurements/C-14 AMS/TW data analysis/TW3500-3549/TW3518/TW3518_1.xlsx')

# first I need to concat all the current data together, and then I can merge the results overtop...
# I need to merge the RCM10_data sheet to get the masses and other things associated with the data...
currents = pd.concat([tw3504, tw3509, tw3514, tw3518])

# only keep columns I really need
currents = currents[['run','position','TP#','12CLEcurr']].rename(columns={"TP#":'TP'})

# I also want to simplify Jacob's dataframe, for simplicity:
rcm10_data = rcm10_data[['Job::R', 'TP', 'TW', 'CRA', 'CRA_Error',
              'F_corrected_normed', 'F_corrected_normed_error', 'Collection Date',
              'JOB Notes', 'Samples::Sample ID', 'Samples::Sample Type',
              'Graphite::End Date', 'Graphite::Reactor_Name',
              'Graphite::mgFe_from_Pressure', 'Graphite::mgC_from_pCO2RT', '1/Mass',
              'Graphite::Prebake_Yield', 'Graphite::CO2_Yield',
              'Graphite::Graphite_Yield', 'Standard Type Number', 'Quality Flag',
              'Ratio to standard', '1 - RTS', 'Ratio to standard error']]

df_tot = currents.merge(rcm10_data, on='TP', how='outer')

# of course, the raw AMS data also contains primary standards and things which I dont want right now...
df_tot = df_tot.dropna(subset='TW')

# fix the rotation numbers
df_tot2 = pd.DataFrame()

Tps = np.unique(df_tot['TP'])
for i in range(0, len(Tps)): #iterate through the TP values

    tpi = df_tot.loc[df_tot['TP'] == Tps[i]].reset_index(drop=True)
    tpi['rotation_number'] = tpi.index

    df_tot2 = pd.concat([df_tot2, tpi])

df_tot = df_tot2.reset_index(drop=True) # rename to fit code below

df_tot['Mass'] = 1/df_tot['1/Mass'] # make a new column called mass

df_tot.to_excel(r'I:/C14Data/Graphite/RCM10/Wheel data/merge_out_CBL.xlsx')

# Just want to break up the differnt masses for a plot later with this new fake column
df_tot['Rot_number_edit'] = -999
print(min(df_tot['Mass']))
print(max(df_tot['Mass']))

# Define the edit_rot function
def edit_rot(df, const):
    df['Rot_number_edit'] = df['rotation_number'] + const
    return df

# Apply the function to the subset of the DataFrame
df_tot.loc[(df_tot['Mass'] > 0) & (df_tot['Mass'] < 0.030), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > 0) & (df_tot['Mass'] < 0.030), 'rotation_number'] + 105
df_tot.loc[(df_tot['Mass'] > .03) & (df_tot['Mass'] < 0.060), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .03) & (df_tot['Mass'] < 0.060), 'rotation_number'] + 90
df_tot.loc[(df_tot['Mass'] > .06) & (df_tot['Mass'] < 0.1), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .06) & (df_tot['Mass'] < 0.1), 'rotation_number'] + 75
df_tot.loc[(df_tot['Mass'] > .1) & (df_tot['Mass'] < 0.2), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .1) & (df_tot['Mass'] < 0.2), 'rotation_number'] + 60
df_tot.loc[(df_tot['Mass'] > .2) & (df_tot['Mass'] < 0.3), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .2) & (df_tot['Mass'] < 0.3), 'rotation_number'] + 45
df_tot.loc[(df_tot['Mass'] > .3) & (df_tot['Mass'] < 0.4), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .3) & (df_tot['Mass'] < 0.4), 'rotation_number'] + 30
df_tot.loc[(df_tot['Mass'] > .4) & (df_tot['Mass'] < 0.5), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .4) & (df_tot['Mass'] < 0.5), 'rotation_number'] + 15
df_tot.loc[(df_tot['Mass'] > .5), 'Rot_number_edit'] = df_tot.loc[(df_tot['Mass'] > .5), 'rotation_number'] + 0

df_tot = df_tot.loc[df_tot['TP'] != 88101]
df_tot = df_tot.loc[df_tot['TP'] != 88100]
df_tot = df_tot.loc[df_tot['TP'] != 88099]
sample = np.unique(df_tot['Samples::Sample ID'])
print(sample)
"""
Recreating plots from XU and WALKER PAPERS
BLANKS!!!
"""

def plot_beam_currents(column_name):

    # Create a new figure
    plt.figure()
    blanks = df_tot.loc[df_tot['Samples::Sample ID'] == column_name]
    blanktps = np.unique(blanks['TP'])
    for i in range(0, len(blanktps)):
        tp1 = blanks.loc[blanks['TP'] == blanktps[i]]
        plt.scatter(tp1['Rot_number_edit'], tp1['12CLEcurr'])

    # Set logarithmic scale for y-axis
    plt.yscale('log')
    plt.ylim(1, 150)
    plt.xlim(0,120)
    plt.gca().yaxis.set_major_formatter(LogFormatter())
    plt.xticks([], [])
    plt.ylabel(r'he$^{12}$C$^+$ ($\mu$Amp)')
    plt.title(f'{column_name}')
    plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)
    # add vertical lines for mass deliniation
    vertical_lines_x = [15, 30,45, 60, 75, 90, 105]  # Specify x-values where vertical lines should be added
    names =            ['.03','.06','.1','.2','.3','.4','.5','.6']
    for line_x in vertical_lines_x:
        plt.axvline(x=line_x, color='black', linestyle='-', alpha=0.05)

    plt.text(0, 1.25, '>0.6', horizontalalignment='left', verticalalignment='center')
    plt.text(15, 1.25, '0.5', horizontalalignment='left', verticalalignment='center')
    plt.text(30, 1.25, '0.4', horizontalalignment='left', verticalalignment='center')
    plt.text(45, 1.25, '0.3', horizontalalignment='left', verticalalignment='center')
    plt.text(60, 1.25, '0.2', horizontalalignment='left', verticalalignment='center')
    plt.text(75, 1.25, '0.1', horizontalalignment='left', verticalalignment='center')
    plt.text(90, 1.25, '0.06', horizontalalignment='left', verticalalignment='center')
    plt.text(105, 1.25, '0.03', horizontalalignment='left', verticalalignment='center')


    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/{column_name}_currents.png', dpi=300, bbox_inches="tight")
    plt.close()


# plot the beam currents
for item in sample:
    plot_beam_currents(item)

# plot the blank performance
plt.figure()
kap = df_tot.loc[df_tot['Samples::Sample ID'] == 'Kapuni CO2']
marb = df_tot.loc[df_tot['Samples::Sample ID'] == 'IAEA-C1']
kaur = df_tot.loc[df_tot['Samples::Sample ID'] == 'Kauri 0157 - Wk17031']
plt.scatter(kap['Mass'], kap['F_corrected_normed'], label='Kapuni CO2', marker='D', color='black')
plt.scatter(marb['Mass'], marb['F_corrected_normed'], label= 'Carrera Marble', marker='o', color='gray')
plt.scatter(kaur['Mass'], kaur['F_corrected_normed'], label='Kauri', marker='^', color='slategray')
plt.xlabel('Mass')
plt.ylabel('FM')
plt.title('Blanks')
plt.legend()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/blanks_FM.png', dpi=300, bbox_inches="tight")
plt.close()

# plot oxalic performance
plt.figure()
ox = df_tot.loc[df_tot['Samples::Sample ID'] == 'Oxalic']

plt.errorbar(ox['Mass'], ox['F_corrected_normed'], yerr=ox['F_corrected_normed_error'], label='Oxalic', marker='o', color='black', linestyle='')
plt.axhline(y=1, color='black', linestyle='-', alpha=0.05)
plt.xlabel('Mass')
plt.ylabel('FM')
plt.title('Oxalic')
plt.legend()
plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/Oxalic_FM.png', dpi=300, bbox_inches="tight")
plt.close()



# plt.figure()
# blanks = df_tot.loc[df_tot['Samples::Sample ID'] == 'Kapuni CO2']
# plt.scatter(blanks['Mass'], blanks['F_corrected_normed'], zorder=1, color='black')
# plt.xlabel('Mass')
# plt.ylabel('FM')
# plt.title('Kapuni')
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/blank_FM.png', dpi=300, bbox_inches="tight")
# plt.close()

# """
# C1!
# """
#
# # Create a new figure
# plt.figure()
# blanks = df_tot.loc[df_tot['Samples::Sample ID'] == 'IAEA-C1']
# blanktps = np.unique(blanks['TP'])
# for i in range(0, len(blanktps)):
#     tp1 = blanks.loc[blanks['TP'] == blanktps[i]]
#     plt.scatter(tp1['Rot_number_edit'], tp1['12CLEcurr'])
#
# # Set logarithmic scale for y-axis
# plt.yscale('log')
# plt.ylim(1, 150)
# plt.xlim(0,120)
# plt.gca().yaxis.set_major_formatter(LogFormatter())
# plt.xticks([], [])
# plt.ylabel(r'he$^{12}$C$^+$ ($\mu$Amp)')
# plt.title('IAEA-C1')
# plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)
# # add vertical lines for mass deliniation
# vertical_lines_x = [15, 30,45, 60, 75, 90, 105]  # Specify x-values where vertical lines should be added
# names =            ['.03','.06','.1','.2','.3','.4','.5','.6']
# for line_x in vertical_lines_x:
#     plt.axvline(x=line_x, color='black', linestyle='-', alpha=0.05)
#
# plt.text(0, 1.25, '>0.6', horizontalalignment='left', verticalalignment='center')
# plt.text(15, 1.25, '0.5', horizontalalignment='left', verticalalignment='center')
# plt.text(30, 1.25, '0.4', horizontalalignment='left', verticalalignment='center')
# plt.text(45, 1.25, '0.3', horizontalalignment='left', verticalalignment='center')
# plt.text(60, 1.25, '0.2', horizontalalignment='left', verticalalignment='center')
# plt.text(75, 1.25, '0.1', horizontalalignment='left', verticalalignment='center')
# plt.text(90, 1.25, '0.06', horizontalalignment='left', verticalalignment='center')
# plt.text(105, 1.25, '0.03', horizontalalignment='left', verticalalignment='center')
#
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/IAEA_currents.png', dpi=300, bbox_inches="tight")
# plt.close()
#
# plt.figure()
# blanks = df_tot.loc[df_tot['Samples::Sample ID'] == 'IAEA-C1']
# plt.scatter(blanks['Mass'], blanks['F_corrected_normed'], zorder=1, color='black')
# plt.xlabel('Mass')
# plt.ylabel('FM')
# plt.title('IAEA-C1')
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/IAEA_C1_FM.png', dpi=300, bbox_inches="tight")
# plt.close()
#
#
#
#
# """
# OXALIC!
# """
#
# plt.figure()
# blanks = df_tot.loc[df_tot['Samples::Sample ID'] == 'Oxalic']
# print(blanks)
#
# blanktps = np.unique(blanks['TP'])
# for i in range(0, len(blanktps)):
#     tp1 = blanks.loc[blanks['TP'] == blanktps[i]]
#     plt.scatter(tp1['Rot_number_edit'], tp1['12CLEcurr'])
#
# # Set logarithmic scale for y-axis
# plt.yscale('log')
# plt.ylim(1, 150)
# plt.xlim(0,120)
# plt.gca().yaxis.set_major_formatter(LogFormatter())
# plt.xticks([], [])
# plt.ylabel(r'he$^{12}$C$^+$ ($\mu$Amp)')
# plt.title('Oxalic')
# plt.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)
# # add vertical lines for mass deliniation
# vertical_lines_x = [15, 30,45, 60, 75, 90, 105]  # Specify x-values where vertical lines should be added
# names =            ['.03','.06','.1','.2','.3','.4','.5','.6']
# for line_x in vertical_lines_x:
#     plt.axvline(x=line_x, color='black', linestyle='-', alpha=0.05)
#
# plt.text(0, 1.25, '>0.6', horizontalalignment='left', verticalalignment='center')
# plt.text(15, 1.25, '0.5', horizontalalignment='left', verticalalignment='center')
# plt.text(30, 1.25, '0.4', horizontalalignment='left', verticalalignment='center')
# plt.text(45, 1.25, '0.3', horizontalalignment='left', verticalalignment='center')
# plt.text(60, 1.25, '0.2', horizontalalignment='left', verticalalignment='center')
# plt.text(75, 1.25, '0.1', horizontalalignment='left', verticalalignment='center')
# plt.text(90, 1.25, '0.06', horizontalalignment='left', verticalalignment='center')
# plt.text(105, 1.25, '0.03', horizontalalignment='left', verticalalignment='center')
#
#
# plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/ox_currents.png', dpi=300, bbox_inches="tight")
# plt.close()

"""
FIGURE IN PLOTLY
"""
# import plotly.io as pio
# import plotly.graph_objects as go
# # Create a Plotly figure
# fig = go.Figure()
# """
# OXALIC!!!
# """
# blanks = df_tot.loc[df_tot['Samples::Sample ID'] == 'Oxalic']
#
# # Add scatter plots for each unique TP value
# for tp in blanktps:
#     tp1 = blanks.loc[blanks['TP'] == tp]
#     fig.add_trace(go.Scatter(
#         x=tp1['Rot_number_edit'],
#         y=tp1['12CLEcurr'],
#         mode='markers',
#         name=f'TP {tp}'
#     ))
#
# # Set logarithmic scale for y-axis
# fig.update_yaxes(type='log')
#
# # Set custom y-axis label
# fig.update_yaxes(title_text=r'he$^{12}$C$^+$ ($\mu$Amp)')
#
# # Set title and disable x-axis ticks
# fig.update_layout(
#     title='RCM10 he$^{12}$C$^+$ ($\mu$Amp)',
#     xaxis=dict(
#         showticklabels=False
#     ),
#     yaxis=dict(
#         title_text='he$^{12}$C$^+$ ($\mu$Amp)'
#     ),
#     showlegend=True
# )
#
# # Add a grid
# fig.update_xaxes(showgrid=False)
# fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='LightGrey')
#
# # Save the plot as an HTML file
# pio.write_html(fig, file='C:/Users/clewis/IdeaProjects/GNS/xcams/small_graphite_output/oxalic.html')


# # fig = px.scatter(subset1, x="TP", y="F_corrected_normed", error_y='F_corrected_normed_error', title=f'{name}')
# fig.write_html(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_4_output/{name}.html')

