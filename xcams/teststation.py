import pandas as pd
from scipy import stats
import os

output_file = r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_2_2026_output\test.xlsx'
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Example datasets
group1 = [10, 12, 9, 11, 13]
group2 = [8, 7, 10, 6, 9]

group3 = [5, 6, 7, 8, 9]
group4 = [4, 5, 6, 7, 8]

results_lines = []

# First t-test
t1, p1 = stats.ttest_ind(group1, group2)
results_lines.append(
    f"The results are t={t1:.3f} and p={p1:.4f} for Group1 vs Group2."
)

# Second t-test
t2, p2 = stats.ttest_ind(group3, group4)
results_lines.append(
    f"The results are t={t2:.3f} and p={p2:.4f} for Group3 vs Group4."
)

# Convert to DataFrame (each sentence becomes its own row)
results_df = pd.DataFrame({"Results": results_lines})

# Write to Excel
with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
    results_df.to_excel(writer, sheet_name="T_Test_Results", index=False)

print("Results written!")









# import pandas as pd
# from scipy import stats
#
# # Example data
# group1 = [10, 12, 9, 11, 13]
# group2 = [8, 7, 10, 6, 9]
#
# # Run independent t-test
# t_stat, p_value = stats.ttest_ind(group1, group2)
#
# # Format output using f-strings
# results_dict = {
#     "t_statistic": [t_stat],
#     "p_value": [p_value],
#     "summary": [f"t = {t_stat:.3f}, p = {p_value:.4f}"]
# }
#
# results_df = pd.DataFrame(results_dict)
#
# # Write to new Excel sheet
# output_file = f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2026_output/test.xlsx'
#
# with pd.ExcelWriter(output_file, engine="openpyxl", mode="w") as writer:
#     results_df.to_excel(writer, sheet_name="T_Test_Results", index=False)
#
# print("Results written to new sheet!")