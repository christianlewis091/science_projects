import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3596\detector_pressure_rising.xlsx", comment='#')

plt.figure(figsize=(8, 6))
plt.scatter(df['Elapsed Time (hours)'], df['Detector Pressure'])
plt.plot(df['Elapsed Time (hours)'], df['Detector Pressure'],alpha=0.3)
plt.xlabel('Time Elapsed (Hours)')
plt.ylabel('Detector Pressure (Torr)')
plt.savefig(r"I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3597/detector_pressure.png", dpi=300, bbox_inches="tight")
plt.close()
