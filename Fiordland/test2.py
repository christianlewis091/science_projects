import pandas as pd
import numpy as np

# df = pd.read_excel(f'C:/Users/clewis/IdeaProjects/tiller.xlsx', sheet_name='Transactions')
# df  = df[df['Description'].str.contains('Lynette', case=False, na=False)].reset_index(drop=True)
piano = 1215

# with 12 months of $150 allowance/month, this is
tot_allowance = 12*150
print(tot_allowance)
