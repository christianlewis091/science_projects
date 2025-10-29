"""
October 28, 2025
This file was created because I need to re-do a lot of the previous work,
This is because the WTW error term is contained inside the F_corrected_normed_error.
This means we're double dipping when calculating sigma_res
I need to fix, streamline, and clean the older code to finally get this paper out.

Much of this will be taken from an older file which was moved to a new directory for clarity:
"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_OLD\Data_quality_Paper_3.py"
"""
import pandas as pd

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
df = df.loc[df['Keep_Remove'] == 'Keep']

"""
The first thing we'll do is tackle the sigma_residual question because it's going to be the most challenging
"""

# TODO adapt work from "C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Paper_OLD\Data_quality_Paper_3.py"
# TODO to recalculate sigma_res to get rid of WTW error