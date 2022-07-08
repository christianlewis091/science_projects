import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib import cm
from colorspacious import cspace_converter
import pandas as pd
import seaborn as sns
from X_my_functions import scatter_plot, error_plot

from intercomparison_math_1 import ansto, rrl, sio_nwt3, sio_nwt4, rrl_nwt3, rrl_nwt4, rafter, magallanes


error_plot(rrl['Decimal_date'], rrl['FM'], rrl['FM_err'],
           x2 = ansto['Decimal_date'], y2 = ansto['FM'], z2 = ansto['FM_err'], savename = 'ANSTO_comparison',
           label1= 'Rafter', label2 = 'ANSTO', ylabel = 'Fraction Modern', xlabel = 'Growth Year')

error_plot(sio_nwt3['Decimal_date'], sio_nwt3['D14C'], sio_nwt3['D14C_err'], label1 = 'SIO',
           x2 = rrl_nwt3['Decimal_date'], y2 = rrl_nwt3['D14C'], z2 = rrl_nwt3['D14C_err'], label2 = 'Rafter',
           ylabel = '\u0394$^1$$^4$CO$_2$ (\u2030)', xlabel = 'Date (or Measurement #)', savename = 'SIO_Comparison')

