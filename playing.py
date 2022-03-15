import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cdc = pd.read_csv(r'C:\Users\lewis\Desktop\cdc.csv')
# df = df.drop(columns=['Column Names that I want to drop'], axis = 1)
cdc = cdc.drop(columns=['INDICATOR', 'PANEL_NUM', 'UNIT', 'UNIT_NUM', 'STUB_NAME',
                        'STUB_NAME_NUM', 'STUB_LABEL', 'STUB_LABEL_NUM', 'YEAR_NUM',
                        'AGE', 'AGE_NUM', 'SE', 'FLAG'], axis=1)
print(cdc)
food_allergy = cdc.loc[cdc['PANEL'] == 'Food allergy among persons under 18 years']
percent = food_allergy['ESTIMATE']
time = food_allergy['YEAR']
print(percent)

print(cdc.columns)



colors = sns.color_palette("rocket")
size = 5
alpha1 = 0.4
plt.plot(percent, color=colors[0], alpha=alpha1)
plt.xlabel('Date', fontsize=14)
plt.ylabel('\u0394 14CO2', fontsize=14)  # label the y axis
plt.show()
plt.close()