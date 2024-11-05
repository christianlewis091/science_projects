import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec

easy_access = pd.read_excel(r'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/hysplit/output_data/easy_access2_extramaps.xlsx')
for i in range(0, len(easy_access)):
    row = easy_access.iloc[i]
    codename = row['Codename']
    y = row['NewLat']
    x = row['ChileFixLon']
    pltname = row['Site']
    fig = plt.figure(figsize=(16, 8))
    gs = gridspec.GridSpec(1, 2)
    gs.update(wspace=0.1, hspace=0.35)

    xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
    m = Basemap(llcrnrlat=y-10, urcrnrlat=y+10, llcrnrlon=x-10, urcrnrlon=x+10, resolution='i')
    x, y = m(x, y)
    m.scatter(x, y,  marker='*', color='yellow', s=180, edgecolor='black', alpha=1)
    m.shadedrelief()
    m.drawcoastlines()
    plt.title(f'{pltname}')
    m.drawparallels(np.arange(-90, 90, 2.5), labels=[True, False, False, False], linewidth=0.5)
    m.drawmeridians(np.arange(-180, 180, 2.5), labels=[1, 1, 0, 1], linewidth=0.5)

    xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
    m = Basemap(llcrnrlat=y-2.5, urcrnrlat=y+2.5, llcrnrlon=x-2.5, urcrnrlon=x+2.5, resolution='i')
    x, y = m(x, y)
    m.scatter(x, y,  marker='*', color='yellow', s=180, edgecolor='black', alpha=1)
    m.shadedrelief()
    m.drawcoastlines()
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/supp_info_xtraplots/SuppInfo_{codename}.png',
                dpi=300, bbox_inches="tight")
    plt.close()