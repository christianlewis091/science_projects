

data = [[1, 2, 3, 4],
        [1, 2, 3, 4],
        [1, 2, 3, 4]]
table2 = (tabulate(data, headers=["Label", "Label", "Average", "Std Error / Prop Error"]))
df = pd.DataFrame(data=data)
print(df)
print(table2)




