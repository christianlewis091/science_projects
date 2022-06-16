import matplotlib as mpl
import numpy as np
import pandas as pd
import seaborn as sns
from X_my_functions import long_date_to_decimal_date
from scipy import stats

df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\Heidelberg_OffsetCorrections.xlsx')
cgo = df.loc[(df['#location']) == 'CGO']
neu = df.loc[(df['#location']) == 'Macquarie_Isl.']
mcq = df.loc[(df['#location']) == 'NMY']

cgo_offset1 = cgo['D14C_1']
cgo_offset2 = cgo['D14C_2']
neu_offset1 = neu['D14C_1']
neu_offset2 = neu['D14C_2']
mcq_offset1 = mcq['D14C_1']
mcq_offset2 = mcq['D14C_2']
ttesting = df['D14C_2_err_test']
ttesting2 = df['D14C_2_err']

cgo_test = stats.ttest_rel(cgo_offset1, cgo_offset2)
print(cgo_test)
neu_test = stats.ttest_rel(neu_offset1, neu_offset2)
print(neu_test)
mcq_test = stats.ttest_rel(mcq_offset1, mcq_offset2)
print(mcq_test)
ttest_test = stats.ttest_rel(ttesting, ttesting2)
print(ttest_test)




