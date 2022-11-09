"""
Trying to understand the "goodness of fit test" that is used in AccelNet and also understand/be able to write/derive
our measurement precision on my own for deeper understanding.

According to J C Turnbull et al., "Chi square tests are used to evaluate the consistency of the data set by examining
the scatter of the mean values and their assigned uncertainties. When the chi-square right tail-probability is less
than 25% for the full dataset, or less than 2.5% for a single target, we increase sigma_ams to account for excess
variability.

The things I need to know for this is: in AccelNet, what is the chiLIM? Is it the chiStat for the 25% boundary of the
right tail?
"""
import numpy as np
import pandas as pd

df = pd.read_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\TW3438_testing.xlsx', skiprows=3)

calibration_positions = [0, 5, 10, 15, 20, 25, 30, 35]
unks_positions = [1, 2, 3, 4,
                  6, 7, 8, 9,
                  11, 12, 13, 14,
                  16,17,18,19,
                  21,22,23,24,
                  26,27,28,29,
                  31,32,33,34,
                  36,37,38,39]
"""
The following code block calculates the fcir for the standards, based on equations 3a and 3b in Zondervan 2015
"""
fcir_array = []
for i in range(0, len(calibration_positions)):
    cat = df.loc[df['position'] == calibration_positions[i]]
    c14_i, c12_i, c13_i, t = cat['14Ccnts'], cat['12Ccurr'], cat['13Ccurr'], cat['Tdetect']
    fcir_i = (c14_i * c12_i) / (t * (c13_i**2))  # calculates PER RUN FCIR
    fcir_i = np.average(fcir_i)
    fcir_array.append(fcir_i)

fcir_calibration = np.average(fcir_array)  # finds ONE VALUE for STANDARDS (which I know isn't really true since CALAMS
                                           # has a whole line.

"""
The following code block calculates the RTS for the unknowns, based on equations 4a and 4b in Zondervan 2015
"""
rts_array = []
unks = pd.DataFrame()
for i in range(0, len(unks_positions)):
    cat = df.loc[df['position'] == unks_positions[i]]
    c14_i, c12_i, c13_i, t = cat['14Ccnts'], cat['12Ccurr'], cat['13Ccurr'], cat['Tdetect']
    fcir_i = (c14_i * c12_i) / (t * (c13_i**2))  # calculates PER RUN FCIR (eqn 3a)
    sigma_i = fcir_i / np.sqrt(c14_i + 1)        # calculates PER RUN sigma (eqn 3b)
    w = 1/(sigma_i**2)                           # calculates PER RUN W

    # since the eqn 4a shows sigma(i), which indicates per run, I'm going to do the step inside the brackets next.
    numerator = (w * (fcir_i)) / fcir_calibration

    # the math is done for the entire selected cathode at each time, so now, I can just take the sum of the whole
    # array, and then divide, and append the final RTS to an array.
    rts = (np.sum(numerator)) / np.sum(w)
    rts_array.append(rts)

    cat = cat.iloc[[1]]
    cat = cat[['position', 'TP#']]
    unks = pd.concat([unks, cat], axis=0).reset_index(drop=True)

unks['RTS'] = rts_array
unks.to_excel(r'H:\Science\Current_Projects\04_ams_data_quality\AMS_stats\testing.xlsx')

