import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
df = df.loc[df['Job::R'] == '26294/1']
print(df)

plt.scatter(df['wtgraph'], df['RTS_corrected'])
plt.show()