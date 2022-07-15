import pandas as pd


df = pd.read_excel(r'C:\Users\clewis\IdeaProjects\GNS\radiocarbon_intercomparison\Interlab_comparison\Results_table_for_pub.xlsx')  # import data

x = df.pivot_table(index=['Time Period'], columns=['Rafter - Heidelberg'])
print(x)