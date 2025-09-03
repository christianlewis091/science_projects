"""
Coding up some RLIMS eqns as functions for various future purposes.
r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis shows the RLIMS eqns in an easy to understand format.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

def rts_corrected(rts, mcc, dcc, dcc_std):
    rts_corr = (rts-mcc)/(1+dcc_std-dcc-mcc)
    return rts_corr

def rts_corr_error(rts, rts_err,
                   mcc, mcc_err,
                   dcc, dcc_err,
                   dcc_std, dcc_std_err):

    p1 = (rts_err**2)/(1+dcc_std-dcc-mcc)**2
    p2 = (mcc_err**2 * ((rts-1)**2 / (1+dcc_std-dcc-mcc)**4))
    p3 = (dcc_err**2 * ((rts-mcc)**2 / (1+dcc_std-dcc-mcc)**4))
    p4 = (dcc_std_err**2 * ((rts-mcc)**2 / (1+dcc_std-dcc-mcc)**4))

    rts_corr_err = np.sqrt( p1 + p2 + p3 + p4 )
    return rts_corr_err

def f_normed_corrected(rts_corr, Std_13C_val_const):
    # Norm exp factor is usually 0, knocking out middle term
    # Stand 13C val const = .987
    # Stand spec act const = 0.95
    # f_normed_corr = (rts_corr / (0.95 * 1)) *(((1 + delta13C_stds_av/ 1000) / (1 + delta13C_In_Calculation / 1000))**Norm_exp_factor )* Std_13C_val_const # middle term usually knocked out
    f_normed_corr = (rts_corr / (0.95 * 1))* Std_13C_val_const # why is 13C value incl, this isn't the normalization correction, # 9878 is correction for oxalic primary standard
    return f_normed_corr

def f_corr_norm_err(rts_corr, rts_corr_err, wtw_err):
    f_corr_norm_error =  np.sqrt(rts_corr_err**2 +(wtw_err*.01*rts_corr)**2) / 0.95
    return f_corr_norm_error

"""
Diagonal blank plot
"""
def UCI_MCC_plot(wtgraph, rts, savelocation, title):
    # Create a figure and a set of subplots
    fig, ax = plt.subplots()

    # Set the x and y scales to logarithmic
    ax.set_xscale('log')
    ax.set_yscale('log')

    # Set the limits for x and y axes
    ax.set_xlim(0.001, 10)
    ax.set_ylim(0.0001, 1)

    # Add labels to the axes
    ax.set_xlabel('Sample Size (mg)')
    ax.set_ylabel('Ratio to OX-1')
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_scientific(False)
    # Add a grid for better readability
    ax.grid(True, which="both", ls="--")

    # add the diagonal lines
    x = [0.001, 10]
    y1 = [0.2, .00002]
    y2 = [0.3, .00003]
    y3 = [0.4, .00004]
    y4 = [0.5, .00005]
    y5 = [0.6, .00006]
    y6 = [0.8, .00008]
    y7 = [1, .0001]
    y8 = [2, .0002]
    y9 = [5, .0005]
    ys = [y1, y2, y3, y4, y5, y6, y7, y8, y9]
    labels = ['0.2','0.3','0.4','0.5','0.6','0.8','1','2','5']
    for i in range(0, len(ys)):
        plt.plot(x, ys[i], label=f'{labels[i]}')


    plt.scatter(wtgraph, rts, label='', zorder=0)

    plt.savefig(f'{savelocation}/{title}.png', dpi=300, bbox_inches="tight")
    plt.close()

"""
Testing
# I'm going to take an old air wheel and test that the eqn's work
TP = 88149; rts = 0.99966, rts_err = 0.00114, mcc = .00214, mcc_err = 0.00023

"""
# print(rts_corrected(0.99966, .00214, 0, 0)) # correct
# print(rts_corr_error(0.99966, .00114, .00214, .00023, 0,0,0,0))
# print(f_normed_corrected(0.99966,.98780))
# print(f_corr_norm_err(0.99966,0.00114, .09)) # 4th digit currently different
#
