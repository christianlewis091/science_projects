"""
Trying to simplify Tree_ring_analysis2

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

# indexing the data according to the matrix in my DataScience Notebook:
nz_a1 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]  # North of 40S, 1980 - 1990
nz_a2 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]  # North of 40S, 1990 - 2000
nz_a3 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]  # etc...
nz_a4 = nz.loc[(nz['Lat'] >= -40) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

nz_b1 = nz.loc[(nz['Lat'] >= -45) & (nz['Lat'] < -40) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]
nz_b2 = nz.loc[(nz['Lat'] >= -45) & (nz['Lat'] < -40) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
nz_b3 = nz.loc[(nz['Lat'] >= -45) & (nz['Lat'] < -40) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
nz_b4 = nz.loc[(nz['Lat'] >= -45) & (nz['Lat'] < -40) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

nz_c1 = nz.loc[(nz['Lat'] >= -50) & (nz['Lat'] < -45) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]
nz_c2 = nz.loc[(nz['Lat'] >= -50) & (nz['Lat'] < -45) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
nz_c3 = nz.loc[(nz['Lat'] >= -50) & (nz['Lat'] < -45) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
nz_c4 = nz.loc[(nz['Lat'] >= -50) & (nz['Lat'] < -45) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

nz_d1 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 1980) & (nz['DecimalDate'] < 1990)]  # > -998 keeps this portion from grabbing the Eastborne data set at -999.
nz_d2 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 1990) & (nz['DecimalDate'] < 2000)]
nz_d3 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 2000) & (nz['DecimalDate'] < 2010)]
nz_d4 = nz.loc[(nz['Lat'] > -998) & (nz['Lat'] < -50) & (nz['DecimalDate'] >= 2010) & (nz['DecimalDate'] < 2020)]

"""
Perform the linear regression for each time period and latitude range: 

https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html
"""
A_nz_a1 = np.vstack([nz_a1['DecimalDate'], np.ones(len(nz_a1['DecimalDate']))]).T
A_nz_a2 = np.vstack([nz_a2['DecimalDate'], np.ones(len(nz_a2['DecimalDate']))]).T
A_nz_a3 = np.vstack([nz_a3['DecimalDate'], np.ones(len(nz_a3['DecimalDate']))]).T
A_nz_a4 = np.vstack([nz_a4['DecimalDate'], np.ones(len(nz_a4['DecimalDate']))]).T

A_nz_b1 = np.vstack([nz_b1['DecimalDate'], np.ones(len(nz_b1['DecimalDate']))]).T
A_nz_b2 = np.vstack([nz_b2['DecimalDate'], np.ones(len(nz_b2['DecimalDate']))]).T
A_nz_b3 = np.vstack([nz_b3['DecimalDate'], np.ones(len(nz_b3['DecimalDate']))]).T
A_nz_b4 = np.vstack([nz_b4['DecimalDate'], np.ones(len(nz_b4['DecimalDate']))]).T

A_nz_c1 = np.vstack([nz_c1['DecimalDate'], np.ones(len(nz_c1['DecimalDate']))]).T
A_nz_c2 = np.vstack([nz_c2['DecimalDate'], np.ones(len(nz_c2['DecimalDate']))]).T
A_nz_c3 = np.vstack([nz_c3['DecimalDate'], np.ones(len(nz_c3['DecimalDate']))]).T
A_nz_c4 = np.vstack([nz_c4['DecimalDate'], np.ones(len(nz_c4['DecimalDate']))]).T

A_nz_d1 = np.vstack([nz_d1['DecimalDate'], np.ones(len(nz_d1['DecimalDate']))]).T
A_nz_d2 = np.vstack([nz_d2['DecimalDate'], np.ones(len(nz_d2['DecimalDate']))]).T
A_nz_d3 = np.vstack([nz_d3['DecimalDate'], np.ones(len(nz_d3['DecimalDate']))]).T
A_nz_d4 = np.vstack([nz_d4['DecimalDate'], np.ones(len(nz_d4['DecimalDate']))]).T

m_a1, c_a1 = np.linalg.lstsq(A_nz_a1, nz_a1['offset'], rcond=None)[0]
m_a2, c_a2 = np.linalg.lstsq(A_nz_a2, nz_a2['offset'], rcond=None)[0]
m_a3, c_a3 = np.linalg.lstsq(A_nz_a3, nz_a3['offset'], rcond=None)[0]
m_a4, c_a4 = np.linalg.lstsq(A_nz_a4, nz_a4['offset'], rcond=None)[0]

m_b1, c_b1 = np.linalg.lstsq(A_nz_b1, nz_b1['offset'], rcond=None)[0]
m_b2, c_b2 = np.linalg.lstsq(A_nz_b2, nz_b2['offset'], rcond=None)[0]
m_b3, c_b3 = np.linalg.lstsq(A_nz_b3, nz_b3['offset'], rcond=None)[0]
m_b4, c_b4 = np.linalg.lstsq(A_nz_b4, nz_b4['offset'], rcond=None)[0]

m_c1, c_c1 = np.linalg.lstsq(A_nz_c1, nz_c1['offset'], rcond=None)[0]
m_c2, c_c2 = np.linalg.lstsq(A_nz_c2, nz_c2['offset'], rcond=None)[0]
m_c3, c_c3 = np.linalg.lstsq(A_nz_c3, nz_c3['offset'], rcond=None)[0]
m_c4, c_c4 = np.linalg.lstsq(A_nz_c4, nz_c4['offset'], rcond=None)[0]

m_d1, c_d1 = np.linalg.lstsq(A_nz_d1, nz_d1['offset'], rcond=None)[0]
m_d2, c_d2 = np.linalg.lstsq(A_nz_d2, nz_d2['offset'], rcond=None)[0]
m_d3, c_d3 = np.linalg.lstsq(A_nz_d3, nz_d3['offset'], rcond=None)[0]
m_d4, c_d4 = np.linalg.lstsq(A_nz_d4, nz_d4['offset'], rcond=None)[0]


"""
Testing the Figure
"""
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
a = 0.15
size1 = 15
fig = plt.figure(2)
plt.plot(nz_a1['DecimalDate'], m_a1*nz_a1['DecimalDate'] + c_a1, label='North of 40S', color='black', linestyle = "dashdot")
plt.plot(nz_a2['DecimalDate'], m_a2*nz_a2['DecimalDate'] + c_a2, color='black', linestyle = "dashdot")
plt.plot(nz_a3['DecimalDate'], m_a3*nz_a3['DecimalDate'] + c_a3, color='black', linestyle = "dashdot")
plt.plot(nz_a4['DecimalDate'], m_a4*nz_a4['DecimalDate'] + c_a4, color='black', linestyle = "dashdot")

plt.scatter(nz_a1['DecimalDate'], nz_a1['offset'], alpha = a, color='black', s = size1)
plt.scatter(nz_a2['DecimalDate'], nz_a2['offset'], alpha = a, color='black', s = size1)
plt.scatter(nz_a3['DecimalDate'], nz_a3['offset'], alpha = a, color='black', s = size1)
plt.scatter(nz_a4['DecimalDate'], nz_a4['offset'], alpha = a, color='black', s = size1)

# TODO fix the B part of the matrix - doesn't seem to be indexing properly.
plt.plot(nz_b1['DecimalDate'], m_b1*nz_b1['DecimalDate'] + c_b1, label='40-45S', color=colors[1], linestyle = "dotted")
plt.plot(nz_b2['DecimalDate'], m_b2*nz_b2['DecimalDate'] + c_b2, color=colors[1], linestyle = "dotted")
plt.plot(nz_b3['DecimalDate'], m_b3*nz_b3['DecimalDate'] + c_b3, color=colors[1], linestyle = "dotted")
plt.plot(nz_b4['DecimalDate'], m_b4*nz_b4['DecimalDate'] + c_b4, color=colors[1], linestyle = "dotted")

plt.scatter(nz_b1['DecimalDate'], nz_b1['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(nz_b2['DecimalDate'], nz_b2['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(nz_b3['DecimalDate'], nz_b3['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(nz_b4['DecimalDate'], nz_b4['offset'], alpha = a, color=colors[1], s = size1)


plt.plot(nz_c1['DecimalDate'], m_c1*nz_c1['DecimalDate'] + c_c1, label='45-50S', color=colors2[1], linestyle = "dashed")
plt.plot(nz_c2['DecimalDate'], m_c2*nz_c2['DecimalDate'] + c_c2, color=colors2[1], linestyle = "dashed")
plt.plot(nz_c3['DecimalDate'], m_c3*nz_c3['DecimalDate'] + c_c3, color=colors2[1], linestyle = "dashed")
plt.plot(nz_c4['DecimalDate'], m_c4*nz_c4['DecimalDate'] + c_c4,  color=colors2[1], linestyle = "dashed")

plt.scatter(nz_c1['DecimalDate'], nz_c1['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(nz_c2['DecimalDate'], nz_c2['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(nz_c3['DecimalDate'], nz_c3['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(nz_c4['DecimalDate'], nz_c4['offset'], alpha = a, color=colors2[1], s = size1)

plt.plot(nz_d1['DecimalDate'], m_d1*nz_d1['DecimalDate'] + c_d1, label='50-55S', color=colors[5], linestyle = "solid")
plt.plot(nz_d2['DecimalDate'], m_d2*nz_d2['DecimalDate'] + c_d2, color=colors[5], linestyle = "solid")
plt.plot(nz_d3['DecimalDate'], m_d3*nz_d3['DecimalDate'] + c_d3, color=colors[5], linestyle = "solid")
plt.plot(nz_d4['DecimalDate'], m_d4*nz_d4['DecimalDate'] + c_d4, color=colors[5], linestyle = "solid")

plt.scatter(nz_d1['DecimalDate'], nz_d1['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(nz_d2['DecimalDate'], nz_d2['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(nz_d3['DecimalDate'], nz_d3['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(nz_d4['DecimalDate'], nz_d4['offset'], alpha = a, color=colors[5], s = size1)
plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
plt.xlim([1980, 2020])
plt.ylim([-15, 10])
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring2_dev.png',
            dpi=300, bbox_inches="tight")
plt.close()



"""
Trying to do the same as above for the Chile data
"""

chile_a1 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]  # North of 40S, 1980 - 1990
chile_a2 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]  # North of 40S, 1990 - 2000
chile_a3 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]  # etc...
chile_a4 = chile.loc[(chile['Lat'] >= -40) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

chile_b1 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]
chile_b2 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
chile_b3 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
chile_b4 = chile.loc[(chile['Lat'] >= -45) & (chile['Lat'] < -40) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

chile_c1 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]
chile_c2 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
chile_c3 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
chile_c4 = chile.loc[(chile['Lat'] >= -50) & (chile['Lat'] < -45) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

chile_d1 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 1980) & (chile['DecimalDate'] < 1990)]  # > -998 keeps this portion from grabbing the Eastborne data set at -999.
chile_d2 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 1990) & (chile['DecimalDate'] < 2000)]
chile_d3 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 2000) & (chile['DecimalDate'] < 2010)]
chile_d4 = chile.loc[(chile['Lat'] > -998) & (chile['Lat'] < -50) & (chile['DecimalDate'] >= 2010) & (chile['DecimalDate'] < 2020)]

A_chile_a1 = np.vstack([chile_a1['DecimalDate'], np.ones(len(chile_a1['DecimalDate']))]).T
A_chile_a2 = np.vstack([chile_a2['DecimalDate'], np.ones(len(chile_a2['DecimalDate']))]).T
A_chile_a3 = np.vstack([chile_a3['DecimalDate'], np.ones(len(chile_a3['DecimalDate']))]).T
A_chile_a4 = np.vstack([chile_a4['DecimalDate'], np.ones(len(chile_a4['DecimalDate']))]).T

A_chile_b1 = np.vstack([chile_b1['DecimalDate'], np.ones(len(chile_b1['DecimalDate']))]).T
A_chile_b2 = np.vstack([chile_b2['DecimalDate'], np.ones(len(chile_b2['DecimalDate']))]).T
A_chile_b3 = np.vstack([chile_b3['DecimalDate'], np.ones(len(chile_b3['DecimalDate']))]).T
A_chile_b4 = np.vstack([chile_b4['DecimalDate'], np.ones(len(chile_b4['DecimalDate']))]).T

A_chile_c1 = np.vstack([chile_c1['DecimalDate'], np.ones(len(chile_c1['DecimalDate']))]).T
A_chile_c2 = np.vstack([chile_c2['DecimalDate'], np.ones(len(chile_c2['DecimalDate']))]).T
A_chile_c3 = np.vstack([chile_c3['DecimalDate'], np.ones(len(chile_c3['DecimalDate']))]).T
A_chile_c4 = np.vstack([chile_c4['DecimalDate'], np.ones(len(chile_c4['DecimalDate']))]).T

A_chile_d1 = np.vstack([chile_d1['DecimalDate'], np.ones(len(chile_d1['DecimalDate']))]).T
A_chile_d2 = np.vstack([chile_d2['DecimalDate'], np.ones(len(chile_d2['DecimalDate']))]).T
A_chile_d3 = np.vstack([chile_d3['DecimalDate'], np.ones(len(chile_d3['DecimalDate']))]).T
A_chile_d4 = np.vstack([chile_d4['DecimalDate'], np.ones(len(chile_d4['DecimalDate']))]).T

m_a1, c_a1 = np.linalg.lstsq(A_chile_a1, chile_a1['offset'], rcond=None)[0]
m_a2, c_a2 = np.linalg.lstsq(A_chile_a2, chile_a2['offset'], rcond=None)[0]
m_a3, c_a3 = np.linalg.lstsq(A_chile_a3, chile_a3['offset'], rcond=None)[0]
m_a4, c_a4 = np.linalg.lstsq(A_chile_a4, chile_a4['offset'], rcond=None)[0]

m_b1, c_b1 = np.linalg.lstsq(A_chile_b1, chile_b1['offset'], rcond=None)[0]
m_b2, c_b2 = np.linalg.lstsq(A_chile_b2, chile_b2['offset'], rcond=None)[0]
m_b3, c_b3 = np.linalg.lstsq(A_chile_b3, chile_b3['offset'], rcond=None)[0]
m_b4, c_b4 = np.linalg.lstsq(A_chile_b4, chile_b4['offset'], rcond=None)[0]

m_c1, c_c1 = np.linalg.lstsq(A_chile_c1, chile_c1['offset'], rcond=None)[0]
m_c2, c_c2 = np.linalg.lstsq(A_chile_c2, chile_c2['offset'], rcond=None)[0]
m_c3, c_c3 = np.linalg.lstsq(A_chile_c3, chile_c3['offset'], rcond=None)[0]
m_c4, c_c4 = np.linalg.lstsq(A_chile_c4, chile_c4['offset'], rcond=None)[0]

m_d1, c_d1 = np.linalg.lstsq(A_chile_d1, chile_d1['offset'], rcond=None)[0]
m_d2, c_d2 = np.linalg.lstsq(A_chile_d2, chile_d2['offset'], rcond=None)[0]
m_d3, c_d3 = np.linalg.lstsq(A_chile_d3, chile_d3['offset'], rcond=None)[0]
m_d4, c_d4 = np.linalg.lstsq(A_chile_d4, chile_d4['offset'], rcond=None)[0]

"""
Testing the Figure
"""
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
a = 0.15
size1 = 15
fig = plt.figure(3)
plt.plot(chile_a1['DecimalDate'], m_a1*chile_a1['DecimalDate'] + c_a1, label='North of 40S', color='black', linestyle = "dashdot")
plt.plot(chile_a2['DecimalDate'], m_a2*chile_a2['DecimalDate'] + c_a2, color='black', linestyle = "dashdot")
plt.plot(chile_a3['DecimalDate'], m_a3*chile_a3['DecimalDate'] + c_a3, color='black', linestyle = "dashdot")
plt.plot(chile_a4['DecimalDate'], m_a4*chile_a4['DecimalDate'] + c_a4, color='black', linestyle = "dashdot")

plt.scatter(chile_a1['DecimalDate'], chile_a1['offset'], alpha = a, color='black', s = size1)
plt.scatter(chile_a2['DecimalDate'], chile_a2['offset'], alpha = a, color='black', s = size1)
plt.scatter(chile_a3['DecimalDate'], chile_a3['offset'], alpha = a, color='black', s = size1)
plt.scatter(chile_a4['DecimalDate'], chile_a4['offset'], alpha = a, color='black', s = size1)

plt.plot(chile_b1['DecimalDate'], m_b1*chile_b1['DecimalDate'] + c_b1, label='40-45S', color=colors[1], linestyle = "dotted")
plt.plot(chile_b2['DecimalDate'], m_b2*chile_b2['DecimalDate'] + c_b2, color=colors[1], linestyle = "dotted")
plt.plot(chile_b3['DecimalDate'], m_b3*chile_b3['DecimalDate'] + c_b3, color=colors[1], linestyle = "dotted")
plt.plot(chile_b4['DecimalDate'], m_b4*chile_b4['DecimalDate'] + c_b4, color=colors[1], linestyle = "dotted")

plt.scatter(chile_b1['DecimalDate'], chile_b1['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(chile_b2['DecimalDate'], chile_b2['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(chile_b3['DecimalDate'], chile_b3['offset'], alpha = a, color=colors[1], s = size1)
plt.scatter(chile_b4['DecimalDate'], chile_b4['offset'], alpha = a, color=colors[1], s = size1)


plt.plot(chile_c1['DecimalDate'], m_c1*chile_c1['DecimalDate'] + c_c1, label='45-50S', color=colors2[1], linestyle = "dashed")
plt.plot(chile_c2['DecimalDate'], m_c2*chile_c2['DecimalDate'] + c_c2, color=colors2[1], linestyle = "dashed")
plt.plot(chile_c3['DecimalDate'], m_c3*chile_c3['DecimalDate'] + c_c3, color=colors2[1], linestyle = "dashed")
plt.plot(chile_c4['DecimalDate'], m_c4*chile_c4['DecimalDate'] + c_c4,  color=colors2[1], linestyle = "dashed")

plt.scatter(chile_c1['DecimalDate'], chile_c1['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(chile_c2['DecimalDate'], chile_c2['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(chile_c3['DecimalDate'], chile_c3['offset'], alpha = a, color=colors2[1], s = size1)
plt.scatter(chile_c4['DecimalDate'], chile_c4['offset'], alpha = a, color=colors2[1], s = size1)

plt.plot(chile_d1['DecimalDate'], m_d1*chile_d1['DecimalDate'] + c_d1, label='50-55S', color=colors[5], linestyle = "solid")
plt.plot(chile_d2['DecimalDate'], m_d2*chile_d2['DecimalDate'] + c_d2, color=colors[5], linestyle = "solid")
plt.plot(chile_d3['DecimalDate'], m_d3*chile_d3['DecimalDate'] + c_d3, color=colors[5], linestyle = "solid")
plt.plot(chile_d4['DecimalDate'], m_d4*chile_d4['DecimalDate'] + c_d4, color=colors[5], linestyle = "solid")

plt.scatter(chile_d1['DecimalDate'], chile_d1['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(chile_d2['DecimalDate'], chile_d2['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(chile_d3['DecimalDate'], chile_d3['offset'], alpha = a, color=colors[5], s = size1)
plt.scatter(chile_d4['DecimalDate'], chile_d4['offset'], alpha = a, color=colors[5], s = size1)
plt.axhline(y=0, color='black', linestyle='-', alpha = 0.15)
# plt.xlim([1980, 2020])
# plt.ylim([-15, 10])
plt.legend()
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/Tree_ring2_dev_CHILE.png',
            dpi=300, bbox_inches="tight")
plt.close()












