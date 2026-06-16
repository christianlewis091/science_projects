import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

df = pd.read_excel(rf"C:\Users\clewis\IdeaProjects\GNS/xcams\Data_Quality_Version_6\output\Data_quality_paper_2_V6_output/Final_results_V6_edit2.xlsx", sheet_name='Clean Dataset')

df = df.loc[df['Job::R'] == '40430/3']

df['1om'] = 1/df['wtgraph']


mean1 = np.mean(df['RTS_corrected'])
plt.scatter(df['1om'],df['RTS_corrected'])
print(f'mean is {mean1}')

plt.show()






















