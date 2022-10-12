"""
October 10, 2022

This script will take the two (+1) reference datasets and use the CCGCRV output to generate x-values for
the trended and smooth curves at all datapoints we have for the SAMPLES.

Currently, for some reason, during creatino of the final dataframe, the x-values get jumbled and the bomb peak looks
like it's drunk. I'm not sure why. Need to come back to this.
"""

import pandas as pd
from X_my_functions import monte_carlo_randomization_smooth
from X_my_functions import monte_carlo_randomization_trend
import matplotlib.pyplot as plt

# read in the list of all SAMPLES (SOAR, MCQ, NEU)
samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/complete_samples.xlsx')
samples = samples[['Ring code', 'R number', 'Site', 'F14C', 'F14Cerr',
                  'Decimal_date', 'D14C', 'D14Cerr', 'Lat', 'Lon', '#location', 'Sample',
                  'Lab', 'Analysis', 'Sample ', 'Sample.1', 'Average of Dates', 'd13C',
                  'Flag', 'D14C_1', 'weightedstderr_D14C_1', 'sampler_id',
                  'wheightedanalyticalstdev_D14C']]

# read in the references
ref2 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/harmonized_dataset.xlsx')
ref3 = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference3.xlsx')

output_xvals = pd.concat([ref2['Decimal_date'], ref3['Decimal_date'], samples['Decimal_date']]).reset_index(drop=True)
output_xvals = pd.DataFrame({'x': output_xvals}).sort_values(by=['x'], ascending=True).reset_index(drop=True)
output_xvals_sorted = output_xvals['x']
output_xvals_sorted.to_excel('testing_sort.xlsx')
n = 10000  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff

"""
See Interlab_comparison project heidelberg_intercomparison_wD14C for further explanation of this function.
"""
reference2_smooth = monte_carlo_randomization_smooth(ref2['Decimal_date'], output_xvals_sorted, ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
reference2_trend = monte_carlo_randomization_trend(ref2['Decimal_date'], output_xvals_sorted, ref2['D14C'], ref2['weightedstderr_D14C'], cutoff, n)
reference3_smooth = monte_carlo_randomization_smooth(ref3['Decimal_date'], output_xvals_sorted, ref3['D14C'], ref3['weightedstderr_D14C'], cutoff, n)
reference3_trend = monte_carlo_randomization_trend(ref3['Decimal_date'], output_xvals_sorted, ref3['D14C'], ref3['weightedstderr_D14C'], cutoff, n)

reference2_smooth = reference2_smooth[2]
ref2_mean_smooth, ref2_stdevs_smooth = reference2_smooth['Means'], reference2_smooth['stdevs']
reference2_trend = reference2_trend[2]
ref2_mean_trend, ref2_stdevs_trend = reference2_trend['Means'], reference2_trend['stdevs']
reference3_smooth = reference3_smooth[2]
ref3_mean_smooth, ref3_stdevs_smooth = reference3_smooth['Means'], reference3_smooth['stdevs']
reference3_trend = reference3_trend[2]
ref3_mean_trend, ref3_stdevs_trend = reference3_trend['Means'], reference3_trend['stdevs']


reference_dictionary = pd.DataFrame({"Decimal_date": output_xvals_sorted,
                                     "Ref 2.S Means": ref2_mean_smooth,
                                     "Ref 2.S stdev": ref2_stdevs_smooth,
                                     "Ref 2.T Means": ref2_mean_trend,
                                     "Ref 2.T stdev": ref2_stdevs_trend,
                                     "Ref 3.S Means": ref3_mean_smooth,
                                     "Ref 3.S stdev": ref3_stdevs_smooth,
                                     "Ref 3.T Means": ref3_mean_trend,
                                     "Ref 3.T stdev": ref3_stdevs_trend})

reference_dictionary_samples_only = reference_dictionary.merge(samples.drop_duplicates('Decimal_date'), how='left', on='Decimal_date')
reference_dictionary_samples_only = reference_dictionary_samples_only.dropna(subset='D14C')
reference_dictionary_samples_only = reference_dictionary_samples_only.loc[reference_dictionary_samples_only['Decimal_date'] > 1954.00274]

print(len(samples))
print(len(reference_dictionary))
print(len(reference_dictionary_samples_only))

reference_dictionary_samples_only.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/reference_dictionary_10000.xlsx')


# plt.plot(output_xvals_sorted, ref2_mean_smooth)
# plt.scatter(reference_dictionary['Decimal_date'], reference_dictionary['Ref 2.S Means'])
# plt.show()
#













