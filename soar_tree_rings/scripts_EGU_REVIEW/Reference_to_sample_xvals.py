"""
December 4, 2024: Final check that the script still runs successfully before I submit the paper etc.
Still runs :)

October 17, 2022
Data outputs properly, but the final trended line isn't really smooth at all. The trended lines should be really smooth,
free of jagged peaks. Have I actually used smooth instead of trend? I do both...

October 14, 2022
Still troubleshooting the data output here, dates are coming out funky I think because of scrambling along indexes

October 10, 2022

This script will take the two (+1) reference datasets and use the CCGCRV output to generate x-values for
the trended and smooth curves at all datapoints we have for the SAMPLES.

Currently, for some reason, during creatino of the final dataframe, the x-values get jumbled and the bomb peak looks
like it's drunk. I'm not sure why. Need to come back to this.
"""
import pandas as pd
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend
from datetime import datetime
import matplotlib.pyplot as plt
# read in the list of all SAMPLES (SOAR)
# samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
# Dec 3 check from final EGU runs
samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')

# 12/12/2023 I need to add MCQ comparison (to validate CMP) into the paper. Need to add these into the works here,
# will add Heidelberg data now, and remove before main plots.
mcq = pd.read_excel('H:/Science/Datasets/heidelberg_MQA.xlsx')

res = []
# need to convert MCQ dates to decimal dates
for i in range(0, len(mcq)):
    row = mcq.iloc[i]
    date_string = str(row['Average of Dates'])
    date_string = date_string[:10]
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    decimal_date = date_object.year + (date_object.timetuple().tm_yday - 1) / 365.25
    res.append(decimal_date)
mcq['Average of Dates'] = res

mcq = mcq[['#location', 'Average of Dates', 'D14C','1sigma_error']]
mcq = mcq.rename(columns={'#location': 'Site', 'Average of Dates': 'DecimalDate', '1sigma_error':'∆14Cerr','D14C':'∆14C'})
samples = pd.concat([samples, mcq])
# samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned.xlsx')

# read in the references
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/harmonized_dataset.xlsx')
ref1 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/reference1.xlsx')

output_xvals = pd.concat([ref2['Decimal_date'], ref1['Decimal_date'], samples['DecimalDate']]).reset_index(drop=True)
output_xvals = pd.DataFrame({'x': output_xvals}).sort_values(by=['x'], ascending=True).reset_index(drop=True)

n = 10000  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff
#
# """
# See Interlab_comparison project heidelberg_intercomparison_wD14C for further explanation of this function.
# """
reference2_smooth = monte_carlo_randomization_smooth(ref2['Decimal_date'], output_xvals['x'], ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
reference2_trend = monte_carlo_randomization_trend(ref2['Decimal_date'], output_xvals['x'], ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
reference3_smooth = monte_carlo_randomization_smooth(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)
reference3_trend = monte_carlo_randomization_trend(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)

reference2_smooth = reference2_smooth[2]
reference2_trend = reference2_trend[2]
reference3_smooth = reference3_smooth[2]
reference3_trend = reference3_trend[2]

montes = pd.DataFrame({'Decimal_date': output_xvals['x'],
                       'D14C_ref2s_mean': reference2_smooth['Means'], 'D14C_ref2s_std': reference2_smooth['stdevs'],
                       'D14C_ref2t_mean': reference2_trend['Means'], 'D14C_ref2t_std': reference2_trend['stdevs'],
                       'D14C_ref3s_mean': reference3_smooth['Means'], 'D14C_ref3s_std': reference3_smooth['stdevs'],
                       'D14C_ref3t_mean': reference3_trend['Means'], 'D14C_ref3t_std': reference3_trend['stdevs']
                       }).drop_duplicates(subset='Decimal_date')
# montes.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
montes.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/monte_output.xlsx')






# #
# # # samples = samples[['Ring code', 'R number', 'Site', 'F14C', 'F14Cerr',
# # #                   'Decimal_date', 'D14C', 'D14Cerr', 'Lat', 'Lon', '#location', 'Sample',
# # #                   'Lab', 'Analysis', 'Sample ', 'Sample.1', 'Average of Dates', 'd13C',
# # #                   'Flag', 'D14C_1', 'weightedstderr_D14C_1', 'sampler_id',
# # #                   'wheightedanalyticalstdev_D14C']]
#
# # samples['Ref1'] = -999  # currently a placeholder
