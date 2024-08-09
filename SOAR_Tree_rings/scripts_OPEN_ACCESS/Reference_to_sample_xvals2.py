import pandas as pd

samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_tree_ring_analysis/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
montes = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_x_vals/monte_output.xlsx') # from References_to_samples_xvals

D14C_ref2s_mean = []  # initialize an empty array
D14C_ref2s_std = []  # initialize an empty array

D14C_ref2t_mean = []  # initialize an empty array
D14C_ref2t_std = []  # initialize an empty array

D14C_ref3s_mean = []  # initialize an empty array
D14C_ref3s_std = []  # initialize an empty array

D14C_ref3t_mean = []  # initialize an empty array
D14C_ref3t_std = []  # initialize an empty array

for i in range(0, len(samples)):
    samples_row = samples.iloc[i]
    sample_date = samples_row['DecimalDate']

    for k in range(0, len(montes)):
        df_row = montes.iloc[k]
        df_date = df_row['Decimal_date']

        if sample_date == df_date:
            D14C_ref2s_mean.append(df_row['D14C_ref2s_mean'])
            D14C_ref2s_std.append(df_row['D14C_ref2s_std'])
            D14C_ref2t_mean.append(df_row['D14C_ref2t_mean'])
            D14C_ref2t_std.append(df_row['D14C_ref2t_std'])
            D14C_ref3s_mean.append(df_row['D14C_ref3s_mean'])
            D14C_ref3s_std.append(df_row['D14C_ref3s_std'])
            D14C_ref3t_mean.append(df_row['D14C_ref3t_mean'])
            D14C_ref3t_std.append(df_row['D14C_ref3t_std'])

samples['D14C_ref2s_mean'] = D14C_ref2s_mean
samples['D14C_ref2s_std'] = D14C_ref2s_std
samples['D14C_ref2t_mean'] = D14C_ref2t_mean
samples['D14C_ref2t_std'] = D14C_ref2t_std
samples['D14C_ref3s_mean'] = D14C_ref3s_mean
samples['D14C_ref3s_std'] = D14C_ref3s_std
samples['D14C_ref3t_mean'] = D14C_ref3t_mean
samples['D14C_ref3t_std'] = D14C_ref3t_std

samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/samples_with_references10000.xlsx')

