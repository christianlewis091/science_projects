"""
This iteration of this file was brought about by an email sent by Ingeborg Levin and Sam Hammer to Jocelyn and I, which
we recieved on 19 September 2023, morning New Zealand time.
To answer her message, I need to adjust and re-write a bit of code, specifically from the previous two python files:

pre_processing_Heidelberg.py
heidelberg_intercomparins_wD14C.py,
intercomparison_viz_1.py

I"m going to copy and paste a lot but also adjust where necessary to recreate her plots to try to answer her questions
specifically related to the difference between BHD flask and intergrated sampling.

"""
import numpy as np
import xlsxwriter
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
from X_my_functions import long_date_to_decimal_date
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend

# READ IN THE TWO DATA SETS
heidelberg = pd.read_excel(r'H:\Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40).dropna(subset=['D14C'])  # import heidelberg data
baringhead = pd.read_excel(r'H:\Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')  # import Baring Head data

# ADAPT THE DATE COLUMNS USING MY FUNCTION SO THEY"RE DECIMAL DATES AND CAN BE RUN THROUGH THE FUNCTION
heidelberg['Decimal_date'] = long_date_to_decimal_date(heidelberg['Average pf Start-date and enddate'])

# CLEAN UP BOTH DATASETS
# print(np.unique(heidelberg['flag_D14C'])) # HEIDELBERG DATA HAS NO FLAGS TO REMOVE
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)].reset_index(drop=True)  # Filtering out an outlier around 2019
baringhead = baringhead.loc[(baringhead['DELTA14C_ERR'] > -999)] # Filtering out data with uncertainties of -1000
baringhead = baringhead.loc[(baringhead['FLAG'] == '...')]

baringhead = baringhead.rename(columns = {'SITE':'Site', 'DEC_DECAY_CORR':'Decimal_date', 'DELTA14C':'D14C', 'DELTA14C_ERR':'D14C_err', 'F14C':'FM',
                                          'F14C_ERR':'FM_err'})
heidelberg = heidelberg.rename(columns = {'#location':'Site', 'weightedstderr_D14C':'D14C_err'})

# SPLIT BHD INTO TWO BASED ON METHOD
bhd_int = baringhead.loc[baringhead['METH_COLL'] == 'NaOH_static']
bhd_flask = baringhead.loc[baringhead['METH_COLL'] == 'Whole_air']

"""
Almost ready to start smoothing and having a look at the data, and recreate ingeborg's plot
"""

fake_x_temp = np.linspace(1986, 2016, (2016-1986)*12*3)  # create arbitrary set of x-values to control output, 3 per month for the years of interest

"""
Now we can do the curve smoothing
"""
n = 1000  # set the amount of times the code will iterate (set to 10,000 once everything is final)
ns = [10, 100, 1000]
for i in range(0, len(ns)):
    cutoff = 667  # FFT filter cutoff

    # bhd_smooth = monte_carlo_randomization_smooth(x1_bhd, my_x_1986_1991, y1_bhd, z1_bhd, cutoff, n)

    bhd_flask_smooth = monte_carlo_randomization_smooth(bhd_flask['Decimal_date'], fake_x_temp, bhd_flask['D14C'], bhd_flask['D14C_err'], cutoff, ns[i])
    bhd_int_smooth = monte_carlo_randomization_smooth(bhd_flask['Decimal_date'], fake_x_temp, bhd_flask['D14C'], bhd_flask['D14C_err'], cutoff, ns[i])
    heidelberg_smooth = monte_carlo_randomization_smooth(heidelberg['Decimal_date'], fake_x_temp, heidelberg['D14C'], heidelberg['D14C_err'], cutoff, ns[i])

    bhd_flask_trend = monte_carlo_randomization_trend(bhd_flask['Decimal_date'], fake_x_temp, bhd_flask['D14C'], bhd_flask['D14C_err'], cutoff, ns[i])
    bhd_int_trend = monte_carlo_randomization_trend(bhd_flask['Decimal_date'], fake_x_temp, bhd_flask['D14C'], bhd_flask['D14C_err'], cutoff, ns[i])
    heidelberg_trend = monte_carlo_randomization_trend(heidelberg['Decimal_date'], fake_x_temp, heidelberg['D14C'], heidelberg['D14C_err'], cutoff, ns[i])

    bhd_flask_smooth = bhd_flask_smooth[2]
    bhd_int_smooth = bhd_int_smooth[2]
    heidelberg_smooth = heidelberg_smooth[2]

    bhd_flask_trend = bhd_flask_trend[2]
    bhd_int_trend = bhd_int_trend[2]
    heidelberg_trend = heidelberg_trend[2]


    results = pd.DataFrame({'Decimal_date': fake_x_temp,
                            "BHD_Flask_Smooth_Mean": bhd_flask_smooth['Means'],
                            "BHD_Flask_Smooth_Stdev": bhd_flask_smooth['stdevs'],
                            "BHD_Int_Smooth_Mean": bhd_int_smooth['Means'],
                            "BHD_Int_Smooth_Stdev": bhd_int_smooth['stdevs'],

                            "BHD_Flask_trend_Mean": bhd_flask_trend['Means'],
                            "BHD_Flask_trend_Stdev": bhd_flask_trend['stdevs'],
                            "BHD_Int_trend_Mean": bhd_int_trend['Means'],
                            "BHD_Int_trend_Stdev": bhd_int_trend['stdevs'],

                            "Heid_trend_Mean": heidelberg_trend['Means'],
                            "Heid_trend_Stdev": heidelberg_trend['stdevs'],
                            "Heid_smooth_Mean": heidelberg_smooth['Means'],
                            "Heid_smooth_Stdev": heidelberg_smooth['stdevs'],

                            "D_BHD_int_flask_smooth": bhd_int_smooth['Means'] - bhd_flask_smooth['Means'],
                            "D_BHD_int_flask_smooth_err": (np.sqrt(bhd_int_smooth['stdevs']*2 + bhd_flask_smooth['stdevs']*2)),

                            "D_BHD_int_flask_trend": bhd_int_trend['Means'] - bhd_flask_trend['Means'],
                            "D_BHD_int_flask_trend_err": (np.sqrt(bhd_int_trend['stdevs']*2 + bhd_flask_trend['stdevs']*2)),

                            "CGO-BHD_int_smooth" : heidelberg_smooth['Means'] - bhd_int_smooth['Means'],
                            "CGO-BHD_int_smooth_err": (np.sqrt(heidelberg_smooth['stdevs']*2 + bhd_int_smooth['stdevs']*2)),

                            "CGO-BHD_int_trend" : heidelberg_trend['Means'] - bhd_int_trend['Means'],
                            "CGO-BHD_int_trend_err": (np.sqrt(heidelberg_trend['stdevs']*2 + bhd_int_trend['stdevs']*2)),

                            "CGO-BHD_flask_smooth" : heidelberg_smooth['Means'] - bhd_flask_smooth['Means'],
                            "CGO-BHD_flask_smooth_err": (np.sqrt(heidelberg_smooth['stdevs']*2 + bhd_flask_smooth['stdevs']*2)),

                            "CGO-BHD_flask_trend" : heidelberg_trend['Means'] - bhd_flask_trend['Means'],
                            "CGO-BHD_flask_trend_err": (np.sqrt(heidelberg_trend['stdevs']*2 + bhd_flask_trend['stdevs']*2)),
    })
    results = results[::10]
    results_trim = results.loc[(results['Decimal_date'] > 2010) | (results['Decimal_date'] < 1993)]
    # heidelberg_results = results[["Heid_trend_Mean","Heid_trend_Stdev","Heid_smooth_Mean","Heid_smooth_Stdev"]]
    # bhd_int_results = results[["BHD_Int_trend_Mean","BHD_Int_trend_Stdev","BHD_Int_smooth_Mean","BHD_Int_smooth_Stdev"]]
    # bhd_flask_results = results[["BHD_Flask_trend_Mean","BHD_Flask_trend_Stdev","BHD_Flask_smooth_Mean","BHD_Flask_smooth_Stdev"]]

    """
    Plot the data and the differences
    """

    fig = plt.figure(1, figsize=(16,8))
    gs = gridspec.GridSpec(2, 4)
    gs.update(wspace=.5, hspace=0.1)
    size1 = 5
    a1 = 0.15
    a2 = 1

    xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
    plt.title(f"CCGCRV Smooth {ns[i]}")
    # Add the Raw Data
    plt.errorbar(heidelberg['Decimal_date'], heidelberg['D14C'], yerr=heidelberg['D14C_err'], fmt='o', color='black', label='Cape Grim (40.7S)', alpha=a1)
    plt.errorbar(bhd_int['Decimal_date'], bhd_int['D14C'], yerr=bhd_int['D14C_err'], fmt='o', color='mediumspringgreen', label='Baring Head Integrated (41.4S)', alpha=a1)
    plt.errorbar(bhd_flask['Decimal_date'], bhd_flask['D14C'], yerr=bhd_flask['D14C_err'], fmt='o', color='cadetblue', label='Baring Head Flask (41.4S)', alpha=a1)

    # Add smoothed data
    plt.plot(results['Decimal_date'], results['Heid_smooth_Mean'], color='black', label='CGO smo')
    plt.plot(results['Decimal_date'], results["BHD_Int_Smooth_Mean"], color='mediumspringgreen', label='BHD Int smo')
    plt.plot(results['Decimal_date'], results["BHD_Flask_Smooth_Mean"], label='BHD Flask smo', color='cadetblue')
    plt.axvline()
    plt.legend()
    plt.grid()
    plt.xlim(1985, 2020)
    plt.ylim(-20, 200)
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')
    plt.xlabel('Collection Date')

    xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
    # plt.errorbar(results['Decimal_date'], results["CGO-BHD_int_smooth" ], yerr=results["CGO-BHD_int_smooth_err" ], fmt='o', color='cadetblue', label='CGO-BHD integral', alpha=a2)
    # plt.errorbar(results['Decimal_date'], results["CGO-BHD_flask_smooth"], yerr=results["CGO-BHD_flask_smooth_err" ], fmt='o', color='mediumspringgreen', label='CGO-BHD flask', alpha=a2)
    # plt.errorbar(results['Decimal_date'], results["D_BHD_int_flask_smooth"], yerr=results["D_BHD_int_flask_smooth_err"], fmt='o', color='red', label='BHD_int-BHD_flask', alpha=a2)

    plt.scatter(results['Decimal_date'], results["CGO-BHD_int_smooth" ],marker='o', color='cadetblue', label='CGO-BHD integral', alpha=a2)
    plt.scatter(results['Decimal_date'], results["CGO-BHD_flask_smooth"], marker='o', color='mediumspringgreen', label='CGO-BHD flask', alpha=a2)
    plt.scatter(results_trim['Decimal_date'], results_trim["D_BHD_int_flask_smooth"], marker='o', color='red', label='BHD_int-BHD_flask', alpha=a2)

    plt.axvline()
    plt.legend()
    plt.grid()
    plt.xlim(1985, 2020)
    plt.ylim(-10, 10)
    plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
    plt.xlabel('Collection Date')
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/forIngeborg_smooth_{ns[i]}.png',
                dpi=300, bbox_inches="tight")

    plt.close()


    """
    XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    """
    fig = plt.figure(1, figsize=(16,8))
    gs = gridspec.GridSpec(2, 4)
    gs.update(wspace=.5, hspace=0.1)
    size1 = 5
    a1 = 0.15
    a2 = 1

    xtr_subsplot = fig.add_subplot(gs[0:2, 0:2])
    plt.title(f"CCGCRV Trend {ns[i]}")
    # Add the Raw Data
    plt.errorbar(heidelberg['Decimal_date'], heidelberg['D14C'], yerr=heidelberg['D14C_err'], fmt='o', color='black', label='Cape Grim (40.7S)', alpha=a1)
    plt.errorbar(bhd_int['Decimal_date'], bhd_int['D14C'], yerr=bhd_int['D14C_err'], fmt='o', color='mediumspringgreen', label='Baring Head Integrated (41.4S)', alpha=a1)
    plt.errorbar(bhd_flask['Decimal_date'], bhd_flask['D14C'], yerr=bhd_flask['D14C_err'], fmt='o', color='cadetblue', label='Baring Head Flask (41.4S)', alpha=a1)

    # Add smoothed data
    plt.plot(results['Decimal_date'], results['Heid_trend_Mean'], color='black', label='CGO smo')
    plt.plot(results['Decimal_date'], results["BHD_Int_trend_Mean"], color='mediumspringgreen', label='BHD Int smo')
    plt.plot(results['Decimal_date'], results["BHD_Flask_trend_Mean"], label='BHD Flask smo', color='cadetblue')
    plt.axvline()
    plt.legend()
    plt.grid()
    plt.xlim(1985, 2020)
    plt.ylim(-20, 200)
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')
    plt.xlabel('Collection Date')

    xtr_subsplot = fig.add_subplot(gs[0:2, 2:4])
    # plt.errorbar(results['Decimal_date'], results["CGO-BHD_int_smooth" ], yerr=results["CGO-BHD_int_smooth_err" ], fmt='o', color='cadetblue', label='CGO-BHD integral', alpha=a2)
    # plt.errorbar(results['Decimal_date'], results["CGO-BHD_flask_smooth"], yerr=results["CGO-BHD_flask_smooth_err" ], fmt='o', color='mediumspringgreen', label='CGO-BHD flask', alpha=a2)
    # plt.errorbar(results['Decimal_date'], results["D_BHD_int_flask_smooth"], yerr=results["D_BHD_int_flask_smooth_err"], fmt='o', color='red', label='BHD_int-BHD_flask', alpha=a2)

    plt.scatter(results['Decimal_date'], results["CGO-BHD_int_trend" ],marker='o', color='cadetblue', label='CGO-BHD integral', alpha=a2)
    plt.scatter(results['Decimal_date'], results["CGO-BHD_flask_trend"], marker='o', color='mediumspringgreen', label='CGO-BHD flask', alpha=a2)
    plt.scatter(results_trim['Decimal_date'], results_trim["D_BHD_int_flask_trend"], marker='o', color='red', label='BHD_int-BHD_flask', alpha=a2)

    plt.axvline()
    plt.legend()
    plt.grid()
    plt.xlim(1985, 2020)
    plt.ylim(-10, 10)
    plt.ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
    plt.xlabel('Collection Date')
    plt.savefig(f'C:/Users/clewis/IdeaProjects/GNS/Interlab_Comparison/output/forIngeborg_trend_{ns[i]}.png',
                dpi=300, bbox_inches="tight")

    plt.close()






