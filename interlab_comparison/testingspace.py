import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\lewis\venv\python310\python-masterclass-remaster-shared\radiocarbon_intercomparison2\interlab_comparison\offset_10000.xlsx').dropna(subset=['offset'])



offset = df['offset']
offset_err = df['offset_errors']
xs = df['tree_ring_xs']

plt.errorbar(xs, offset, label='Tree Rings offset from background' , yerr=offset_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2, alpha = 0.15)
# plt.scatter(sample_xs, offsets, label='Tree Rings Data offset from Harmonized Background', color='black', alpha = 0.15)
plt.legend()
plt.xlabel('Year of Growth', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
# plt.ylim([-50, 50])
# plt.savefig('C:/Users/lewis/venv/python310/python-masterclass-remaster-shared/'
#             'radiocarbon_intercomparison2/interlab_comparison/plots/tree_ring_offsets_errorprop_10000.png',
#             dpi=300, bbox_inches="tight")

plt.show()
plt.close()