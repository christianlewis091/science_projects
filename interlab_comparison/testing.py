from X_my_functions import d14C_to_fm
import pandas as pd

df = pd.read_excel(r'H:\The Science\Datasets\function_testing.xlsx')  # import Baring Head data
x = d14C_to_fm(df['D14C'], df['D14C_err'], 2020)

FM_out = x[0]
FM_err_out = x[1]

df['FM_out'] = FM_out
df['FM_out_err'] = FM_err_out
df.to_excel('function_testing_check.xlsx')

