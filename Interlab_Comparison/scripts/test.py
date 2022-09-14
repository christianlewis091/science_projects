from Pre_Processing_Heidelberg import combine_heidelberg
import numpy as np

baringhead = combine_heidelberg.loc[(combine_heidelberg['Site'] == 'BHD')]
print(len(baringhead))

baringhead = baringhead.loc[(baringhead['Decimal_date'] != 1990.0534)]
print(len(baringhead))


testing2 = baringhead.loc[(baringhead['Decimal_date'].between(1990, 1993)) & (baringhead['METH_COLL'] == 'NaOH_static')]
