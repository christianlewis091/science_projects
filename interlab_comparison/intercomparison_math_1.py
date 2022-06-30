import numpy as np
import pandas as pd
from scipy import stats
# import the data from the "Pre-Processing" files:
from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_Heidelberg import combine_heidelberg
from Pre_Processing_UniMagallanes import combine_Magallanes
from Pre_Processing_SIO_LLNL import combine_SIO

"""
I opt to begin the series of intercomparisons with the ANSTO v RRL intercomparison. In this data, there is only
one measurement per years available, and 9 measuremnts per site. This one can be done quickly using a paired t test. 


"""
ansto = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'ANSTO')]
rrl = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'RRL')]

X = stats.ttest_rel(ansto['D14C'], rrl['D14C'])
print(X)
