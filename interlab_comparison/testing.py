import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend
import seaborn as sns

rands = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\rands.xlsx')  # import heidelberg data
smooths = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\smooths.xlsx')  # import heidelberg data
mean = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\mean.xlsx')  # import heidelberg data

rands2 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\rands2.xlsx')  # import heidelberg data
trends2 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\trends2.xlsx')  # import heidelberg data
mean2 = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\mean2.xlsx')  # import heidelberg data

baringhead = pd.read_excel(r'H:\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
baringhead = baringhead.dropna(subset=['DELTA14C'])            # drop bad 14C values
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
xtot_bhd = baringhead['DEC_DECAY_CORR']                        # extract entire dataset x-values
ytot_bhd = baringhead['DELTA14C']                              # entire dataset y-values
ztot_bhd = baringhead['DELTA14C_ERR']                          # entire dataset z-values
fake_x_temp = np.linspace(min(xtot_bhd), max(xtot_bhd), 480)   # identify some fake X-values at which to plot data
xs = pd.DataFrame(fake_x_temp)

# EXTRACT THE RETURNED DATA FROM SMOOTH
mean = mean['Means']    # extracts the means from the summary DataFrame
#
rand1 = rands.iloc[1]
print(len(rand1))
print(len(xtot_bhd))
rand2 = rands.iloc[2]
rand3 = rands.iloc[3]
rand4 = rands.iloc[4]
rand5 = rands.iloc[5]
smooths1 = smooths.iloc[1]
smooths2 = smooths.iloc[2]
smooths3 = smooths.iloc[3]
smooths4 = smooths.iloc[4]
smooths5 = smooths.iloc[5]

# EXTRACT THE RETURNED DATA FROM TREND
mean2 = mean2['Means']    # extracts the means from the summary DataFrame

rand6 = rands2.iloc[1]
rand7 = rands2.iloc[2]
rand8 = rands2.iloc[3]
rand9 = rands2.iloc[4]
rand10 = rands2.iloc[5]
trend6 = trends2.iloc[1]
trend7 = trends2.iloc[2]
trend8 = trends2.iloc[3]
trend9 = trends2.iloc[4]
trend10 = trends2.iloc[5]

colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

fig, (ax1, ax2) = plt.subplots(1, 2)
# plot the randomized data...
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand4, color=colors[3], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand5, color=colors[4], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
# plot the smoothed data...
ax1.plot(fake_x_temp, smooths1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths2, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths4, color=colors[3], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths5, color=colors[4], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax1.plot(fake_x_temp, mean, color='black', label='Mean', alpha=1)
ax1.set_xlim([1980, 1982])
ax1.set_ylim([250, 290])

ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand7, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand9, color=colors[3], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand10, color=colors[4], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
# plot the smoothed data...
ax2.plot(fake_x_temp, trend6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend7, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend9, color=colors[3], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend10, color=colors[4], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax2.plot(fake_x_temp, mean, color='black', label='Mean', alpha=1)
ax2.set_xlim([1980, 1982])
ax2.set_ylim([250, 290])


plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/FirstDraft_figure2.png',
    dpi=300, bbox_inches="tight")


plt.show()
plt.close()

# ADJUST / BEAUTIFY PLOT LATER.
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html


fig, (ax1, ax2) = plt.subplots(1, 2)
# plot the randomized data...
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand4, color=colors[3], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand5, color=colors[4], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
# plot the smoothed data...
ax1.plot(fake_x_temp, smooths1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths2, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths4, color=colors[3], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths5, color=colors[4], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax1.plot(fake_x_temp, mean, color='black', label='Mean', alpha=1)
ax1.set_xlim([1980, 1982])
ax1.set_ylim([250, 290])

ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand7, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand9, color=colors[3], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand10, color=colors[4], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
# plot the smoothed data...
ax2.plot(fake_x_temp, trend6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend7, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend9, color=colors[3], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend10, color=colors[4], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax2.plot(fake_x_temp, mean, color='black', label='Mean', alpha=1)
ax2.set_xlim([1980, 1982])
ax2.set_ylim([250, 290])


plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/FirstDraft_figure2.png',
    dpi=300, bbox_inches="tight")


plt.show()
plt.close()

# ADJUST / BEAUTIFY PLOT LATER.
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html


