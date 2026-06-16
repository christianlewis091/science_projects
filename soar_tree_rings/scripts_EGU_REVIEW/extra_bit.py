import pandas as pd
import numpy as np

# Load data
ref2 = pd.read_excel(
    r"C:\Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_REVIEW\Data_Files\FINAL_DATA_JAN3_2025\harmonized_dataset.xlsx"
)

# --- Filter using .loc ---
df = ref2.loc[ref2['Decimal_date'] > 2010]

# --- Fit a line: D14C = m * decimal_date + b ---
# Use polyfit (degree=1) → returns slope, intercept
slope, intercept = np.polyfit(df['Decimal_date'], df['D14C'], 1)

print("Slope:", slope)
print("Intercept:", intercept)
print(max(df['Decimal_date']))