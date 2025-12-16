"""
AFTER FIXING UP V2 OF THE DATA, I WANT TO MAKE SURE THAT THE CTD FILENAMES LAT LON AND MY WRITTEN LAT LONS AGREE IN
ALL CASES!
"""
import pandas as pd
import numpy as np
import nzgeom.coastlines
import matplotlib.pyplot as plt

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\05_concatonate_DIC_data/DIC_JOINED_FINAL_V2_edited.xlsx', comment='#')
ctds = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2\04_concatonate_CTD_data\ctd_cat.xlsx")
filename_a = np.unique(df['FileName'])
groups = np.unique(df['helper column group'])

for i in range(0, len(filename_a)):
    dic_data = df.loc[df['FileName'] == filename_a[i]]
    ctd_data = ctds.loc[ctds['FileName'] == filename_a[i]]

    dic_lat = dic_data['Lat N'].iloc[0]
    dic_lon = dic_data['Lon E'].iloc[0]
    ctd_lat = ctd_data['latitude'].iloc[0]
    ctd_lon = ctd_data['longitude'].iloc[0]

    c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
    ax = c.plot(color="lightgray", figsize=(6,8))
    siz = 50
    ax.scatter(dic_lon, dic_lat, color='blue', marker='o', label=f'{filename_a[i]}', alpha=0.2, s=siz)
    ax.scatter(ctd_lon, ctd_lat, color='red', marker='D', alpha=0.2, s=siz)
    plt.legend()
    # plt.show()
    # Show the map
    plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/06_DataCheck/{filename_a[i]}.png", dpi=300, bbox_inches="tight")
    plt.close()

"""
Check the groups are assignmed properly
"""
for i in range(0, len(groups)):
    data = df.loc[df['helper column group'] == groups[i]]

    c =  nzgeom.coastlines.get_NZ_coastlines(bbox=(166.5, -45.8, 167.2, -45.2))
    ax = c.plot(color="lightgray", figsize=(6,8))
    siz = 50
    ax.scatter(data['Lon E'], data['Lat N'], color='blue', marker='o', label=f'{groups[i]}', alpha=0.2, s=siz)
    plt.legend()
    plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/06_DataCheck/Group_check_{groups[i]}.png", dpi=300, bbox_inches="tight")
    plt.close()