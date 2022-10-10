"""
October 10, 2022

For the SOAR Tree ring dataset, in order to see all the data in reference to the backgrounds, I need to get all the background smoothed and have
outputs for all the sample x's. This short script will merge all the sample data into one file so I can easily find
all the x-values I need to output for my background reference

I tried importing directly from the other scripts but then it needs to rerun all those scripts which takes too long.
Therefore I'm going to import from the written excel files.
"""
import pandas as pd
import matplotlib.pyplot as plt

# import cleaned SOAR Tree rings
soar = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/SOARTreeRingData_CBL_cleaned.xlsx')
mcq = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/MCQ_offset.xlsx')
neu = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/NEU_offset.xlsx')

# cleanup the datasets for simpler use later
soar = soar[['Ring code', 'R number', 'Site', 'F14C', 'F14Cerr',
             'DecimalDate', '∆14C', '∆14Cerr', 'Lat', 'Lon']]
soar = soar.rename(columns={'∆14C': 'D14C',
                            '∆14Cerr': 'D14Cerr',
                            'DecimalDate': 'Decimal_date'})

mcq = mcq[['#location', 'Sample', 'Lab', 'Analysis',
           'Sample ', 'Sample.1', 'Average of Dates', 'D14C', '1sigma_error',
           'd13C', 'Flag', 'Decimal_date', 'D14C_1', 'weightedstderr_D14C_1']]
mcq = mcq.rename(columns={'1sigma_error': 'D14Cerr'})

neu = neu[['#location', 'sampler_id',
           'D14C', 'weightedstderr_D14C', 'wheightedanalyticalstdev_D14C',
           'Decimal_date', 'D14C_1',
           'weightedstderr_D14C_1']]
neu = neu.rename(columns={'weightedstderr_D14C': 'D14Cerr'})

complete_samples = pd.concat([soar, mcq, neu])
complete_samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/complete_samples.xlsx')

plt.scatter(complete_samples['Decimal_date'], complete_samples['D14C'])
plt.show()
