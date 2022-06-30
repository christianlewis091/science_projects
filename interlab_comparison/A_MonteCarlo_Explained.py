import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend, long_date_to_decimal_date
import seaborn as sns

# Baring Head data excel file
baringhead = pd.read_excel(r'H:\The Science\Datasets'
                           r'\BHD_14CO2_datasets_20211013.xlsx')
baringhead = baringhead.dropna(subset=['DELTA14C'])            # drop bad 14C values
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > 0)]  # get rid of data where the error flag is -1000
xtot_bhd = baringhead['DEC_DECAY_CORR']                        # extract entire dataset x-values
ytot_bhd = baringhead['DELTA14C']                              # entire dataset y-values
ztot_bhd = baringhead['DELTA14C_ERR']                          # entire dataset z-values

heidelberg = pd.read_excel(r'H:\The Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)  # import heidelberg data
x_init_heid = heidelberg['Average pf Start-date and enddate']  # extract x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)  # convert the x-values to a decimal date
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe
heidelberg = heidelberg.dropna(subset=['D14C'])  # drop NaN's in the column I'm most interested in
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]  # Filtering out an outlier around 2019
heidelberg.reset_index()  # reset the index to avoid heaps of gnarly errors
xtot_heid = heidelberg['Decimal_date']  # entire dataset x-values
ytot_heid = heidelberg['D14C']  # entire dataset y-values
ztot_heid = heidelberg['weightedstderr_D14C']  # entire dataset error(z)-values

fake_x_temp = np.linspace(min(xtot_bhd), max(xtot_bhd), 480)   # identify some fake X-values at which to plot data
xs = pd.DataFrame(fake_x_temp)

# print(fake_x_temp)


n = 10000
# RUN THE FUNCTION
new_df = monte_carlo_randomization_smooth(xtot_bhd, fake_x_temp, ytot_bhd, ztot_bhd, 667, n)
new_df2 = monte_carlo_randomization_trend(xtot_bhd, fake_x_temp, ytot_bhd, ztot_bhd, 667, n)
new_df3 = monte_carlo_randomization_smooth(xtot_heid, fake_x_temp, ytot_heid, ztot_heid, 667, n)
new_df4 = monte_carlo_randomization_trend(xtot_heid, fake_x_temp, ytot_heid, ztot_heid, 667, n)

# EXTRACT THE RETURNED DATA FROM SMOOTH
rands = new_df[0]  # extract the first thing the function returns, the randomized data.
smooths = new_df[1]  # extract the second thing the function returns, the smoothed data. Each row = new iteration
mean = new_df[2]  # extracts the summary DataFrame
stdev = mean['stdevs']
mean = mean['Means']    # extracts the means from the summary DataFrame
#
rand1 = rands.iloc[1]
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
rands2 = new_df2[0]  # extract the first thing the function returns, the randomized data.
trends2 = new_df2[1]  # extract the second thing the function returns, the smoothed data. Each row = new iteration
mean2 = new_df2[2]  # extracts the summary DataFrame
stdev2 = mean2['stdevs']
mean2 = mean2['Means']    # extracts the means from the summary DataFrame


mean3 = new_df3[2]  # extracts the summary DataFrame
stdev3 = mean3['stdevs']
mean3 = mean3['Means']    # extracts the means from the summary DataFrame

mean4 = new_df4[2]  # extracts the summary DataFrame
stdev4 = mean4['stdevs']
mean4 = mean4['Means']    # extracts the means from the summary DataFrame

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
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)

ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])

plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp1.png',
    dpi=300, bbox_inches="tight")
plt.close()

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')


ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp2.png',
    dpi=300, bbox_inches="tight")
plt.close()


fig, (ax1, ax2) = plt.subplots(1, 2)
# plot the randomized data...
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')


ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand7, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp3.png.png',
    dpi=300, bbox_inches="tight")
plt.close()

fig, (ax1, ax2) = plt.subplots(1, 2)
# plot the randomized data...
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')

ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand7, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp4.png.png',
    dpi=300, bbox_inches="tight")
plt.close()


fig, (ax1, ax2) = plt.subplots(1, 2)
# plot the randomized data...
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
# plot the smoothed data...
ax1.plot(fake_x_temp, smooths1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths2, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...


ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand7, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')

# plot the smoothed data...
ax2.plot(fake_x_temp, trend6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend7, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])

plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp5.png.png',
    dpi=300, bbox_inches="tight")

plt.close()

fig, (ax1, ax2) = plt.subplots(1, 2)
# plot the randomized data...
ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.scatter(xtot_bhd, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax1.scatter(xtot_bhd, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax1.scatter(xtot_bhd, rand3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
# plot the smoothed data...
ax1.plot(fake_x_temp, smooths1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths2, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax1.plot(fake_x_temp, smooths3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax1.plot(fake_x_temp, mean, color='red', label='Monte Carlo Iteration 1')


ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.scatter(xtot_bhd, rand6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
ax2.scatter(xtot_bhd, rand7, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
ax2.scatter(xtot_bhd, rand8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')

# plot the smoothed data...
ax2.plot(fake_x_temp, trend6, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend7, color=colors[1], label='Monte Carlo Iteration 1', alpha=0.35)
ax2.plot(fake_x_temp, trend8, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35)
# and the mean...
ax2.plot(fake_x_temp, mean2, color='red', label='Monte Carlo Iteration 1')
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])

plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp6.png.png',
    dpi=300, bbox_inches="tight")

plt.close()




fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax1.plot(fake_x_temp, mean, color='red', label='Monte Carlo Iteration 1')
ax1.plot(fake_x_temp, (mean + stdev), color='blue', label='Monte Carlo Iteration 1', alpha = 0.5)
ax1.plot(fake_x_temp, (mean - stdev), color='blue', label='Monte Carlo Iteration 1', alpha = 0.5)

ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
ax2.plot(fake_x_temp, mean2, color='red', label='Monte Carlo Iteration 1')
ax2.plot(fake_x_temp, (mean2 + stdev2), color='blue', label='Monte Carlo Iteration 1', alpha = 0.5)
ax2.plot(fake_x_temp, (mean2 - stdev2), color='blue', label='Monte Carlo Iteration 1', alpha = 0.5)
ax1.set_xlim([1990, 1992])
ax1.set_ylim([140, 155])

ax2.set_xlim([1990, 1992])
ax2.set_ylim([140, 155])
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp7.png.png',
    dpi=300, bbox_inches="tight")

plt.close()

fig, (ax1, ax2) = plt.subplots(1, 2)

# ax1.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
# ax1.errorbar(xtot_heid, ytot_heid, yerr=ztot_heid, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)

ax1.plot(fake_x_temp, mean, color=colors[3], label='Monte Carlo Iteration 1')
ax1.plot(fake_x_temp, (mean + stdev), color=colors[3], label='Monte Carlo Iteration 1', alpha = 0.5)
ax1.plot(fake_x_temp, (mean - stdev), color=colors[3], label='Monte Carlo Iteration 1', alpha = 0.5)

ax1.plot(fake_x_temp, mean3, color=colors2[3], label='Monte Carlo Iteration 1')
ax1.plot(fake_x_temp, (mean3 + stdev3), color=colors2[3], label='Monte Carlo Iteration 1', alpha = 0.5)
ax1.plot(fake_x_temp, (mean3 - stdev3), color=colors2[3], label='Monte Carlo Iteration 1', alpha = 0.5)

# ax2.errorbar(xtot_bhd, ytot_bhd, yerr=ztot_bhd, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
# ax1.errorbar(xtot_heid, ytot_heid, yerr=ztot_heid, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)

ax2.plot(fake_x_temp, mean2, color=colors[3], label='RRL')
ax2.plot(fake_x_temp, (mean2 + stdev2), color=colors[3],  alpha = 0.5)
ax2.plot(fake_x_temp, (mean2 - stdev2), color=colors[3], alpha = 0.5)

ax2.plot(fake_x_temp, mean4, color=colors2[3], label='UH')
ax2.plot(fake_x_temp, (mean4 + stdev4), color=colors2[3],  alpha = 0.5)
ax2.plot(fake_x_temp, (mean4 - stdev4), color=colors2[3],  alpha = 0.5)
ax1.set_ylim([150, 175])
ax1.set_xlim([1988, 1991])
plt.legend()
ax2.set_ylim([150, 175])
ax2.set_xlim([1988, 1991])
plt.savefig(
    'C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/monte_exp9.png.png',
    dpi=300, bbox_inches="tight")

plt.show()