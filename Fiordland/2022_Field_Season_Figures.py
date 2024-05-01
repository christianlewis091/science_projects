import pandas as pd
import matplotlib.gridspec as gridspec
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('H:/Science/Datasets/Fiordland/Past_Field_Season_Data/2022_CTD_DATAMERGE_LEWIS.xlsx').dropna(subset='DepSM')

# for each location / sound
locations = np.unique(df['ctdSampleLocation'])

# loop through and create plots
for k in range(0, len(locations)):

    location1 = df.loc[df['ctdSampleLocation'] == locations[k]].sort_values(by=['DepSM'])
    # grab each station within the "sound" subloop
    stations = np.unique(location1['fileName'])  # each filename comes from a differnet CTD cast

    # add each of those stations onto a plot
    for i in range(0, len(stations)):
        stn1 = location1.loc[location1['fileName'] == stations[i]].sort_values(by=['DepSM'])

        # extract the variables
        depth = stn1['DepSM']
        temp = stn1['DepSM']
        sal = stn1['Sal00']
        flour = stn1['WetStar']
        pottemp = stn1['Potemp090C']
        density = stn1['Sigma-é00']
        max_depth = max(depth)
        # extract lat lons for the map
        lat = np.unique(stn1['latitude'])
        lon = np.unique(stn1['longitude'])

        # stn1 = stn1.iloc[::25]  # data is very dense
        plt.plot(pottemp, depth)
        plt.title(f'{locations[k]}')
    plt.ylim(max_depth, 0)
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_Field_Season_Figures/{locations[k]}_new',
                dpi=300, bbox_inches="tight")
    plt.close()

fig = plt.figure(figsize=(15,5))
gs = gridspec.GridSpec(3, 5)
gs.update(wspace=0.5, hspace=0.5)

xtr_subsplot = fig.add_subplot(gs[0:3, 0:2])

xtr_subsplot = fig.add_subplot(gs[0:1, 2:3])

xtr_subsplot = fig.add_subplot(gs[1:3, 2:3])

xtr_subsplot = fig.add_subplot(gs[0:1, 3:4])

xtr_subsplot = fig.add_subplot(gs[1:3, 3:4])

xtr_subsplot = fig.add_subplot(gs[0:1, 4:5])

xtr_subsplot = fig.add_subplot(gs[1:3, 4:5])


plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Fiordland/OUTPUT/2022_Field_Season_Figures/template.png',
            dpi=300, bbox_inches="tight")





























