import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyAstronomy import pyasl
from scipy.stats import chisquare
import matplotlib.gridspec as gridspec

# warnings.simplefilter("ignore")

"""
Want to plot the data and find the chi2 of the secondary standards from the AMS over time, and then we can see 
if we need to adjust the wheel to wheel errors. 
"""


def long_date_to_decimal_date(x):
    array = []  # define an empty array in which the data will be stored
    for i in range(0, len(x)):  # initialize the for loop to run the length of our dataset (x)
        j = x[i]  # assign j: grab the i'th value from our dataset (x)
        decy = pyasl.decimalYear(j)  # The heavy lifting is done via this Py-astronomy package
        decy = float(decy)  # change to a float - this may be required for appending data to the array
        array.append(decy)  # append it all together into a useful column of data
    return array  # return the new data


def cbl_chi2_v2(data):
    # see file:///H:/Science/Current_Projects/04_ams_data_quality/AMS_stats/chi2.pdf, first page
    final_lin = 'ok'

    chi2 = chisquare(data['Ratio to standard'])
    print(chi2)
    chi2 = chisquare(data['residuals'])
    print(chi2)
    print()


# read in the data
df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\alldata.xlsx').dropna(subset='Ratio to standard').reset_index(drop=True)
print(len(df))
# drop duplicate data
df = df.drop_duplicates(subset='TP', keep='first')

# get rid of empty cells
df = df.dropna(subset='AMS Submission Results Complete::Description from Sample').reset_index(drop=True)

# convert dates to decimal form and keep only everything after 2019
df['Decimal_date'] = long_date_to_decimal_date(df['Date Run'])
df = df.loc[df['Decimal_date'] > 2019]

# remove things with bad quality flags by only keepnig the good stuff, and only keep large data
df = df.loc[(df['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag
df = df.loc[(df['wtgraph'] > 0.3)]  # Drop everything that is smaller than 0.3 mg.
# list of secondaries we're intesreted in

secondaries = df.loc[df['AMS Submission Results Complete::Category Field'] == 'RRL-UNSt-LG']
names = np.unique((secondaries['Job::R']))

# for plotting an air wheel:

print(len(df))
print(names)


"""Based on each unique sample ID, calculate summary information on each one"""
with PdfPages('H:/Science/Current_Projects/04_ams_data_quality/AMS_stats/15122022.pdf') as pdf:
    name_arr = []
    average_arr = []
    stddev_arr = []
    count_arr = []
    chi2_arr = []

    for i in range(0, len(names)):
        current_name = names[i]
        print(current_name)
        current_std = df.loc[df['Job::R'] == current_name].reset_index(drop=True)
        if len(current_std) > 1:
            current_desc = current_std['AMS Submission Results Complete::Description from Sample']
            current_desc = current_desc[0]
            print(current_desc)

            # x_1 - x_bar
            x_bar = np.average(current_std['Ratio to standard'])
            x_bar_1sigma = np.std(current_std['Ratio to standard'])
            # error-weighted residual
            current_std['residuals'] = (current_std['Ratio to standard'] - x_bar) / (np.sqrt(current_std['Ratio to standard error'] ** 2 + x_bar_1sigma ** 2))

            # append some stats of this current standard to the arrays that I created above.
            count_arr.append(len(current_std))
            name_arr.append(current_name)
            average_arr.append(np.average(current_std['Ratio to standard']))
            stddev_arr.append(np.std(current_std['Ratio to standard']))

            golden_rat = 1.618
            n = 8
            fig = plt.figure(figsize=(n, (n*golden_rat)))
            gs = gridspec.GridSpec(4, 2)  # 4 spaces down, 2 spaces across
            gs.update(wspace=.5, hspace=.5)

            xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
            plt.title(f"{current_desc}, RTS Average and 1-sigma")
            plt.scatter(current_std['Decimal_date'], current_std['Ratio to standard'], color='black')
            plt.fill_between(current_std['Decimal_date'], x_bar - x_bar_1sigma, x_bar + x_bar_1sigma , alpha = 0.3, color = 'dodgerblue')
            plt.axhline(x_bar, color = 'black')

            xtr_subsplot = fig.add_subplot(gs[2:4, 0:2])
            plt.title(f"{current_desc}, Residuals (x - x_bar / sqrt(rts^2 + 1-sigma^2)")
            plt.scatter(current_std['Decimal_date'], current_std['residuals'], color='black')
            plt.fill_between(current_std['Decimal_date'], 1, -1, alpha = 0.3, color = 'dodgerblue')
            # plt.show()

            # save the plot to a PDF
            pdf.savefig()  # saves the current figure into a pdf page
            plt.close()


