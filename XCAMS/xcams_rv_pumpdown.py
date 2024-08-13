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
df = pd.read_excel('I:/XCAMS/4_maintenance/vacuum pumps/Alcatel Adixen/RotaryPump_Testing_AfterMaintenance.xlsx')

# WHEN YOU TEST A NEW PUMP, ADD THE NAME OF THE COLUMNS BELOW
vacuum_reading_columns = ['AM673883 Torr','AM673883 Torr 2','AM673883 Torr 3','Torr 4','Torr 5','Torr 6','Torr 7','Torr 8', 'Torr 9', 'Torr 10','Torr_11', 'Torr_12']
time_reading_columns = ['AM673883 Time','AM673883 Time 2','AM673883 Time 3','AM673198 Time','AM673888 Time','AM672417 Time',' AS10988 Time','AM672414_083123 Time', 'SciTekScrewPump','AM673878_07032024_Time','AM673883_290724','AM673198_08082024']
labels = ['AM673883','AM673883','AM673883','AM673198','AM673888','AM672417',' AS10988','AM672414_083123','SciTekScrewPump','AM673878_July7,2024','AM673883_290724','AM673198_08082024']

# SETUP PARAMETERS TO MAKE PLOTTING RUN SMOOTHLY
colors = ['b','g','r','c','m','y','k','b','g','r','c','m','y','k','b','g','r','c','m','y','k']

# INITIALIZE THE FIGURE
fig = plt.figure(1, figsize=(8, 8))

# LOOP THROUGH THE PUMPS
for i in range(0, len(vacuum_reading_columns)):
    x = df[f'{time_reading_columns[i]}']
    y = df[f'{vacuum_reading_columns[i]}']
    x = x/60  # convert to minutes
    label1 = labels[i]

    plt.scatter(x,y, label=label1, marker=i)
    plt.plot(x,y, marker=i)
    plt.legend()

plt.ylim(0.0001, 1000)
plt.axhline(0.005, color='black', linestyle='-', alpha=0.1)

plt.xlabel('Time (min)'), plt.ylabel('Convectron Reading (Torr)')
plt.yscale("log"), plt.legend()
plt.title(r'C:\Users\clewis\IdeaProjects\GNS\xcams\xcams_rv_pumpdown.py')
plt.savefig('I:/XCAMS/4_maintenance/vacuum pumps/Alcatel Adixen/PUMPDOWNSPEED.png', dpi=300, bbox_inches="tight")
#
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
import numpy as np

df = pd.read_excel('I:/XCAMS/4_maintenance/SNICS ion source/SNICS OPENINGS/SORX reports/2024/1_July_2024/Pumpdowns.xlsx')

fig = plt.figure(1, figsize=(8, 8))

cleans = np.unique(df['Opening Event'])

for i in range(0, len(cleans)):
    this_clean = df.loc[(df['Opening Event'] == cleans[i]) & (df['Turbo Pump'] > -999)]  # grab only after gate valve is open
    x = this_clean['Time_Min'].reset_index(drop=True)
    x = x - x[0]

    y = this_clean['Turbo Pump']

    plt.scatter(x,y, label=f'{cleans[i]}')
    plt.plot(x,y)
plt.xlabel('Time (min)')
plt.ylabel('Vacuum (Torr)')
plt.legend()
plt.yscale('log')
plt.title('Turbo Pump Vacuum After Ion Source Rebuilds')

plt.savefig('I:/XCAMS/4_maintenance/SNICS ion source/SNICS OPENINGS/SORX reports/2024/1_July_2024/Pumpdowns.png',
            dpi=300, bbox_inches="tight")
plt.close()
