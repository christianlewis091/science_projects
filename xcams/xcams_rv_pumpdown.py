"""
Updates:
August 31, 2023
Descriptions added to this section. New pump tests added.

This script is used to plot various things in XCAMS, including:
- the relationship between ionizer voltage and wattage readback
- the testing of rotary backing pumps when they are returned from the workshop
- + more
"""

# IMPORT STATEMENTS
import matplotlib.pyplot as plt
import pandas as pd

"""
***************************************************************************************************
This section relates to testing the relationship between SCICS Ionizer voltage and wattage readback 
***************************************************************************************************
"""
# df = pd.read_excel(
#     r'I:\XCAMS\4_maintenance\SNICS ion source\SNICS OPENINGS\SORX reports\2023\June14_2023\ionizerwattage.xlsx').reset_index(
#     drop=True)
# df = df.loc[df['Case'] == 'ovn_off']
#
# df = df.sort_values('A').reset_index(drop=True)
# plt.title('Ionizer Wattage Readback After Ion Source Clean')
# plt.plot(df['A'], df['WR'], color='darkred', label='Oven off')
# plt.scatter(df['A'], df['WR'], color='black')
# plt.plot(df['A'], df['WR_model'], color='black', alpha=0.5, label='Modeled')
#
# df = pd.read_excel(
#     r'I:\XCAMS\4_maintenance\SNICS ion source\SNICS OPENINGS\SORX reports\2023\June14_2023\ionizerwattage.xlsx').reset_index(
#     drop=True)
# df = df.loc[df['Case'] == 'ovn_on']
# plt.scatter(df['A'], df['WR'], color='black', marker='D', label='Oven on')
#
# plt.xlabel('Amps (Current Applied by User)')
# plt.ylabel('Wattage Readback (P (watts) =I$^2$R)')
# plt.legend()
# plt.savefig(r'I:\XCAMS\4_maintenance\SNICS ion source\SNICS OPENINGS\SORX reports\2023\June14_2023\WattageReadback.png',
#             dpi=300, bbox_inches="tight")
#
# df = pd.read_excel(
#     r'I:\XCAMS\4_maintenance\SNICS ion source\SNICS OPENINGS\SORX reports\2023\June14_2023\Pumpdowns.xlsx')
#
# df1 = df.loc[df['Day'] == 'Day 1']
# plt.plot(df1['Time_min'], df1['Rough'], label='Rough - Day 1', color='black', linestyle='-')
# plt.plot(df1['Time_min'], df1['Turbo'], label='Turbo - Day 1', color='black', linestyle='--')
#
# df2 = df.loc[df['Day'] == 'Day 2']
# plt.plot(df2['Time_min'], df2['Rough'], label='Rough - Day 2', color='darkred', linestyle='-')
# plt.plot(df2['Time_min'], df2['Turbo'], label='Turbo - Day 2', color='darkred', linestyle='--')
# plt.yscale('log')
# plt.legend()
# plt.savefig(r'I:\XCAMS\4_maintenance\SNICS ion source\SNICS OPENINGS\SORX reports\2023\June14_2023\SORXpumpdown.png',
#             dpi=300, bbox_inches="tight")
# plt.close()
#
#
"""
***************************************************************************************************
This section relates to testing rotary backing pumps that come back from the workshop 
***************************************************************************************************
"""
import numpy as np
df = pd.read_excel('I:\XCAMS/4_maintenance/01_Vacuum_Pumps\Alcatel Adixen/RotaryPump_Testing_AfterMaintenance.xlsx', sheet_name='TidyVersion', comment='#')
its = np.unique(df['Number'])

# edit this line to determine which one is bold and which are transpoaret.
x = 16 # which number pump change are you on MINUS ONE! beacuse of the way python counts
date = 'Oct24_25'

fig = plt.figure(1, figsize=(12, 8))

for i in range(0, len(its)):
    df_i = df.loc[df['Number'] == its[i]].reset_index(drop=True)

    # extract name for plot title
    id_tag = df_i['MaintenanceID']
    id_tag = id_tag[0]

    # plot this one
    if i == x:
        a = 1
    else:
        a = 0.2
    plt.scatter(df_i['Time'], df_i['Vacuum'], label=id_tag, alpha=a)
    plt.plot(df_i['Time'], df_i['Vacuum'], alpha=a)


plt.ylim(0.0001, 1000)
plt.axhline(0.005, color='black', linestyle='-', alpha=0.1)

plt.xlabel('Time (min)'), plt.ylabel('Convectron Reading (Torr)')
plt.yscale("log"), plt.legend()
plt.title(r'C:\Users\clewis\IdeaProjects\GNS\xcams\xcams_rv_pumpdown.py')
plt.savefig(f'I:\XCAMS/4_maintenance/01_Vacuum_Pumps\Alcatel Adixen/PUMPDOWNSPEED_{date}.png', dpi=300, bbox_inches="tight")



#
"""
***************************************************************************************************
Plotting issue from standy more Febraury 3-4 2023
***************************************************************************************************
"""
#
# df = pd.read_excel('I:/XCAMS/2_procedures/08_XCAMS_To_Standby_Mode/Standby_vac_progression_030223.xlsx')
# fig, axs = plt.subplots(2, sharex=True)
#
# axs[0].scatter(df['Time (Minutes)'], df['Backing'], label='Backing Vacuum', alpha=0.5, marker='s')
# axs[0].plot(df['Time (Minutes)'], df['Backing'], linestyle='-')
#
# axs[1].scatter(df['Time (Minutes)'], df['Ion Gauge'], label='ICG03', alpha=0.5, marker='s')
# axs[1].plot(df['Time (Minutes)'], df['Ion Gauge'], linestyle='-')
#
# axs[0].set_title('Backing Vac, Convectron Reading')
# axs[1].set_title('Beamline Ion Gauge Reading')
#
# axs[1].set_xlabel('Minutes')
#
# plt.savefig('I:/XCAMS/2_procedures/08_XCAMS_To_Standby_Mode/IGC03_after_standby.png', dpi=95, bbox_inches="tight")


"""
***************************************************************************************************
Plotting pumpdowns after Ion suorce cleans
***************************************************************************************************
"""

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# from matplotlib.gridspec import GridSpec
#
# # Load data
# df = pd.read_excel(r"I:\XCAMS\4_maintenance\02_SNICS ion source\SNICS OPENINGS\SORX reports\2023\June14_2023\Pumpdowns.xlsx", comment='#')
# df = df[['Time_min','Rough','Turbo']]
#
# fig = plt.figure(figsize=(12, 8))
# gs = GridSpec(1, 2, width_ratios=[1, 2], figure=fig)
#
# ax1 = fig.add_subplot(gs[0, 0])
# cleans = np.unique(df['Opening Event'])
#
# for i in range(len(cleans)):
#     this_clean = df.loc[(df['Opening Event'] == cleans[i]) & (df['Turbo Pump'] > -999)]
#     x = this_clean['Time_Min'].reset_index(drop=True)
#     y = this_clean['Rough Pump']
#
#     ax1.scatter(x, y, label=f'{cleans[i]}')
#     ax1.plot(x, y)
# ax1.set_xlim(-10, 400)
# ax1.set_xlabel('Time (min)')
# ax1.set_ylabel('Vacuum (Torr)')
# ax1.set_yscale('log')
# ax1.set_title('Rough Pump Vacuum After Ion Source Rebuilds')
# ax1.legend()
#
# # Second plot on the right
# ax2 = fig.add_subplot(gs[0, 1])
#
# for i in range(len(cleans)):
#     this_clean = df.loc[(df['Opening Event'] == cleans[i]) & (df['Turbo Pump'] > -999)]
#     x = this_clean['Time_Min'].reset_index(drop=True)
#     y = this_clean['Turbo Pump']
#
#     ax2.scatter(x, y, label=f'{cleans[i]}')
#     ax2.plot(x, y)
# ax2.set_xlim(-10, 400)
# ax2.set_xlabel('Time (min)')
# ax2.set_ylabel('Vacuum (Torr)')
# ax2.set_yscale('log')
# ax2.set_title('Turbo Pump Vacuum After Ion Source Rebuilds')
# ax2.legend()
#
# # Show and save the plot
# plt.tight_layout()
# plt.savefig('H:/Science/Pumpdowns.png',
#             dpi=300, bbox_inches="tight")
# plt.show()
# # plt.close()

"""
***************************************************************************************************
Stripper trap bake 2025 Realignment Sept 29
***************************************************************************************************
"""
#
# import matplotlib.pyplot as plt
# import pandas as pd
#
# fig = plt.figure(1, figsize=(12, 8))
# df = pd.read_excel(r'I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Hands-on\September_29_2025\Stripper_Trap_Bake.xlsx')
#
# plt.scatter(df['Elapsed Time 2'], df['Vacuum (Torr)'])
# plt.plot(df['Elapsed Time 2'], df['Vacuum (Torr)'])
#
#
# plt.ylim(0.0001, 1000)
# # plt.axhline(0.005, color='black', linestyle='-', alpha=0.1)
#
#
# plt.xlabel('Time (min)'), plt.ylabel('Convectron Reading (Torr)')
# plt.yscale("log"), plt.legend()
# plt.title(r'C:\Users\clewis\IdeaProjects\GNS\xcams\xcams_rv_pumpdown.py')
# plt.savefig(r'I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Hands-on\September_29_2025/stripperBakeout_plot.png', dpi=300, bbox_inches="tight")
