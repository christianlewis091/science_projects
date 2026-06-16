import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.gridspec as gridspec

# oxalic 26294/1
# carerra marble C1 14047/1
# kauri 40142/1
# Kapuni 40699/1

df = pd.read_excel("H:/Science/Datasets/graphite_storage7.xlsx").dropna(subset='AMS Submission Results Complete::AMS Category ID XCAMS').replace({"?":''}).dropna(subset='F_corrected_normed')
df['Job::R'] = df['Job::R'].str.replace('/', '_')
df = df.replace('', np.nan)


# some data needs to have quality flags added
df.loc[((df['Job::R'] == '26294_1') & (df['F_corrected_normed'] < 1)), 'Quality Flag'] = 'C..'  # IF OXALICS ARE TOO LOW(THERE ARE A FEW, ADD A CBL FLAG)
df.loc[((df['Job::R'] == '40699_1') & (df['F_corrected_normed'] > 0.01)), 'Quality Flag'] = 'C..'  # IF KAPUNIS ARE TOO HIGH(THERE ARE A FEW, ADD A CBL FLAG)
df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/graphite_storage/newflags.xlsx')
df = df.loc[df['Quality Flag'] == '...']

time = 60

rnums = np.unique(df['Job::R'])
print(rnums)

for i in range(0, len(rnums)):
    rnum_i = rnums[i]
    sub_df = df.loc[df['Job::R'] == rnum_i].reset_index(drop=True)
    if rnum_i == '26294_1':
        sub_df = sub_df.loc[sub_df['F_corrected_normed']>0]

    id = sub_df['Samples::Sample ID']
    id = id[0]

    sub_df = sub_df.loc[sub_df['DaysAsGraphite'] < time]

    av = round(np.average(sub_df['F_corrected_normed']), 4)
    sig1 = round(np.std(sub_df['F_corrected_normed']), 4)
    sig2 = 2*sig1

    fig, ax = plt.subplots()

    plt.errorbar(sub_df['DaysAsGraphite'], sub_df['F_corrected_normed'], yerr=sub_df['F_corrected_normed_error'],marker='o', color='k', label=f'Kapuni CO2', capsize=5, linestyle='')
    ax.axhline(y=av)
    ax.fill_between([0,time], av-sig1, av+sig1, alpha=.5, linewidth=0)

    ax.set_title(f"{id}_{rnum_i}, mean = {av}+/-{sig1}, QFs removed")
    ax.set_ylabel('F_corrected_normed')
    ax.set_xlabel('Days as Graphite')
    ax.set_xlim(0,time)

    plt.savefig(f"C:/Users/clewis/IdeaProjects/GNS/xcams/graphite_storage/graphite_storage_{id}_{time}_{rnum_i}.png",
                dpi=300, bbox_inches="tight")


