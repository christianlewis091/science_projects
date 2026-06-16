"""
Space for troubleshooting
"""
"""
1. Why do I have LESS BHDAmb when I include MORE time? 
"""
import pandas as pd
v6 = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output\Final_results_V6.xlsx", sheet_name='Clean Dataset')
v05 = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\Final_results_May202025_stderror.xlsx", sheet_name='Clean Dataset')

listv6 = v6.loc[v6['Job::R'] == '40430/1']
listv05 = v05.loc[v05['Job::R'] == '40430/1']

# lists
list6 = listv6['TP']
list05 = listv05['TP']

# convert to sets (drop NaNs just in case)
set1 = set(list6.dropna())
set2 = set(list05.dropna())

# differences
only_in_list1 = set1 - set2
only_in_list2 = set2 - set1

print("Only in list6:")
print(sorted(only_in_list1))

print("\nOnly in list05:")
print(sorted(only_in_list2))
