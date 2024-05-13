
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.gridspec as gridspec
import seaborn as sns
colors2 = sns.color_palette("mako", 7)
colors2= list(reversed(colors2))


results = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS.xlsx')

"""
I want to see how the D14C for the Different Southern Ocean basins are changing over time. However, currently, 
the pot. density anomaly min and max are only set for the Southern OCean as a whole. Im just going to manually assign the values to the correct rows below. 
"""

results.loc[(results['Water Mass'] == 'Layer 10'), 'roe_min'] = 26.1
results.loc[(results['Water Mass'] == 'Layer 10'), 'roe_max'] = 26.4
results.loc[(results['Water Mass'] == 'Layer 11_AAIW'), 'roe_min'] = 26.4
results.loc[(results['Water Mass'] == 'Layer 11_AAIW'), 'roe_max'] = 26.9
results.loc[(results['Water Mass'] == 'Layer 16'), 'roe_min'] = 27.4
results.loc[(results['Water Mass'] == 'Layer 16'), 'roe_max'] = 36.8
results.loc[(results['Water Mass'] == 'Layers 12_13'), 'roe_min'] = 26.9
results.loc[(results['Water Mass'] == 'Layers 12_13'), 'roe_max'] = 27.1
results.loc[(results['Water Mass'] == 'Layers 14-15'), 'roe_min'] = 27.1
results.loc[(results['Water Mass'] == 'Layers 14-15'), 'roe_max'] = 27.4
results.loc[(results['Water Mass'] == 'Layers 1_9_Upper Ocean'), 'roe_min'] = 0
results.loc[(results['Water Mass'] == 'Layers 1_9_Upper Ocean'), 'roe_max'] = 26.1

# results.to_excel('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY_RESULTS_EDITED.xlsx')

# better to make a function than repeating this for ages below.
def plotting_func(input1, sel_xticks=None, sel_yticks=None):
    subdf = results.loc[results['Ocean Region'] == input1].reset_index(drop=True)
    subdf = subdf.sort_values(by='roe_min')
    for i in range(0, len(subdf)):
        row = subdf.iloc[i]
        roe_max = row['roe_max']
        x = [1990, 2000, 2010]
        y = [row['DELC14_MEAN_1990s'],
             row['DELC14_MEAN_2000s'],
             row['DELC14_MEAN_2010s']]
        errbar = [row['DELC14_STD_1990s'],
                  row['DELC14_STD_2000s'],
                  row['DELC14_STD_2010s']]

        lab = row['Water Mass']
        plt.errorbar(x,y, errbar, label=f'\u03C3$_\u03B8$ {roe_max}', color=colors2[i])
        plt.title(f'{input1}')
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.ylim(-250, 150)
        plt.scatter(x,y, color=colors2[i])
        if sel_xticks == 'off':
            plt.xticks([], [])
        if sel_yticks == 'off':
            plt.yticks([], [])

fig = plt.figure(1, figsize=(12, 9))
gs = gridspec.GridSpec(3, 3)
gs.update(wspace=.6, hspace=.25)

xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
plotting_func('North Atlantic', sel_xticks='off')

xtr_subsplot = fig.add_subplot(gs[1:2, 0:1])
plotting_func('South Atlantic', sel_xticks='off')
plt.ylabel('\u0394$^1$$^4$C (\u2030)')

xtr_subsplot = fig.add_subplot(gs[2:3, 0:1])
plotting_func('Southern - Atlantic Sector')

xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plotting_func('North Pacific', sel_xticks='off', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[1:2, 1:2])
plotting_func('South Pacific', sel_xticks='off', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[2:3, 1:2])
plotting_func('Southern - Pacific Sector', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[1:2, 2:3])
plotting_func('Indian', sel_xticks='off', sel_yticks='off')

xtr_subsplot = fig.add_subplot(gs[2:3, 2:3])
plotting_func('Southern - Indian Sector', sel_yticks='off')

plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP4_data_analysis/STEP4_SUMMARY.jpg', dpi=300, bbox_inches="tight")
