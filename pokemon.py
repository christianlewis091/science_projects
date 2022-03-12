import pandas as pd
import re
# import the data from the excel sheet...
df = pd.read_csv(r'C:\Users\lewis\Google Drive\Work'
                   r'\GNS Radiocarbon Scientist\The Science'
                   r'\Stats and Data Analysis\MATLAB Methods'
                   r'\pokemon_data.csv')
# print(df)
# print(df.head(3)) # print top 3 rows
# print(df['Name']) # prints a list of that column
# print(df[['Name','Type 1', 'HP']])
# print(df.iloc[2,1])
# for index, row in df.iterrows():
#     print(index, row['Name'])
Fire = df.loc[df['Type 1'] == "Fire" ]
print(Fire)
# df.sort_values(['Type 1', 'HP'], ascending=[1,0]) Sort values
# print(df)
# https://www.youtube.com/watch?v=vmEHCJofslg&t=399s&ab_channel=KeithGalli
# Add a new column based on doing some math with the other values....

# df['Total'] = df['HP'] + df['Attack'] + df['Defense'] + df['Sp. Atk'] + df['Sp. Def'] + df['Speed']

# df.head(5)
# df = df.drop(columns=['Total'])
# print(df)
# df.to_csv('modified.csv') # move back to csv file


# MORE ADVANCED FILTERING OF DATA

# df.loc[(df['Type 1'] == 'Grass') & (df['Type 2'] == 'Poison')] # filtering based on two types of data AND
# df.loc[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Poison')] # filtering based on two types of data OR
# df.loc[df['Type 1'] == "Fire" ]
# Filter = df.loc[(df['Type 1'] == 'Grass') & (df['Type 2'] == 'Poison') & (df['HP'] > 70)]
# Filter = Filter.reset_index()
#
#
# # Filter = df.loc[(df['Name'].str.contains('Mega'))] #filter all data that contains the word mega
#
# Filter = df.loc[df['Type 1'].str.contains('Fire|Grass', flags = re.I, regex = True)]
#
# print(Filter)
