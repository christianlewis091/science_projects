import pandas as pd

samples = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/complete_samples.xlsx')
montes = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/monte_output10000.xlsx')

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
    sample_date = samples_row['Decimal_date']

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

samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/samples_with_references.xlsx')

