import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm as mpl_cm
cmap = mpl_cm.viridis
from scipy import stats
from scipy.stats import linregress

df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3593\past_wtgraphs.xlsx")
ox = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3593\past_wtgraphs_ox.xlsx")
spike = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3593\past_wtgraphs_bhdspike.xlsx")

tws = np.unique(df['TW'])
ox = ox.loc[ox['TW'].isin(tws)]
spike = spike.loc[spike['TW'].isin(tws)]

fig = plt.subplots(figsize=(12, 8))
plt.scatter(df['TW'], df['wtgraph'], color='black', label='CO2_from_whole_air_flask')
plt.scatter(ox['TW'], ox['wtgraph'], color='red', marker='s', label='OX1 CO2 flask', alpha=0.4)
plt.scatter(spike['TW'], spike['wtgraph'], color='blue', marker='D', s=100, label='BHDspike2013', alpha=0.4)
plt.xlim(3550,3600)
plt.legend()
plt.xlabel('TW')
plt.ylabel('wtgraph')
plt.savefig(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3593/wtgraphs.png",
            dpi=300, bbox_inches="tight")
