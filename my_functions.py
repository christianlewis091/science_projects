import numpy as np
from PyAstronomy import pyasl
import pandas as pd
from numpy.fft import fft, ifft
from tabulate import tabulate
import random
from miller_curve_algorithm import ccgFilter
# dfx = pd.read_excel(
#     r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Stats and Data Analysis\Matlab and Python Files\tables.xlsx',
#     sheet_name='t table', skiprows=6)
# dfx = dfx.reset_index()
# t_table_05 = dfx[0.05]
# x = random.sample(range(10, 500), 150) # for testing
# x2 = random.sample(range(400, 1000), 600) # for testing

"""
In the Miller code, it getMonthlymeans returns a column of years, and a column of
months, and I need a way to get decimal dates out of it for plotting. This code does that.
you need:
x = year data
y = month data
"""

x = [1, 2, 4]
y = [1, 5, 15]


def year_month_todecimaldate(x, y):
    L = np.linspace(0, 1, 365)
    # add the number that is 1/2 of the previous month plus the current month
    Jan = 31
    Feb = (28 / 2) + 31
    Mar = (31 / 2) + 31 + 28
    Apr = (30 / 2) + 31 + 28 + 31
    May = (31 / 2) + 31 + 28 + 31 + 30
    June = (30 / 2) + 31 + 28 + 31 + 30 + 31
    July = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30
    August = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31
    Sep = (30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31
    Oct = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30
    Nov = (30 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30
    Dec = (31 / 2) + 31 + 28 + 31 + 30 + 31 + 30 + 31 + 31 + 30 + 30 + 30
    empty_array = []
    for i in range(0, len(x)):
        r = x[i]
        if y[i] == 1:
            r = x[i] + L[int(Jan)]
        elif y[i] == 2:
            r = x[i] + L[int(Feb)]
        elif y[i] == 3:
            r = x[i] + L[int(Mar)]
        elif y[i] == 4:
            r = x[i] + L[int(Apr)]
        elif y[i] == 5:
            r = x[i] + L[int(May)]
        elif y[i] == 6:
            r = x[i] + L[int(June)]
        elif y[i] == 7:
            r = x[i] + L[int(July)]
        elif y[i] == 8:
            r = x[i] + L[int(August)]
        elif y[i] == 9:
            r = x[i] + L[int(Sep)]
        elif y[i] == 10:
            r = x[i] + L[int(Oct)]
        elif y[i] == 11:
            r = x[i] + L[int(Nov)]
        elif y[i] == 12:
            r = x[i] + L[int(Dec)]
        empty_array.append(r)

    return empty_array


"""
The following code will transfer a date in form:
dd/mm/yyyy to a decimal date, more useful for curve smoothing
"""


def long_date_to_decimal_date(x):
    array = []
    for i in range(0, len(x)):
        j = x[i]
        decy = pyasl.decimalYear(j)
        decy = float(decy)
        # print(decy)
        array.append(decy)
    # print(array)
    return array


# returns the array/list back but in the decimal form

"""
My rough attempt to curve fit a line before I got the John Miller Code working
Ensure the data has been re-indexed before putting through here or it won't work.
"""


def cbl_curve_fit(x, y):
    n = 4
    empty_array = []  # pre-allocate an array where the for loop will put the coefficient outputs
    cols = []  # empty array pre-allocated for the columns needed in new dataframe
    for i in range(0, n):
        p = np.polyfit(x, y, i, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
        print(type(p))
        empty_array.append(p)
        cols.append(i)
    coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
    coeffs = pd.DataFrame(empty_array, columns=['0', '1', '2', '3'])  # output the results from for loop into dataframe

    degree0 = coeff.iloc[0]
    degree1 = coeff.iloc[1]
    degree2 = coeff.iloc[2]
    degree3 = coeff.iloc[3]

    y_guess_0th = degree0[0] * x ** 0
    y_guess_lin = degree1[0] * x ** 1 + degree1[1] * x ** 0
    y_guess_2nd = degree2[0] * x ** 2 + degree2[1] * x ** 1 + degree2[2] * x ** 0
    y_guess_3rd = degree3[0] * x ** 3 + degree3[1] * x ** 2 + degree3[2] * x ** 1 + degree3[3] * x ** 0
    #
    Degree_to_test = y_guess_3rd
    residual = y - Degree_to_test

    # # TRANSFORM RESIDUAL
    G = fft(residual)
    G = abs(G)

    # # CREATE LOW PASS FILTER
    fs = 0.1  # sampling frequency
    x_new = np.arange(0, len(G))
    x_new = x_new * 0.1  # setting the data to be measured once per second (10 Hz)
    delta = 1 / (len(G) * fs)  # parameter used to calculate the frequency
    k = np.arange(0, len(G), 1)  # list from 0 to 3952
    freq = k * delta
    cutoff = 667
    f_c = 365 / cutoff
    p = 4
    ln2 = -.0693
    H_f = np.exp(ln2 * (freq / f_c) ** p)

    # MULTIPLY FUNCTION BY FILTER AND SMOOTH LINE
    residual_forinv = G * H_f
    G_new = ifft(residual_forinv)
    G_new = np.real(G_new)
    smoothed_trend = G_new + y_guess_3rd

    return smoothed_trend, print(type(p))


"""
A standard student's two-tail t-test that will require two lists/arrays as input
https://www.youtube.com/watch?v=pTmLQvMM-1M&ab_channel=BozemanScience
Null Hypothesis = there is NO difference between the samples
If t-value is lower than critical value, DON'T REJECT NULL = NO DIFFERENCE
If t-value is higher than critical value, REJECT = DIFFERENCE EXISTS

this test uses 0.05 probability

THIS METHOD DOES NOT WORK YET - MUST DEAL WITH VARIABLE D_of_F's not equal to those in table
"""


def simple_t_test(x1, x2):
    dfx = pd.read_excel(
        r'G:\My Drive\Work\GNS Radiocarbon Scientist\The Science\Stats and Data Analysis\Matlab and Python Files\tables.xlsx',
        sheet_name='t table', skiprows=6)
    dfx = dfx.reset_index()
    t_table_05 = dfx[0.05]

    # get the rough data needed for a t-test
    mean_x1 = np.average(x1)
    mean_x2 = np.average(x2)
    var_x1 = np.var(x1)
    var_x2 = np.var(x2)

    # the math
    mean = abs(mean_x2 - mean_x1)
    denominator = np.sqrt((var_x1 / len(x1)) + (var_x2 / len(x2)))
    t_value = mean / denominator
    d_of_f = len(x1) + len(x2) - 2 + 2  # usually you subtract two, but length starts at zero so I add them back in

    # find the degrees of freedom, and the closest number in the table to my degrees of freedom
    aux = []
    for valor in t_table_05:
        aux.append(abs(d_of_f - valor))
    index = aux.index(min(aux))
    value_crit = t_table_05[index]

    if t_value <= value_crit:
        result = print('There is NO DIFFERENCE')
    else:
        result = print('There IS A DIFFERENCE')
    return result


# http://ipl.physics.harvard.edu/wp-uploads/2013/03/PS3_Error_Propagation_sp13.pdf
# computes the basic analytical data for TWO (ONLY TWO) datasets
def basic_analysis(x, y, name1, name2):
    # compute data for individual datasets

    x_mean = np.average(x)
    y_mean = np.average(y)
    x_stddev = np.std(x)
    y_stddev = np.std(y)
    x_std_err = x_stddev / len(x)
    y_std_err = y_stddev / len(y)

    # compute data for datasets together
    average = (x_mean + y_mean) / 2
    error_prop = (np.sqrt(x_stddev ** 2 + y_stddev ** 2)) / 2

    data = [[name1, x_mean, x_std_err],
            [name2, y_mean, y_std_err],
            ['Both Series', average, error_prop]]
    table2 = (tabulate(data, headers=["Label", "Average", "Std Error / Prop Error"]))
    df = pd.DataFrame(data=data)
    return df


""" 
h = array of y values to monte-carlo
h_err = errors associated with y values
c = an initial array of curve-smoothed data (x-values)
d = an initial array of curve-smoothed data (y-values)
n = number of iterations 
x = x-values for the data that is going through the ccgcv curve fit (must be in decimal date)  
"""


def monte_carlo(h, h_err, c, d, n, x_date):  # a = array of y-values to monte carlo

    # SECTION 1: LOOP THROUGH THE DATA, AND ADD A RANDOM VALUE BETWEEN THE RANGE OF UNCERTAINTY.
    #            DO THIS 'N' TIMES AND STACK THE ARRAY ONTO ITSELF.
    # initializing a new array to "stack" onto because I don't want to stack onto my real data later
    new_array = h
    for i in range(0, n):
        empty_array = []
        for j in range(0, len(h)):
            a = h[j]  # grab the first item in the set
            b = h_err[j]  # grab the uncertainty
            rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
            c = a + rand  # add this to the number
            empty_array.append(c)  # add this to a list
            # print(len(empty_array))
        new_array = np.vstack((new_array, empty_array))

    # SECTION 2: PUT EACH ROW OF THIS NEW ARRAY THROUGH THE MILLER CCGCV CURVE SMOOTHER
    empty_array_for_date = c  # I'm initializing the new array as the original output from the Miller file, so there's something the v-stack onto w/ same changed dimensions.
    empty_array_for_y = d  # I'm initializing the new array as the original output from the Miller file, so there's something the v-stack onto.
    for i in range(0, len(new_array)):
        monte1 = new_array[i]  # grab the first row of the array
        monte_output = ccgFilter(x_date, monte1).getMonthlyMeans()  # put that first row through the miler CCG filter...
        # use my other function to convert Miller code output to decimal dates
        monte_output_date = year_month_todecimaldate(monte_output[0], monte_output[1])
        # also grab the y-data
        monte_output_y = monte_output[2]
        empty_array_for_date = np.vstack((empty_array_for_date, monte_output_date))
        empty_array_for_y = np.vstack((empty_array_for_y, monte_output_y))


    dataf = pd.DataFrame(empty_array_for_y)  # output the results from for loop into dataframe
    mean_array = []
    stdev_array = []
    for i in range(0, len(empty_array_for_y[1])):
        element1 = np.sum(dataf[i])  # grab the first column of the dataframe and take the sum
        element1 = element1 / len(empty_array_for_y)  # find the mean of the first column of the dataframe
        mean_array.append(element1)  # append it to a new array
        stdev_monte = np.std(dataf[i])  # find the stdev of the first column of the dataframe
        stdev_array.append(stdev_monte)

    return mean_array, stdev_array
