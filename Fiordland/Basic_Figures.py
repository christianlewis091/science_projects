import pandas as pd

df = pd.read_excel('H:/Science/Current_Projects/03_CCE_24_25/02_SPEDOC/SPE_Processing_and_Data.xlsx', sheet_name='Cruise_Data_Sheet_ALL', comment='#')
df = df.loc[df['Qflag'] != '.X.']

tannic = df.loc[(df['STD_ONLY_type'] == 'tannic acid')]
salicylic = df.loc[(df['STD_ONLY_type'] == 'salicylic acid')]

