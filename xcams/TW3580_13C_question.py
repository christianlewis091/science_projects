"""
Why is rowena's 13C IRMS so different from AMS? Is it normal, due to dilution by CO2 or due to AMS problem?
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3580\rowena_13C_check.xlsx")
gl = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3580\Grech-Licari foram results.xlsx")
foram = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3580\foram_13C_check.xlsx").dropna(subset='delta13C_IRMS')
foram = foram.loc[foram['wtgraph'] >0.3]
#
"""
plot rowena and gl together
"""

dontwant = ['CO2 extracted from CH4 BHD','CO2 from whole air flask','CO2_from_whole_air_flask','FARI-A NIWA', 'FARI-B NIWA','CO2_NaOH_bottle','CO2 from CH4', 'CO2 extracted from CH4 in Baring Head Air sampled on 20/6/2020',
                                                                                                                    'CO2 extracted from CH4 in Baring Head Air sampled on 8/6/2019']

df = df.loc[~df['Samples::Sample Description'].isin(dontwant)]

# print(np.unique(df['Samples::Sample Description']))

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Plot line
ax.scatter(df['TP'], df['delta13C_AMS'], marker="o", color='black', label='13C AMS - Rowena CO')
ax.scatter(df['TP'], df['delta13C_IRMS'], marker="D", color='gray', label='13C IRMS - Rowena CO')

ax.scatter(foram['TP'], foram['delta13C_AMS'], marker="o", color='blue', label='13C AMS - historical forams')
ax.scatter(foram['TP'], foram['delta13C_IRMS'], marker="D", color='dodgerblue', label='13C IRMS - historical forams')

ax.scatter(gl['TP'], gl['delta13C_AMS'], marker="o", color='red', label='13C AMS - GrechLicari')
ax.scatter(gl['TP'], gl['delta13C_IRMS'], marker="D", color='orange', label='13C IRMS - GrechLicari')


# Labels and title
ax.set_xlabel("TP Number")
ax.set_ylabel("delta13C")
ax.set_title("")

# Show legend
ax.legend()

# Show plot
plt.savefig(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3580\TW3580_13C_AMS_vs_IRMS", dpi=300, bbox_inches="tight")
plt.close()
#
