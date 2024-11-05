"""
Quick final comparison of MCQ, Cambpell Island, Neumauyer
"""

import pandas as pd
from X_my_functions import monte_carlo_randomization_trend

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/samples_with_references10000.xlsx')
cmp = df.loc[df['Site'] == 'Campbell Island, NZ']
mcq = pd.read_excel('H:/Science/Datasets/heidelberg_MQA.xlsx')
nmy = pd.read_excel('H:/Science/Datasets/heidelberg_neumayer.xlsx', sheet_name='DataOnly')

cmp = cmp[['DecimalDate','∆14C']]
nmy = nmy[['DecimalDate','D14C']]
mcq = mcq[['Average of Dates','D14C']]

cmp['Site'] = 'Campbell'
nmy['Site'] = 'Neumayer'
mcq['Site'] = 'Mac'

cmp = cmp.rename(columns={'∆14C':'Delta14C'})
nmy = nmy.rename(columns={'D14C':'Delta14C'})
mcq = mcq.rename(columns={'D14C':'Delta14C', 'Average of Dates': 'DecimalDate'})


def convert_to_decimal_date(date_series):
    """
    Converts a pandas Series of datetime objects to a Series of decimal dates.

    Parameters:
    date_series (pd.Series): Series of datetime objects

    Returns:
    pd.Series: Series of decimal dates
    """
    # Function to convert a single datetime object to decimal date
    def to_decimal_date(dt):
        # Number of days passed in the year (Julian day) - 1
        day_of_year = float(dt.strftime("%j")) - 1
        # Number of days in the year (considering leap year)
        days_in_year = 366 if dt.year % 4 == 0 and (dt.year % 100 != 0 or dt.year % 400 == 0) else 365
        # Calculate the decimal date
        return dt.year + day_of_year / days_in_year

    # Apply the conversion function to the pandas Series
    return date_series.apply(to_decimal_date)

# Example usage:
# Assuming you have a pandas Series of datetime objects
# dates = pd.Series(pd.to_datetime(["1992-12-12 00:00:00", "2007-04-14 11:42:50"]))
# print(mcq['DecimalDate'])
mcq['DecimalDate'] = convert_to_decimal_date(mcq['DecimalDate'])
nmy['DecimalDate'] = convert_to_decimal_date(nmy['DecimalDate'])

df = pd.concat([cmp, nmy, mcq])
output_xvals = df['DecimalDate'].sort_values()
print(df)

# MOST OF THIS IS COPIED FROM "REFERENCE TO SAMPLE XVALS.py:
ref3 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference1/reference1.xlsx')

n = 10  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff

# output the reference at the X-values that match the data
reference3_trend = monte_carlo_randomization_trend(ref3['Decimal_date'], output_xvals, ref3['D14C'], ref3['weightedstderr_D14C'], cutoff, n)
reference3_trend = reference3_trend[2]

montes = pd.DataFrame({'Decimal_date': output_xvals,
                       'D14C_ref3t_mean': reference3_trend['Means'], 'D14C_ref3t_std': reference3_trend['stdevs']}).drop_duplicates(subset='Decimal_date')

# BELOW IS COPIED FROM REFRENCE TO SAMPLE XVALS2.py
D14C_ref3t_mean = []  # initialize an empty array
D14C_ref3t_std = []  # initialize an empty array

for i in range(0, len(df)):
    samples_row = df.iloc[i]
    sample_date = samples_row['DecimalDate']

    for k in range(0, len(montes)):
        df_row = montes.iloc[k]
        df_date = df_row['Decimal_date']

        if sample_date == df_date:
            D14C_ref3t_mean.append(df_row['D14C_ref3t_mean'])
            D14C_ref3t_std.append(df_row['D14C_ref3t_std'])

df['D14C_ref3t_mean'] = D14C_ref3t_mean
df['D14C_ref3t_std'] = D14C_ref3t_std

df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/nmy_mcq_cmp_comparison.xlsx')






















