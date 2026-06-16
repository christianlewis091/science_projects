import numpy as np
import random
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

df = pd.read_excel(r'H:\The Science\Datasets'
                           r'\prescaling2.xlsx')


df['TW'] = pd.to_numeric(df['TW'], errors = 'coerce')
df = df .loc[(df['TW'] < 5000)]
x = df['TW']
cat = df['cat']
FC01 = df['FC01']
FC03 = df['FC01']
FC04 = df['FC01']
FC05 = df['FC01']
FC06 = df['FC01']

FC03_1 = df['FC03/01']
FC04_3 = df['FC04/03']
FC05_4 = df['FC05/04']
FC06_5 = df['FC06/05']
FC04_1 = df['FC04/01']
FC06_4 = df['FC06/04']
FC06_1 = df['FC06/01']

fig, axs = plt.subplots(2, 5, figsize=(20, 8))
axs[0, 0].scatter(x, FC03_1, label='FC03/01')
axs[0, 0].set_title("FC03/01")
# axs[0, 0].set_ylim(-20, 20)

axs[0, 1].scatter(x, FC04_3, label='FC04/03')
axs[0, 1].set_title("FC04/03")
# axs[0, 1].set_ylim(-20, 20)

axs[0, 2].scatter(x, FC05_4, label='FC05/04')
axs[0, 2].set_title("FC05/04")
# axs[0, 0].set_ylim(-20, 20)

axs[0, 3].scatter(x, FC06_5, label='FC06/05')
axs[0, 3].set_title("FC06/05")
# axs[0, 0].set_ylim(-20, 20)

axs[0, 4].scatter(x, FC04_1, label='FC04/01')
axs[0, 4].set_title("FC04/01")
# axs[0, 0].set_ylim(-20, 20)

axs[1, 1].scatter(x, FC06_4, label='FC06/04')
axs[1, 1].set_title("FC06/04")
# axs[0, 0].set_ylim(-20, 20)

axs[1, 2].scatter(x, FC06_1, label='FC06/01')
axs[1, 2].set_title("FC06/01")
# axs[0, 0].set_ylim(-20, 20)
plt.show()
#
# ##################################################################################
#
# # fig, axs = plt.subplots(2, 5, sharex=True, sharey=True, figsize=(20, 8))
# # plt.scatter(x, FC03_1, label='FC03/01')
# # plt.scatter(x, FC04_3, label='FC04/03')
# # plt.scatter(x, FC05_4, label='FC05/04')
# # plt.scatter(x, FC06_5, label='FC06/05')
# # plt.scatter(x, FC04_1, label='FC04/01')
# # plt.scatter(x, FC06_4, label='FC06/04')
# # plt.scatter(x, FC06_1, label='FC06/01')
# # plt.legend
# # plt.show()
# # plt.close()