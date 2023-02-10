import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd

df = pd.read_excel('I:/XCAMS/4_maintenance/vacuum pumps/Alcatel Adixen/RotaryPump_Testing_AfterMaintenance.xlsx')

#
c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'
fig = plt.figure(1, figsize=(16, 8))
plt.scatter(df['AM673883 Time'], df['AM673883 Torr'], label='AM673883, Suspect Pump With Cu Oil Mist Filter (20/1/23)', color=c1, alpha=0.5, marker='o')
plt.plot(df['AM673883 Time'], df['AM673883 Torr'], color=c1, linestyle='-')

plt.scatter(df['AM673883 Time 2'], df['AM673883 Torr 2'], label='AM673883, Suspect Pump WithOUT Cu Oil Mist Filter (20/1/23)', color=c1, alpha=0.5, marker='x')
plt.plot(df['AM673883 Time 2'], df['AM673883 Torr 2'], color=c1, linestyle='-')

plt.scatter(df['AM673883 Time 3'], df['AM673883 Torr 3'], label='AM673883, Suspect Pump WITH Cu oil mist filter, after return from Workshop (27/1/23)', color=c1, alpha=0.5, marker='s')
plt.plot(df['AM673883 Time 3'], df['AM673883 Torr 3'], color=c1, linestyle='-')

plt.scatter(df['AM673198 Time'], df['Torr 4'], label='AM673198 Returned from shop 7/2/23', color='dodgerblue', alpha=0.5, marker='D')
plt.plot(df['AM673198 Time'], df['Torr 4'], color='dodgerblue', linestyle='-')

plt.scatter(df['AM673888 Time'], df['Torr 5'], label='AM673888 Returned from shop 9/2/23', color='black', alpha=0.5, marker='D')
plt.plot(df['AM673888 Time'], df['Torr 5'], color='black', linestyle='-')

plt.scatter(df['AM672417 Time'], df['Torr 6'], label='AM672417 Returned from shop 9/2/23', color='purple', alpha=0.5, marker='D')
plt.plot(df['AM672417 Time'], df['Torr 6'], color='purple', linestyle='-')

plt.ylim(0.0001, .1)
plt.axhline(0.005, color='black', linestyle='--')
plt.text(900, 0.002, 'Desired Range')
plt.xlabel('Time (s)')
plt.ylabel('Convectron Reading (Torr)')
plt.legend()
plt.savefig('I:/XCAMS/4_maintenance/vacuum pumps/RotaryPump_Testing_AfterMaintenance.png', dpi=95, bbox_inches="tight")
plt.close()









# """
# Plotting issue from standy more Febraury 3-4 2023
# """
#
# df = pd.read_excel('I:/XCAMS/2_procedures/08_XCAMS_To_Standby_Mode/Standby_vac_progression_030223.xlsx')
# fig, axs = plt.subplots(2, sharex=True)
#
# axs[0].scatter(df['Time (Minutes)'], df['Backing'], label='Backing Vacuum', color=c1, alpha=0.5, marker='s')
# axs[0].plot(df['Time (Minutes)'], df['Backing'], color=c1, linestyle='-')
#
# axs[1].scatter(df['Time (Minutes)'], df['Ion Gauge'], label='ICG03', color=c3, alpha=0.5, marker='s')
# axs[1].plot(df['Time (Minutes)'], df['Ion Gauge'], color=c3, linestyle='-')
#
# axs[0].set_title('Backing Vac, Convectron Reading')
# axs[1].set_title('Beamline Ion Gauge Reading')
#
# axs[1].set_xlabel('Minutes')
#
#
# plt.savefig('I:/XCAMS/2_procedures/08_XCAMS_To_Standby_Mode/IGC03_after_standby.png', dpi=95, bbox_inches="tight")
