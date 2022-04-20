"""
In multiple files during my "Radiocarbon Inter comparison" project,
I've had this curve fitting code in every single script, which is
breaking the cardinal programming rule of "don't repeat yourself". I'm going to
keep the code here as a function, and call it so that it can make all of my
other codes simpler.
"""

""" curve fit code currently calculates 'n' number of coefficients (linear, polynomial, poly2, poly3, etc)  """

import numpy as np
import pandas as pd
from numpy.fft import fft, ifft

# df = pd.read_excel(r'C:\Users\lewis\venv\python310\python-masterclass-remaster-shared\RadiocarbonIntercomparison\output3.xlsx')
# x = df['time_decimal']
# y = df['value']

def cbl_curve_fit(x,y):
    n = 4
    empty_array = []  # pre-allocate an array where the for loop will put the coefficient outputs
    cols = []  # empty array pre-allocated for the columns needed in new dataframe
    for i in range(0, n):
        p = np.polyfit(x, y, i, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
        empty_array.append(p)
        cols.append(i)
    coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
    coeffs = pd.DataFrame(empty_array, columns=['0', '1', '2', '3'])  # output the results from for loop into dataframe

    degree0 = coeff.iloc[0]
    degree1 = coeff.iloc[1]
    degree2 = coeff.iloc[2]
    degree3 = coeff.iloc[3]

    y_guess_0th    = degree0[0]*x**0
    y_guess_lin = degree1[0]*x**1 + degree1[1]*x**0
    y_guess_2nd    = degree2[0]*x**2 + degree2[1]*x**1 + degree2[2]*x**0
    y_guess_3rd    = degree3[0]*x**3 + degree3[1]*x**2 + degree3[2]*x**1 + degree3[3]*x**0
#
    Degree_to_test = y_guess_3rd
    residual = y - Degree_to_test

    # # TRANSFORM RESIDUAL
    G = fft(residual)
    G = abs(G)

    # # CREATE LOW PASS FILTER
    fs = 0.1 # sampling frequency
    x_new = np.arange(0, len(G))
    x_new = x_new*0.1  # setting the data to be measured once per second (10 Hz)
    delta = 1/(len(G)*fs)  # parameter used to calculate the frequency
    k = np.arange(0, len(G), 1) # list from 0 to 3952
    freq = k*delta
    cutoff = 667
    f_c = 365 / cutoff
    p = 4
    ln2 = -.0693
    H_f = np.exp(ln2*(freq/f_c)**p)

    # MULTIPLY FUNCTION BY FILTER AND SMOOTH LINE
    residual_forinv = G*H_f
    G_new = ifft(residual_forinv)
    G_new = np.real(G_new)
    smoothed_trend = G_new + y_guess_3rd

    return smoothed_trend

# cbl_curve_fit(x,y)