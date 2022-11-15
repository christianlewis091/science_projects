import pandas as pd
import numpy as np
import warnings
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyAstronomy import pyasl

warnings.simplefilter("ignore")

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


# # Define chi2 test
# def cbl_chi2(data):
#     # see file:///H:/Science/Current_Projects/04_ams_data_quality/AMS_stats/chi2.pdf, first page
#     final_lin = 'ok'
#     data['mz_num'] = data['Ratio to standard'] / data['Ratio to standard error'] ** 2
#     data['mz_denom'] = 1 / data['Ratio to standard error'] ** 2
#     data['sigma^2_mz'] = 1 / data['Ratio to standard error'] ** 2
#     Mz = (np.sum(data['mz_num'])) / (np.sum(data['mz_denom']))
#     sig = 1 / (np.sum(data['mz_denom']))
#
#     data['x_2_num'] = (data['Ratio to standard'] - Mz) ** 2
#     data['x_2_denom'] = data['Ratio to standard error'] ** 2
#
#     data['x2'] = data['x_2_num'] / data['x_2_denom']
#     chi2 = np.sum(data['x2'])
#     chi2_red = chi2 / len(data)
#     # print(chi2_red)
#     if chi2_red > 1:
#         lins = np.linspace(0, 100, 1000)
#         for j in range(0, len(lins)):
#             lin = lins[j]
#             data['denom_adjusted'] = (data['Ratio to standard error']*(1+lin)) ** 2
#             data['x2_adjusted'] = data['x_2_num'] / data['denom_adjusted']
#             chi2_adjusted = np.sum(data['x2_adjusted'])
#             chi2_red_adjusted = chi2_adjusted / len(data)
#             if chi2_red_adjusted < 1:
#                 final_lin = lin*100
#                 break
#
#     return chi2_red, final_lin

# Define chi2 test
def cbl_chi2_v2(data):
    # see file:///H:/Science/Current_Projects/04_ams_data_quality/AMS_stats/chi2.pdf, first page
    final_lin = 'ok'
    average = np.average(data['residuals'])
    data['chi2'] = ((data['residuals'] - average) ** 2) / (data['residuals_error'] **2)
    chi2_red = np.sum(data['chi2']) / (len(data) - 1)

    # print(chi2_red)
    if chi2_red > 1:
        lins = np.linspace(0, 100, 1000)
        for j in range(0, len(lins)):
            lin = lins[j]
            data['chi2_adjusted'] = ((data['residuals'] - average) ** 2) / ((data['residuals_error']*(1+lin)) **2)
            chi2_red_adjusted = np.sum(data['chi2_adjusted']) / (len(data) - 1)
            if chi2_red_adjusted < 1:
                final_lin = lin*100
                break

    return chi2_red, final_lin




"""Read in the data"""
df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\alldata.xlsx').dropna(subset='Ratio to standard').reset_index(drop=True)
df = df.drop_duplicates(subset='TP', keep='first')
df = df.dropna(subset='AMS Submission Results Complete::Description from Sample').reset_index(drop=True)
df['Decimal_date'] = long_date_to_decimal_date(df['Date Run'])
df = df.loc[df['Decimal_date'] > 2019]

df = df.loc[(df['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag
df = df.loc[(df['wtgraph'] > 0.3)]  # Drop everything that is smaller than 0.3 mg.
# list of secondaries we're intesreted in

secondaries = df.loc[df['AMS Submission Results Complete::Category Field'] == 'RRL-UNSt-LG']
names = np.unique((secondaries['Job::R']))
# print(names)

# names = ['41347/2', '40430/1', '40430/2','24889/4']
# descrips = ['LAC1 Coral', 'BHD ambient air', 'BHD air spiked with 10% dead CO2','Firi-D Wood']


"""Based on each unique sample ID, calculate summary information on each one"""

name_arr = []
average_arr = []
stddev_arr = []
count_arr = []
chi2_arr = []
with PdfPages('H:/Science/Current_Projects/04_ams_data_quality/multipage_pdf_v1.pdf') as pdf:
    for i in range(0, len(names)):
        current_name = names[i]
        current_std = df.loc[df['Job::R'] == current_name].reset_index(drop=True)
        if len(current_std) > 1:
            current_desc = current_std['AMS Submission Results Complete::Description from Sample']
            current_desc = current_desc[0]

            # append some stats of this current standard to the arrays that I created above.
            count_arr.append(len(current_std))
            name_arr.append(current_name)
            average_arr.append(np.average(current_std['Ratio to standard']))
            stddev_arr.append(np.std(current_std['Ratio to standard']))


            # make the plot
            current_std['residuals'] = current_std['Ratio to standard'] - np.average(current_std['Ratio to standard'])
            current_std['residuals_error'] = np.sqrt(current_std['Ratio to standard error']**2 + np.std(current_std['Ratio to standard'])**2)
            x = cbl_chi2_v2(current_std)
            chi2_arr.append(x[0])

            plt.scatter(current_std['Decimal_date'], current_std['residuals'], label='Chi^2 = {}'.format(x), color='black')
            plt.axhline(0, color='black', alpha=0.15)
            plt.ylim(1.10*(min(current_std['residuals'])), 1.10*(max(current_std['residuals'])))

            # make the plot a bit more helpful to see...
            plt.text(min(current_std['Decimal_date']), max(current_std['residuals']), "Chi2 = {}".format(round(x[0], 2)), fontsize=12, backgroundcolor='lightsteelblue', color='red')
            if x[1] != 'ok':
                plt.text(min(current_std['Decimal_date']), 0.8*max(current_std['residuals']), "Error adjustment required: {} %".format(round(x[1], 3)), fontsize=12, backgroundcolor='lightsteelblue')
            plt.title('{}: {}'.format(current_name, current_desc))
            pdf.attach_note("plot of sin(x)")
            # save the plot to a PDF
            pdf.savefig()  # saves the current figure into a pdf page
            plt.close()


data = pd.DataFrame({"Sample ID": name_arr, "Average": average_arr, "1-sigma": stddev_arr, "Chi2 Reduced": chi2_arr,
                     "Count": count_arr}).sort_values("Sample ID", ascending=False).reset_index(drop=True)
data.to_excel('H:/Science/Current_Projects/04_ams_data_quality/secondariesdev.xlsx')





# # Where are all the duplicates in the database?
# df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\alldata.xlsx').dropna(subset='TP').reset_index(drop=True)
# df = pd.concat(g for _, g in df.groupby("TP") if len(g) > 1)
# df.to_excel(r'H:\Science\Current_Projects\04_ams_data_quality\dups.xlsx')

# # finding out where to flag
# df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\alldata.xlsx').dropna(subset='Ratio to standard').reset_index(drop=True)
# df = df.drop_duplicates(subset='TP', keep='first')
# df = df.loc[(df['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag
# df = df.loc[(df['wtgraph'] > 0.3)]  # Drop everything that is smaller than 0.3 mg.
# df = df.loc[df['Job::R'] == '40696/2']
# df['residuals'] = df['Ratio to standard'] - np.average(df['Ratio to standard'])
#
#
# df = df.loc[df['residuals'] < -.01]
# print(df['TP'])
