import matplotlib.pyplot as plt
import numpy as np

# Data
sites = [
    "Bahia San Pedro, Chile", "Raul Marin Balmaceda", "Tortel river", "Tortel island",
    "Seno Skyring", "Monte Tarn, Punta Arenas", "Puerto Navarino, Isla Navarino",
    "Baja Rosales, Isla Navarino", "near Kapuni school field, NZ", "Baring Head, NZ",
    "23 Nikau St, Eastbourne, NZ", "19 Nikau St, Eastbourne, NZ", "Haast Beach, paddock near beach",
    "Oreti Beach", "Campbell island"
]
STZ = [2, 2, 1, 1, 1, 1, 0, 0, 59, 56, 52, 52, 56, 35, 11]
SAZ = [81, 83, 78, 80, 71, 65, 61, 60, 23, 23, 26, 26, 22, 31, 34]
PFZ = [5, 4, 5, 4, 7, 8, 9, 9, 4, 6, 6, 6, 7, 10, 15]
ASZ = [6, 5, 8, 8, 11, 13, 14, 14, 9, 9, 12, 12, 11, 18, 24]
SIZ = [5, 6, 7, 7, 10, 13, 15, 16, 3, 3, 3, 3, 4, 5, 11]

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

ax.bar(sites, STZ, label='STZ')
ax.bar(sites, SAZ, bottom=STZ, label='SAZ')
ax.bar(sites, PFZ, bottom=np.array(STZ) + np.array(SAZ), label='PFZ')
ax.bar(sites, ASZ, bottom=np.array(STZ) + np.array(SAZ) + np.array(PFZ), label='ASZ')
ax.bar(sites, SIZ, bottom=np.array(STZ) + np.array(SAZ) + np.array(PFZ) + np.array(ASZ), label='SIZ')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_xlabel('Site')
ax.set_ylabel('Values')
ax.set_title('Stacked Values by Site and Zone')
ax.set_xticks(np.arange(len(sites)))
ax.set_xticklabels(sites, rotation=90)
ax.legend()

# Show the plot
plt.tight_layout()
plt.show()
