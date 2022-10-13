import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference_dictionary_10000_101222.xlsx')
ref = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')

"""Setup some colors for later"""
# https://colorbrewer2.org/#type=sequential&scheme=BuGn&n=3
# Skyblue to distant mountain green
c1, c2, c3 = '#ece2f0', '#a6bddb', '#1c9099'
d1, d2 = '#ef8a62', '#67a9cf'
size1 = 10
date = df['Decimal_date']
D14C_raw = df['D14C']



fig = plt.figure(1)
plt.scatter(date, D14C_raw, marker='o', label='All data', color=d2, s=size1)
plt.plot(ref['Decimal_date'], ref['D14C'], label='CGO+BHD', color='black', alpha=0.4)
plt.legend()
plt.title('')
# plt.xlim([1985, 2020])
# plt.ylim([0, 220])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.show()
# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/analysis_p1.png',
#             dpi=300, bbox_inches="tight")
# plt.close()