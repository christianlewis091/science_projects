"""
In V6 we've added data up to the present
Now that the analysis is complete in the previous file, 
I want to make it clear what the changes are, especially for the Air samples, which are the most impacted. 
"""

import pandas as pd

# read in the OLD RESULTS
df_old = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\Final_results_May202025_stderror.xlsx", sheet_name='Secondaries Statistics')
sig_old = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\sandbox_post_April3_meeting_output\Final_results_May202025_stderror.xlsx", sheet_name='Group Statistics')

# read in the new results 
df_new = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit2.xlsx", sheet_name='Secondaries Statistics')
sig_new = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit2.xlsx", sheet_name='Group Statistics')

# check changes between secondaries between old and new version
def check_changes(r):
    # Find the rows for Job::R == '40430/1'
    old_row = df_old[df_old['Job::R'] == r]
    new_row = df_new[df_new['Job::R'] == r]

    # Extract chi2reduced values
    old_chi2 = old_row['chi2red'].iloc[0]
    new_chi2 = new_row['chi2red'].iloc[0]

  # Extract len values
    old_len = old_row['n'].iloc[0]
    new_len = new_row['n'].iloc[0]

    # Print comparison
    print(f'for dataset {r}')
    print(f"Old dataset had {old_len} values with chi2reduced: {old_chi2}")
    print(f"New dataset had {new_len} values with chi2reduced: {new_chi2}")
    print()

# check changes between secondaries between old and new version
def sig_changes(group):
    # Find the rows for Job::R == '40430/1'
    old_row = sig_old[sig_old['Group'] == group]
    new_row = sig_new[sig_new['Group'] == group]
    
    # Extract chi2reduced values
    old_chi2 = old_row['Chi2 Reduced'].iloc[0]
    new_chi2 = new_row['Chi2 Reduced'].iloc[0]

  # Extract sig_pm
    old_sig = old_row['sigmabw_pm'].iloc[0]
    new_sig = new_row['sigmabw_pm'].iloc[0]

    # Print comparison
    print(f'for dataset {group}')
    print(f"Old {group} had {old_chi2} and sigbw of {old_sig}")
    print(f"New {group} had {new_chi2} and sigbw of {new_sig}")
    print()


check_changes('40430/1')
check_changes('40430/2')

sig_changes('Air')

