"""
Tree_ring_analysis.py was the first tree ring analysis and that gave me a pretty good handle on the data. I was able
to understand what we have, and the general trends. I can roughly re-create the conclusions that Rachel had. That file
does mostly data-cleaning, indexing, and plotting.

In this file, I'm going to do a little more indexing based on latitudinal and temporal bands, and hopefully compare
them with a cool plot such as a box and whisker or something else.
https://machinelearningmastery.com/time-series-data-visualization-with-python/

I could just import the dataframe from the tree_ring_analysis.py but then it has to run that file every time which is
a pain.
Instead I wrote it to an excel file which I read in.

"""
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# read in the data from the previous file that was saved to an excel file
df = pd.read_excel(
    r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\interlab_comparison\tree_ring_analysis_py.xlsx')

# break up the data into two DataFrames based on their location, and remove all data before 1980.
df = df.loc[(df['DecimalDate'] >= 1980)]  # TODO after analysis is finished, come back to time before 1980
nz = df.loc[(df['Lon'] > 100) | (df['Lon'] == -999)]  # -999 grabs the data that's in Eastbourne
chile = df.loc[(df['Lon'] < 100) & (df['Lon'] > 0)]
# Chile data still needs LONS to be changed to negative, but OK for now

# index the NZ Data based on Latitude
nz_40 = nz.loc[(nz['Lat'] >= -40)]  # check it's working: print(np.unique(nz_40.Site))
nz_40_45 = nz.loc[
    (nz['Lat'] >= -45) & (nz['Lat'] < -40) | (nz['Lat'] == -999)]  # -999's include Eastborne data in there.
nz_45_50 = nz.loc[(nz['Lat'] >= -50) & (nz['Lat'] < -45)]
nz_50_55 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50)]  # > -998 keeps this portion from grabbing the Eastborne data.
# check it works -> print(np.unique(nz_50_55.Site))

# index the Chile Data based on latitude
ch_40_45 = chile.loc[(chile['Lat'] > -45) & (chile['Lat'] <= -40)]
ch_45_50 = chile.loc[(chile['Lat'] > -50) & (chile['Lat'] <= -45)]
ch_50_56 = chile.loc[(chile['Lat'] > -56) & (chile['Lat'] <= -50)]
print(np.unique(ch_50_56.Site))

"""
Testing the linear regression idea with the new zealand data first: 
"""
A_40 = np.vstack([nz_40['DecimalDate'], np.ones(len(nz_40['DecimalDate']))]).T
m_40, c_40 = np.linalg.lstsq(A_40, nz_40['offset'], rcond=None)[0]

A_40_45 = np.vstack([nz_40_45['DecimalDate'], np.ones(len(nz_40_45['DecimalDate']))]).T
m_40_45, c_40_45 = np.linalg.lstsq(A_40_45, nz_40_45['offset'], rcond=None)[0]

A_45_50 = np.vstack([nz_45_50['DecimalDate'], np.ones(len(nz_45_50['DecimalDate']))]).T
m_45_50, c_45_50 = np.linalg.lstsq(A_45_50, nz_45_50['offset'], rcond=None)[0]

A_50_55 = np.vstack([nz_50_55['DecimalDate'], np.ones(len(nz_50_55['DecimalDate']))]).T
m_50_55, c_50_55 = np.linalg.lstsq(A_50_55, nz_50_55['offset'], rcond=None)[0]


colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10

size1 = 30
fig = plt.figure(1)
# plt.scatter(nz_40['DecimalDate'], nz_40['offset'], marker='o', label='Southern Hemisphere Harmonized Dataset',
#             color=colors2[5], s=size1, alpha=0.7)
plt.plot(nz_40['DecimalDate'], m_40 * nz_40['DecimalDate'] + c_40, label='40S', color=colors2[1], linestyle = "dotted")
plt.plot(nz_40_45['DecimalDate'], m_40_45 * nz_40_45['DecimalDate'] + c_40_45, label='40-45S', color=colors2[2], linestyle = "dashdot")
plt.plot(nz_45_50['DecimalDate'], m_45_50 * nz_45_50['DecimalDate'] + c_45_50, label='45-50S', color=colors2[3], linestyle = "dashed")
plt.plot(nz_50_55['DecimalDate'], m_50_55 * nz_50_55['DecimalDate'] + c_50_55, label='50-55S', color=colors2[4])
plt.title('Linear Fit of Tree Ring Offsets from Harmonized record over time. ')
plt.legend()
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis_NZ.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
Testing the linear regression idea with the Chile data
"""
B_40_45 = np.vstack([ch_40_45['DecimalDate'], np.ones(len(ch_40_45['DecimalDate']))]).T
n_40_45, d_40_45 = np.linalg.lstsq(B_40_45, ch_40_45['offset'], rcond=None)[0]

B_45_50 = np.vstack([ch_45_50['DecimalDate'], np.ones(len(ch_45_50['DecimalDate']))]).T
n_45_50, d_45_50 = np.linalg.lstsq(B_45_50, ch_45_50['offset'], rcond=None)[0]

B_50_56 = np.vstack([ch_50_56['DecimalDate'], np.ones(len(ch_50_56['DecimalDate']))]).T
n_50_56, d_50_56 = np.linalg.lstsq(B_50_56, ch_50_56['offset'], rcond=None)[0]

size1 = 30
fig = plt.figure(2)
# plt.scatter(nz_40['DecimalDate'], nz_40['offset'], marker='o', label='Southern Hemisphere Harmonized Dataset',
#             color=colors2[5], s=size1, alpha=0.7)
plt.plot(ch_40_45['DecimalDate'], n_40_45 * ch_40_45['DecimalDate'] + d_40_45, label='40-45S', color=colors2[2], linestyle = "dashdot")
plt.plot(ch_45_50['DecimalDate'], n_45_50 * ch_45_50['DecimalDate'] + d_45_50, label='45-50S', color=colors2[3], linestyle = "dashed")
plt.plot(ch_50_56['DecimalDate'], n_50_56 * ch_50_56['DecimalDate'] + d_50_56, label='50-56S', color=colors2[4])
plt.title('Chilean Tree Ring Offsets Linearly Regressed')
plt.legend()
# plt.xlim([1980, 2020])
# plt.ylim([0, 300])
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring_analysis2_Chilean.png',
            dpi=300, bbox_inches="tight")
plt.close()


















