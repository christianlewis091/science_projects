import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from X_my_functions import fm_to_d14c, two_tail_paired_t_test
from scipy import stats


colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

df = pd.read_excel(r'H:\The Science\Datasets\Ansto_intercomparison.xlsx', skiprows=28)
ansto = df.loc[(df['Site'] == 'ANSTO')]
ansto_x = ansto['Year of Growth']
rrl = df.loc[(df['Site'] == 'RRL')]
rrl_x = rrl['Year of Growth']
rrl_fm = rrl['FM']
rrl_fm_err = rrl['error']
ansto_fm = ansto['FM']
ansto_fm_err = ansto['error']


# first, I can check that my function works by converting RRL FM to D14C and check against the reported D14C.
# x = fm_to_d14c(rrl_fm, rrl_fm_err, rrl_x)
# YES IT WORKS.

x = fm_to_d14c(ansto_fm, ansto_fm_err, ansto_x)
ansto_D14C = x[0]
ansto_D14C_err = x[1]



X = stats.ttest_rel(ansto_D14C, rrl['D14C'])
print(X)
# very high p-value indicates that there is no difference between the two datasets. No offset needs to be applied.


size = 50

plt.errorbar(ansto_x, ansto_D14C, label='ANSTO', yerr=ansto_D14C_err,
             fmt='D', color=colors[3], ecolor=colors[3], elinewidth=1, capsize=2)
plt.errorbar(rrl_x, rrl['D14C'], label='RRL', yerr=rrl['D14C_err'],
             fmt='o', color=colors2[3], ecolor=colors2[3], elinewidth=1, capsize=2)


plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/reading_group_pres/ANSTOvRRL.png',
    dpi=300, bbox_inches="tight")






# T test testing.
#
#
# # pre holds the mileage before applying
# # the different engine oil
# pre = [88, 82, 84, 93, 75, 78, 84, 87,
#        95, 91, 83, 89, 77, 68, 91]
#
# # post holds the mileage before applying
# # the different engine oil
# post = [91, 84, 88, 90, 79, 80, 88, 90,
#         90, 96, 88, 89, 81, 74, 92]
#
# # Performing the paired sample t-test
# X = stats.ttest_rel(pre, post)
# print(X)
#














