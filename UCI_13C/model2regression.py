from pylr2 import regress2
import numpy as np
import pandas as pd

# # Generate a dataset
# x = np.linspace(0, 10, 100)
# e = np.random.normal(size=len(x))
# y = x + e
# # Compute regression type 2
# results = regress2(x, y, _method_type_2="reduced major axis")
# print(results)
# print(type(results))
# print(results['slope'])

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\Version3\OPEN_ACCESS_DATA_FILE_columntitleschangedforregression.xlsx')

# remove rows where data reads "LOST"
df = df.loc[df['SPE-DOC 14C'] != 'LOST'].reset_index(drop=True)

# prepare some arrays to store the data
label = []
label2 = []
depths_arr = []
slope_arr = []
intercept_arr = []
r_arr = []
std_slope = []
std_intercept = []

depths = ['Surface','Deep']
cruises = ['IO7N', 'P16N','P18']

for i in range(0, len(depths)):
    df_depth = df.loc[df['Surface/Deep'] == depths[i]]

    for j in range(0, len(cruises)):
        df_cruise = df_depth.loc[df_depth['GO-SHIP Section'] == cruises[j]]

        # grab the data I want
        x = df_cruise['SPE-DOC 13C Corrected']
        y = df_cruise['SPE-DOC 14C']

        # change it to an array format to put through the regression function
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)

        results = regress2(x, y, _method_type_2="reduced major axis")

        label.append(cruises[j])
        label2.append('SPE-DOC 13C V 14C')
        depths_arr.append(depths[i])
        slope_arr.append(results['slope'])
        intercept_arr.append(results['intercept'])
        r_arr.append(results['r'])
        std_slope.append(results['std_slope'])
        std_intercept.append(results['std_intercept'])


df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\Version3\OPEN_ACCESS_DATA_FILE_columntitleschangedforregression.xlsx',sheet_name='DOC Data')

# remove rows where data reads "LOST"
df = df.dropna(subset='corrDel14C')
df = df.dropna(subset='del13C')

# add new column with quick notation to fit my S and D notation
newcolumnarr = []
for i in range(0, len(df)):
    row = df.iloc[i]
    d = row['CTDPRS']
    if d <= 200:
        newcolumnarr.append('Surface')
    elif 2000 <= d <= 4000:
        newcolumnarr.append('Deep')
    else:
        newcolumnarr.append('Else')

df['Surface/Deep'] = newcolumnarr
# depths = ['Surface','Deep']
# cruises = ['IO7N', 'P16N','P18']

for i in range(0, len(depths)):
    df_depth = df.loc[df['Surface/Deep'] == depths[i]]

    for j in range(0, len(cruises)):
        df_cruise = df_depth.loc[df_depth['SECT_ID'] == cruises[j]]

        # grab the data I want
        x = df_cruise['del13C']
        y = df_cruise['corrDel14C']

        # change it to an array format to put through the regression function
        x = np.array(x, dtype=float)
        y = np.array(y, dtype=float)

        results = regress2(x, y, _method_type_2="reduced major axis")

        label.append(cruises[j])
        label2.append('DOC 13C V 14C')
        depths_arr.append(depths[i])
        slope_arr.append(results['slope'])
        intercept_arr.append(results['intercept'])
        r_arr.append(results['r'])
        std_slope.append(results['std_slope'])
        std_intercept.append(results['std_intercept'])


#
regressed_data = pd.DataFrame({"Label":label, "Compared":label2, "Depth": depths_arr, "Slope": slope_arr, "STD_Slope": std_slope, "Intercept": intercept_arr, "STD_Intercept": std_intercept, "R": r_arr})
regressed_data.to_excel('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Version3/regressed_data.xlsx')
#



