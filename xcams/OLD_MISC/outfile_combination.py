"""

I want this script to combine outfiles that I select for comination
"""
import pandas as pd

dir1 = [r'I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3500-3549\TW3507\TW3507_p1.out']
# dir2 = []
# dir3 = []

pd.read_csv(dir1, delim_whitespace=True).to_excel('output_file.xlsx', index=False)
# df = pd.read_csv(dir1, delim_whitespace=True)
# print(df)