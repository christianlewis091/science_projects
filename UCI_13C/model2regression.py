from pylr2 import regress2
import numpy as np
import pandas as pd
from scipy import stats

# ONLY CHANGED TITLES TO FIX ERROR WITH GREEK LETTERS READING INTO PANDAS!
df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\UCI_13C\output\Version3\OPEN_ACCESS_DATA_FILE_columntitleschangedforregression.xlsx')

# remove rows where data reads "LOST"
df = df.loc[df['SPE-DOC 14C'] != 'LOST'].reset_index(drop=True)
# store as new name for ttests downstream
df_spe = df

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
# storing as new name for the ttests downstream
df_doc = df
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


extra_surf = df.loc[df['Surface/Deep'] == 'Surface']
extra_deep = df.loc[df['Surface/Deep'] == 'Deep']

results = regress2(extra_surf['del13C'], extra_surf['corrDel14C'], _method_type_2="reduced major axis")

label.append(cruises[j])
label2.append('DOC 13C V 14C, all cruises!')
depths_arr.append('Surface')
slope_arr.append(results['slope'])
intercept_arr.append(results['intercept'])
r_arr.append(results['r'])
std_slope.append(results['std_slope'])
std_intercept.append(results['std_intercept'])

results = regress2(extra_deep['del13C'], extra_deep['corrDel14C'], _method_type_2="reduced major axis")

label.append(cruises[j])
label2.append('DOC 13C V 14C, all cruises!')
depths_arr.append('Deep')
slope_arr.append(results['slope'])
intercept_arr.append(results['intercept'])
r_arr.append(results['r'])
std_slope.append(results['std_slope'])
std_intercept.append(results['std_intercept'])






regressed_data = pd.DataFrame({"Label":label, "Compared":label2, "Depth": depths_arr, "Slope": slope_arr, "STD_Slope": std_slope, "Intercept": intercept_arr, "STD_Intercept": std_intercept, "R": r_arr})
regressed_data.to_excel('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Version3/regressed_data.xlsx')


"""
I lost my ttests so I'm redoing them here...

"""

comment = []
statis = []
pval = []
degrees = []

x = df_spe['SPE-DOC 13C Corrected']
y = df_doc['del13C']

a = stats.ttest_ind(x, y)
comment.append('SPE-DOC v DOC, all basins, all depths')
statis.append(a[0])
pval.append(a[1])
degrees.append(len(x)+ len(y) - 2)


depths = ['Surface','Deep']
for k in range(0, len(depths)):
    df2_doc = df_doc.loc[df_doc['Surface/Deep'] == depths[k]]
    df2_spe = df_spe.loc[df_spe['Surface/Deep'] == depths[k]]

    # y = df2_spe['del13C']
    # x = df2_doc['SPE-DOC 13C Corrected']

    cruises = ['IO7N', 'P16N','P18']

    for i in range(0, len(cruises)):
        doc = df2_doc.loc[df2_doc['SECT_ID'] == cruises[i]]
        spe = df2_spe.loc[df2_spe['GO-SHIP Section'] == cruises[i]]

        x = spe['SPE-DOC 13C Corrected']
        y = doc['del13C']

        a = stats.ttest_ind(x, y)
        comment.append(f'SPE-DOC v DOC, {cruises[i]}, {depths[k]}')
        statis.append(a[0])
        pval.append(a[1])
        degrees.append(len(x)+ len(y) - 2)


ttest_data = pd.DataFrame({"Comment": comment, "Statistic": statis, "P-value": pval, "Degrees of Freedom (n - 2)": degrees})
ttest_data.to_excel('C:/Users/clewis/IdeaProjects/GNS/UCI_13C/output/Version3/ttest_data.xlsx')























