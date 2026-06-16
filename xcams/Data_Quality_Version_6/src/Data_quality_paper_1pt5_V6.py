"""
I need to verify that I'm getting the same results as Jocelyn. 
So I'm going to send her the list of TP numbers that are used in my analysis. 
"""
import pandas as pd
import matplotlib.pyplot as plt


# # READ IN THE DATASETS THAT WE'LL BE USING HERE!
df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_1_V6_output\13_manual_drop.xlsx", sheet_name= 'Whole Dataframe')

air_r = ['40430/1','40430/2','40430/5']
inor_r = ['41347/2','41347/3']
water_r = ['41347/12','41347/13']
organic_r = ['24889/4','24889/5','24889/7','24889/9']
rpo_r = ['24889/14']
bone_r = ['26281/1']

air_materials = df.loc[(df['Job::R'].isin(air_r))].copy()

# air_materials.to_excel(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_1pt5_V6_output/airmaterials.xlsx")
bhdamb2013 = air_materials.loc[air_materials['Job::R'] == '40430/1']
bhdspike2013 = air_materials.loc[air_materials['Job::R'] == '40430/2']
bhdspike2025 = air_materials.loc[air_materials['Job::R'] == '40430/5']

# Function to get TP lists
def get_tp_lists(df):
    keep_tp = df.loc[df['Keep_Remove'] == 'Keep', 'TP'].tolist()
    remove_tp = df.loc[df['Keep_Remove'] == 'Remove', 'TP'].tolist()
    return keep_tp, remove_tp

# Get lists for each dataset
amb_keep, amb_remove = get_tp_lists(bhdamb2013)
spike2013_keep, spike2013_remove = get_tp_lists(bhdspike2013)
spike2025_keep, spike2025_remove = get_tp_lists(bhdspike2025)

print('BHDamb2013 Removed')
print(amb_remove)
print()
print('BHDspike2013 Removed')
print(spike2013_remove)
print()
print('BHDspike2025 Removed')
print(spike2025_remove)

"""
Jocelyn wants to check manual outliers that I've selected; I want to make sure I'm not crazy ; lets plot them and see: 
"""
bhdamb2013 = air_materials.loc[air_materials['Job::R'] == '40430/1']
bhdamb2013_keep = air_materials.loc[(air_materials['Job::R'] == '40430/1') & (air_materials['Keep_Remove'] == 'Keep')]
bhdamb2013_remove = air_materials.loc[(air_materials['Job::R'] == '40430/1') & (air_materials['Keep_Remove'] == 'Remove')]
bhdamb2013_hardflag = air_materials.loc[(air_materials['Job::R'] == '40430/1') & (air_materials['Comment'] == 'Hard Flag Found. Set for removal')]
bhdamb2013_plotlyout = air_materials.loc[(air_materials['Job::R'] == '40430/1') & (air_materials['Comment'] == 'Manual outlier found using plotly, see plot. Sept 19, 2025 CBL')]
bhdamb2013_V6out = air_materials.loc[(air_materials['Job::R'] == '40430/1') & (air_materials['Comment'] == 'Extra drops in V6 beacuse new outliers are found with new data added, see comments in script')]

plt.figure()

plt.scatter(bhdamb2013_keep['TP'], bhdamb2013_keep['F_corrected_normed'], label='Keep')
plt.scatter(bhdamb2013_remove['TP'], bhdamb2013_remove['F_corrected_normed'], label='Remove')
plt.scatter(bhdamb2013_hardflag['TP'], bhdamb2013_hardflag['F_corrected_normed'], label='Hard Flag')
plt.scatter(bhdamb2013_plotlyout['TP'], bhdamb2013_plotlyout['F_corrected_normed'], label='Plotly outliers')
plt.scatter(bhdamb2013_V6out['TP'], bhdamb2013_V6out['F_corrected_normed'], label='V6outliers')

plt.xlabel('TP')
plt.ylabel('F_corrected_normed')
plt.legend()
plt.tight_layout()
plt.show()
plt.savefig(rf"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_Version_6\output\Data_quality_paper_1pt5_V6_output/Removeds.png", dpi=300, bbox_inches="tight")

