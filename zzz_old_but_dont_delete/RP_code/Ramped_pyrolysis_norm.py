import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import numpy as np
from numpy import trapz
import warnings
from X_miller_curve_algorithm import ccgFilter
warnings.filterwarnings("ignore")


df124 = pd.read_excel(r'H:\Science\Datasets\Ramped Pyrolysis\Run 124.xlsx')  # read in the Tree Ring data.
df130 = pd.read_excel(r'H:\Science\Datasets\Ramped Pyrolysis\Run 130.xlsx')  # read in the Tree Ring data.
df123 = pd.read_excel(r'H:\Science\Datasets\Ramped Pyrolysis\Run 123 R41115_2.xlsx')  # read in the Tree Ring data.

#
def remove_rp_spimes(df):
    df = df.iloc[::10]
    df['percent_change'] = df['CO2'].pct_change()
    df['percent_change'] = df['percent_change'].replace([np.inf, -np.inf], np.nan)
    # Remove rows with NaN values
    df = df.dropna()
    print(df.columns)

    df = df.loc[(df['percent_change'] < 0.002) & (df['percent_change'] > -.002)]
    return df



print(len(df124))
df124 = remove_rp_spimes(df124)
print(len(df124))
print(len(df130))
df130 = remove_rp_spimes(df130)
print(len(df130))
print(len(df123))
df123 = remove_rp_spimes(df123)
print(len(df123))

"""
2 plots horizontal
"""
fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(1, 2)
gs.update(wspace=0.1, hspace=0.35)

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 0:1])
plt.scatter(df124['Temp'], df124['percent_change'])

# plot structure
xtr_subsplot = fig.add_subplot(gs[0:1, 1:2])
plt.scatter(df124['Temp'], df124['CO2'])
plt.show()



def normalization_function(df):

    # first step is to find the total area under the curve
    y = np.array(df['CO2'])
    area = trapz(y, dx=len(df))

    # define a new array to add the new values to once they're written (the fraction of the total)
    fracs = []

    # run through the array of data and calculate fractions of total area for each line
    for i in range(0, len(df)-2):

        # grab first row plus the second (see drawing)
        rows = df.iloc[i:(i+2)]
        # change y to an array to read into trapz
        row_y = np.array(rows['CO2'])
        # calculate for area
        row_area = trapz(row_y, dx=2)

        # calculate the area relative to the total
        frac_area = row_area / area

        # append it to our list
        fracs.append(frac_area)

    df_out = df.iloc[:-2]

    df_out['Area Fraction'] = fracs
    df_out['Area Percent'] = df_out['Area Fraction']*100
    return df_out


def normalization_function_rosenheim_matlab(df):
    temp = df['Temp'] - min(df['Temp'])
    co2 = df['CO2']

    X = co2 # TODO find out what column 2 is in rosenheim's code
    DO = (X/sum(X))*(len(X)/10000)

    df_out = pd.DataFrame({"Temp": temp, "CO2_norm": DO})

    return df_out

fig = plt.figure(figsize=(16, 8))
gs = gridspec.GridSpec(2, 6)
gs.update(wspace=.75, hspace=1)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
plt.plot(df123['Temp'], df123['CO2'], label='123')
plt.plot(df124['Temp'], df124['CO2'], label='124')
plt.plot(df130['Temp'], df130['CO2'], label='130')
plt.ylabel('CO2 ppm')
plt.xlabel('Temperature (C)')
plt.legend()

# xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
# plt.title('CBL normalization using trapezoid')
# plt.plot(df_out_123['Temp'], df_out_123['Area Fraction'], label='123')
# plt.plot(df_out_124['Temp'], df_out_124['Area Fraction'], label='124')
# plt.plot(df_out_130['Temp'], df_out_130['Area Fraction'], label='130')
# plt.ylabel('Normalized CO2')
# plt.xlabel('Temperature (C)')
# plt.legend()
#
# xtr_subsplot = fig.add_subplot(gs[0:2, 4:6])
# plt.title('CBLs interpretation of Rosenheim\'s Matlab Code')
# plt.plot(df_out_123_rosen['Temp'], df_out_123_rosen['CO2_norm'], label='123')
# plt.plot(df_out_124_rosen['Temp'], df_out_124_rosen['CO2_norm'], label='124')
# plt.plot(df_out_130_rosen['Temp'], df_out_130_rosen['CO2_norm'], label='130')
# plt.ylabel('Normalized CO2')
# plt.xlabel('Temperature (C)')
# plt.legend()
plt.show()
# # plt.savefig(r'C:\Users\clewis\IdeaProjects\Ramped_Pyrolysis\norm.png', dpi=300, bbox_inches="tight")
# #
# #
# #
# #


#
df124.to_excel(r'C:\Users\clewis\IdeaProjects\Ramped_Pyrolysis\test.xlsx')
# plt.savefig(r'C:\Users\clewis\IdeaProjects\Ramped_Pyrolysis\norm.png', dpi=300, bbox_inches="tight")










# df_out_123.to_excel('C:/Users/clewis/IdeaProjects/Ramped_Pyrolysis/test.xlsx')
