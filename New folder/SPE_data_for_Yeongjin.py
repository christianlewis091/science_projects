import pandas as pd
import numpy as np

# THIS IS THE FILE THAT WAS PUBLISHED, WITH ALL THE ISOTOPE DATA, CONCENTRATIONS, ETC
open_acc = pd.read_excel(r"H:\Science\Current_Projects\07_Collaborations\Yeongjin_HK_2026\OPEN_ACCESS_DATA_FILE.xlsx", sheet_name='Data', comment='#')

# THIS FILE HAS THE CONCENTrATIONS OF SPE-DOC IN METHANOL
mets = pd.read_excel(r"H:\Science\Current_Projects\07_Collaborations\Yeongjin_HK_2026\Data_to_share.xlsx")
# get rid of the parenthetical notes from the open access file

df = pd.merge(mets, open_acc, on='SPE-DOC UCID (formerge)', how='outer', indicator=True)

print(df['_merge'].value_counts())
df.to_excel(r"H:\Science\Current_Projects\07_Collaborations\Yeongjin_HK_2026\TEST.xlsx")
