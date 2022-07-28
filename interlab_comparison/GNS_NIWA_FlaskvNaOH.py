import pandas as pd
import numpy as np
from X_my_functions import long_date_to_decimal_date, intercomparison_ttest
import matplotlib.pyplot as plt
import seaborn as sns
size1 = 5
colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
seshadri = ['#c3121e', '#0348a1', '#ffb01c', '#027608', '#0193b0', '#9c5300', '#949c01', '#7104b5']

"""
For Atmospheric CO2 data collected at Baring Head, using the flask method and the NaoH method over the years, 
does the collection method make a difference in the data? Does the time between CO2 collection and extraction 
make a difference with the flask measurements? 

Also were we able to see a difference between atmospheric CO2 from Cape Grim and Baring Head during a specific period of
time in the past ( a very specific test) 
"""

ed = pd.read_excel(r'H:\The Science\Datasets\Extraction_Dates.xlsx')              # import Baring Extraction Date Data
bhd = pd.read_excel(r'H:\The Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import all Baring Head data
bhd = bhd.dropna(subset='DATE_ST').reset_index(drop = True)
bhd = bhd.dropna(subset='DATE_END').reset_index(drop = True)
ed = ed.dropna(subset='Extract').reset_index(drop = True)
x = bhd['DATE_ST']
x2 = bhd['DATE_END']
x3 = ed['Extract']
x = long_date_to_decimal_date(x)
x2 = long_date_to_decimal_date(x2)
x3 = long_date_to_decimal_date(x3)
bhd['DATE_ST_Decimal'] = x
bhd['DATE_END_Decimal'] = x2
ed['Extract_decimal'] = x3

#
ed = ed.dropna(subset=['NZ'])
ed = ed.dropna(subset=['Extract'])
combined = pd.merge(bhd, ed, on = 'NZ')                                           # merge the extraction data with the rest of the data
combined['Waiting_time'] = combined['Extract_decimal'] - combined['DEC_DECAY_CORR']

naoh = bhd.loc[(bhd['METH_COLL'] == 'NaOH_static')]                              # grab all NaOH data
flask = combined.loc[(combined['METH_COLL'] == 'Whole_air')]                          # grab all Flask data

flask_dump = []
naoh_dump = []
#
for i in range(0, len(naoh)):
    naoh_row = naoh.iloc[i]
    for k in range(0, len(flask)):
        flask_row = flask.iloc[k]

        if naoh_row['DATE_ST_Decimal'] < flask_row['DEC_DECAY_CORR'] < naoh_row['DATE_END_Decimal']:
            naoh_dump.append(naoh_row)
            flask_dump.append(flask_row)


flask_dump = pd.DataFrame(flask_dump).reset_index(drop = True)
# flask_dump.to_excel('flaskd.xlsx')
naoh_dump = pd.DataFrame(naoh_dump).reset_index(drop = True)
# naoh_dump.to_excel('naohd.xlsx')
# What is the difference between the flask and the NaOH measurements?
diff = flask_dump['DELTA14C'] - naoh_dump['DELTA14C']
diff_err = np.sqrt(flask_dump['DELTA14C_ERR']**2 + naoh_dump['DELTA14C_ERR']**2)

f = intercomparison_ttest(flask_dump['DELTA14C'], naoh_dump['DELTA14C'], 'Flask v NaOH @ Baring Head', 'paired')

plt.errorbar(naoh_dump['DEC_DECAY_CORR'], diff, label='RRL', yerr=diff_err, fmt='o', color=colors2[2], ecolor=colors2[2], elinewidth=1, capsize=2)
plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Date', fontsize=14)
plt.title('Flask - NaOH \u0394$^1$$^4$C (\u2030)')
plt.ylabel('\u0394\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/2022_Intercomparison_Paper/Flask_v_NaOH.png',
            dpi=300, bbox_inches="tight")
plt.close()

plt.errorbar(flask_dump['Waiting_time'], diff, label='RRL', yerr=diff_err, fmt='o', color=colors2[2], ecolor=colors2[2], elinewidth=1, capsize=2)
plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Time in flask before extraction (Years)', fontsize=14)
plt.title('Flask - NaOH \u0394$^1$$^4$C (\u2030)')
plt.ylabel('\u0394\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/2022_Intercomparison_Paper/Extraction_date_influence.png',
            dpi=300, bbox_inches="tight")
plt.close()

"""
The test that was done between CGO and Baring Head, how did that turn out? 
"""

df = pd.read_excel(r'H:\The Science\Datasets\CGOvBHD.xlsx')              # import Baring Extraction Date Data

f = intercomparison_ttest(df['BHD_D14C'], df['CGO_D14C'], 'CGOvBHD (Both NaOH)', 'paired')

plt.errorbar(df['Date'], df['BHD_D14C'], label='BHD', yerr=df['standard deviation1'], fmt='o', color=colors[2], ecolor=colors[2], elinewidth=1, capsize=2)
plt.errorbar(df['Date'], df['CGO_D14C'], label='CGO', yerr=df['standard deviation2'], fmt='o', color=colors2[2], ecolor=colors2[2], elinewidth=1, capsize=2)
plt.legend(fontsize=7.5)
# plt.xlim(1980, 2020)
# plt.ylim(.95, 1.3)
plt.xlabel('Date', fontsize=14)
plt.title('BHD v CGO')
plt.ylabel('\u0394$^1$$^4$C (\u2030)', fontsize=14)  # label the y axis
plt.savefig('C:/Users/clewis/IdeaProjects/GNS/radiocarbon_intercomparison/interlab_comparison/plots/2022_Intercomparison_Paper/Site_intercomparison.png',
            dpi=300, bbox_inches="tight")
plt.close()