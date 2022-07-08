from Pre_Processing_ANSTO import combine_ANSTO
from Pre_Processing_UniMagallanes import combine_Magallanes
from Pre_Processing_SIO_LLNL import combine_SIO
from X_my_functions import intercomparison_ttest


"""
This file uses PRE-CLEANED data from the following institutions, 
and compares them to RRL using the specified type of data:
ANSTO: Tree Rings
SIO/LLNL: Standard Materials NWT3 and NWT4
University of Magallanes: Tree Rings
University of Heidelberg: Atmospheric CO2 measurements. 
The null hypothesis for the following t-tests is: "There is NO systematic bias between institutions". If p-values 
come out less than 0.01, or 1%, or 98% confidence interval, I call that they are significantly different. 

FOR INTERCOMPARISONS, USE FM WHERE POSSIBLE

All data visualizations will appear in another .py file. 

First I'm going to just index the data I need for the t-tests for ANSTO, SIO/LLNL (NWT3 and NWT4) and Magallanes. 
"""

ansto = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'ANSTO')].reset_index(drop=True)
rrl = combine_ANSTO.loc[(combine_ANSTO['Site'] == 'RRL')].reset_index(drop=True)

NWT3 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT3')]
sio_nwt3 = NWT3.loc[(NWT3['Site'] == 'LLNL')]
rrl_nwt3 = NWT3.loc[(NWT3['Site'] == 'RRL')]

NWT4 = combine_SIO.loc[(combine_SIO['standard_type'] == 'NWT4')]
sio_nwt4 = NWT4.loc[(NWT4['Site'] == 'LLNL')]
rrl_nwt4 = NWT4.loc[(NWT4['Site'] == 'RRL')]

# Magallanes data is setup slightly different, take a look at the data to see why it is indexed this way -
# perhaps it is so only beccause I'm a novice coder...
rafter = combine_Magallanes.loc[(combine_Magallanes['Site'] == 'RRL')]
magallanes = combine_Magallanes.loc[(combine_Magallanes['Site'] == 'Magallanes')]


# UNCOMMENT WHEN DONE WRITING THIS FILE! HERE ARE THE OTHER INTERCOMPARISON!
# I was first supplied with FM data from ANSTO so I'm going to use FM for this calculation.
a = intercomparison_ttest(ansto['D14C'], rrl['D14C'], 'ANSTO v RRL Test: Tree Rings, D14C', 'paired')
a = intercomparison_ttest(ansto['FM'], rrl['FM'], 'ANSTO v RRL Test: Tree Rings, FM', 'paired')

# I'll do this one in FM as well because it minimizes the amount of extra calculatinos
# that can lead to fake systematic bias.
b = intercomparison_ttest(sio_nwt3['FM'], rrl_nwt3['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')
c = intercomparison_ttest(sio_nwt4['FM'], rrl_nwt4['FM'], 'SIO/LLNL v RRL, NWT3 Intercomparison', 'not-paired')

# TODO deal with the multiple records from the same year
# d = intercomparison_ttest(rafter, magallanes, 'Magallanes v RRL Test: Tree Rings', 'paired')




