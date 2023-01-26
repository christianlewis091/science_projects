import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd

df = pd.read_excel('I:/XCAMS/4_maintenance/vacuum pumps/RotaryPump_Testing_AfterMaintenance.xlsx')


c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'
plt.scatter(df['AM673883 Time'], df['AM673883 Torr'], label='AM673883, Suspect Pump With Cu Oil Mist Filter (20/1/23)', color=c1, alpha=0.5, marker='o')
plt.plot(df['AM673883 Time'], df['AM673883 Torr'], color=c1, linestyle='-')

plt.scatter(df['AM673883 Time 2'], df['AM673883 Torr 2'], label='AM673883, Suspect Pump WithOUT Cu Oil Mist Filter (20/1/23)', color=c1, alpha=0.5, marker='x')
plt.plot(df['AM673883 Time 2'], df['AM673883 Torr 2'], color=c1, linestyle='-')

plt.scatter(df['AM673883 Time 3'], df['AM673883 Torr 3'], label='AM673883, Suspect Pump WITH Cu oil mist filter, after return from Workshop (27/1/23)', color=c1, alpha=0.5, marker='s')
plt.plot(df['AM673883 Time 3'], df['AM673883 Torr 3'], color=c1, linestyle='-')


plt.ylim(0.0001, .1)
plt.axhline(0.005, color='black', linestyle='--')
plt.text(900, 0.002, 'Desired Range')
plt.xlabel('Time (s)')
plt.ylabel('Convectron Reading (Torr)')
plt.legend()
plt.savefig('I:/XCAMS/4_maintenance/vacuum pumps/RotaryPump_Testing_AfterMaintenance.png', dpi=95, bbox_inches="tight")
