import pandas as pd

df = pd.read_excel(r'H:\Science\Datasets\RICE_IC_26901_27020.xlsx')
filtered_df = df[df['Injection Name'].str.contains("RICE")]
filtered_df.to_excel(r'H:\Science\Datasets\RICE_IC_26901_27020_RICE.xlsx')
print(filtered_df)
#
# dataf = pd.DataFrame()



# for i in range(0, len(df)):
#     row = df.iloc[i]
#     query = str(row['Injection Name'])
#     if 'RICE' in query:
#         print('yes')
#         new_data = pd.concat([dataf, row])
# new_data.to_excel(r'H:\Science\Datasets\RICE_IC_26901_27020_RICEonly.xlsx')

    # print(row)

#
# # df = df.loc[df['Injection Name'].isin('RICE')]
# new = df['Injection Name'].isin(["RICE"])
# new.to_excel(r'H:\Science\Datasets\RICE_IC_26901_27020_RICE.xlsx')