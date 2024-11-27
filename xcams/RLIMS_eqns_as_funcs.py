"""
Coding up some RLIMS eqns as functions for various future purposes.
r"C:/Users/clewis/IdeaProjects/GNS/xcams/November_2024_fractionation_analysis shows the RLIMS eqns in an easy to understand format.
"""
import numpy as np

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
Testing
# I'm going to take an old air wheel and test that the eqn's work
TP = 88149; rts = 0.99966, rts_err = 0.00114, mcc = .00214, mcc_err = 0.00023

"""
# print(rts_corrected(0.99966, .00214, 0, 0)) # correct
# print(rts_corr_error(0.99966, .00114, .00214, .00023, 0,0,0,0))
# print(f_normed_corrected(0.99966,.98780))
# print(f_corr_norm_err(0.99966,0.00114, .09)) # 4th digit currently different
#
