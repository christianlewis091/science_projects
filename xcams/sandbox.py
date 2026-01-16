"""
Water blank only
"""
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/df_out_from_DQ_2_2025.xlsx')

name = 'Carrera Marble Water Line'

plt.figure(figsize=(8, 6))

subset = df.loc[(df['Job::R'] == '14047/11')]
wmean_num = np.sum(subset['F_corrected_normed']/subset['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset['F_corrected_normed_error']**2)
wmean = wmean_num / wmean_dem

#before blank fix
subset2 = df.loc[(df['Job::R'] == '14047/11') & (df['TW'] < 3488)]
wmean_num = np.sum(subset2['F_corrected_normed']/subset2['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset2['F_corrected_normed_error']**2)
wmean2 = wmean_num / wmean_dem

# afterblank fix
subset3 = df.loc[(df['Job::R'] == '14047/11') & (df['TW'] >= 3488)]
wmean_num = np.sum(subset3['F_corrected_normed']/subset3['F_corrected_normed_error']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
wmean_dem = np.sum(1/subset3['F_corrected_normed_error']**2)
wmean3 = wmean_num / wmean_dem

xmax = np.max(df['TP'])
xmin = np.max(df['TP'])
# TP 87300 is after the 87272 control on the water test wheel
plt.hlines(wmean2, xmin=np.min(subset2['TP']), xmax=87300, colors='black')
plt.hlines(wmean3, xmin=87300, xmax=np.max(subset3['TP']), colors='red', zorder=10)

plt.axvline(87300, color='black', linestyle='--', alpha=0.5)

plt.errorbar(subset2['TP'],subset2['F_corrected_normed'] , yerr=subset2['F_corrected_normed_error'], color='black', linestyle='', marker='o')
plt.errorbar(subset3['TP'],subset3['F_corrected_normed'] , yerr=subset3['F_corrected_normed_error'], color='black', linestyle='', label = f'{name}', marker='o')
plt.legend()

plt.ylabel('Fraction Modern')
plt.xlabel('TP')

plt.tight_layout()
plt.savefig(f'C:/Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_paper_3_2025_output/blanks/waters_special_plot.png',
            dpi=300, bbox_inches="tight")
print(wmean)
print(wmean2)
print(wmean3)
print('Differences between the wmean (for all waters blanks) and those found in the table at the 6th decimal point (should I eye roll at myself?) are beacuse im taking the wmean of rts and then converting to FM for table, while taking wmean of FM here')


