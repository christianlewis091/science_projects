import pandas as pd
import numpy as np
import random

random_numbers = [random.random() for _ in range(10000)]
df = pd.DataFrame({'B': random_numbers})
x = df.rolling(500).sum()
x = x.dropna
print(x)

