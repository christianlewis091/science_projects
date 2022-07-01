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

# Ttest_relResult(statistic=-0.15845108200803193, pvalue=0.8775997722995811)
# No difference.

"""
Let's do SIO/LLNL Next
"""
NWT3 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT3')]
sio = NWT3.loc[(NWT3['Site'] == 'LLNL')]
rrl = NWT3.loc[(NWT3['Site'] == 'RRL')]
X = stats.ttest_ind(sio['D14C'], rrl['D14C'])
print(X)

# Ttest_indResult(statistic=-2.8398495199042815, pvalue=0.005521192151168426)

NWT4 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT4')]
sio = NWT4.loc[(NWT4['Site'] == 'LLNL')]
rrl = NWT4.loc[(NWT4['Site'] == 'RRL')]
X = stats.ttest_ind(sio['D14C'], rrl['D14C'])

# Ttest_indResult(statistic=-3.6590617902433604, pvalue=0.0004197404882645735)

# TODO next, clean up function that does "Basic analysis" to be more broadly used and apply here to get fast averages and such