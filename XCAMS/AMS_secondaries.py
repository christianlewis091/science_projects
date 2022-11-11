import pandas as pd
import numpy as np
import warnings
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PyAstronomy import pyasl
from openpyxl import Workbook

warnings.simplefilter("ignore")


"""
Want to plot the data and find the chi2 of the secondary standards from the AMS over time, and then we can see 
if we need to adjust the wheel to wheel errors. 
"""
# Define chi2 test
def cbl_chi2(data):
    # see file:///H:/Science/Current_Projects/04_ams_data_quality/AMS_stats/chi2.pdf, first page
    data['mz_num'] = data['Ratio to standard'] / data['Ratio to standard error']**2
    data['mz_denom'] = 1 / data['Ratio to standard error']**2
    data['sigma^2_mz'] = 1 / data['Ratio to standard error']**2
    Mz = (np.sum(data['mz_num'])) / (np.sum(data['mz_denom']))
    sig = 1 / (np.sum(data['mz_denom']))

    data['x_2_num'] = (data['Ratio to standard'] - Mz)**2
    data['x_2_denom'] = data['Ratio to standard error']**2

    data['x2'] = data['x_2_num'] / data['x_2_denom']
    chi2 = np.sum(data['x2'])
    chi2_red = chi2 / len(data)

    return chi2_red


"""Read in the data"""
df = pd.read_excel(r'I:\C14Data\C14_blank_corrections_dev\TW3435standards.xlsx').dropna(subset='Ratio to standard').reset_index(drop=True)
df = df.loc[(df['Quality Flag'] == '...')]  # Index: drop everything that contains a quality flag
df = df.loc[(df['wtgraph'] > 0.3)]  # Drop everything that is smaller than 0.3 mg.
names = list((df['R_number'].unique()))

"""Based on each unique sample ID, calculate summary information on each one"""
name_arr = []
average_arr = []
stddev_arr = []
count_arr = []
chi2_arr = []

with PdfPages('H:/Science/Current_Projects/04_ams_data_quality/multipage_pdf.pdf') as pdf:
    for i in range(0, len(names)):
        current_name = names[i]
        current_std = df.loc[df['R_number'] == current_name]

        count_arr.append(len(current_std))
        name_arr.append(current_name)
        average_arr.append(np.average(current_std['Ratio to standard']))
        stddev_arr.append(np.std(current_std['Ratio to standard']))

        residuals = current_std['Ratio to standard'] - np.average(current_std['Ratio to standard'])

        x = cbl_chi2(current_std)
        chi2_arr.append(x)
        plt.scatter(current_std['Job'], residuals, label='Chi^2 = {}'.format(x), color='black')
        plt.axhline(0, color='black', alpha=0.15)
        plt.title('Page One')
        pdf.savefig()  # saves the current figure into a pdf page
        plt.close()

data = pd.DataFrame({"Sample ID": name_arr, "Average": average_arr, "1-sigma": stddev_arr, "Chi2 Reduced": chi2_arr, "Count": count_arr}).sort_values("Sample ID",ascending=False).reset_index(drop=True)
data.to_excel('H:/Science/Current_Projects/04_ams_data_quality/secondariesdev.xlsx')














