"""
Hi Jocelyn,

I’m moving this to a smaller group as the discussion bends away from the specifics of MQA and more broadly to SH D14C.

Do you have a plot of the difference between Campbell and Chile D14C over time, with Heidelberg MQA thrown on for good measure?
Maybe even better, if you provide the data as a file I could plot DRP, MQA and also Chile and Campbell tree values.
It would be interesting to see how they line up relative to one another.

Re intercomparibility, apologies if you shown this already, but could you or Christian share your analysis re INSTAAR minus Heidelberg?

Thanks,

John
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/complete_samples.xlsx')

campbell = df.loc[df['Site'] == 'World\'s Loneliest Tree, Camp Cove, Campbell island']
chile1 = df.loc[df['Site'] == 'Bahia San Pedro, Chile']
chile2 = df.loc[df['Site'] == 'Baja Rosales, Isla Navarino']
chile3 = df.loc[df['Site'] == 'Puerto Navarino, Isla Navarino']
chile4 = df.loc[df['Site'] == 'Raul Marin Balmaceda']
chile5 = df.loc[df['Site'] == 'Seno Skyring']
mcq = df.loc[df['Site'] == 'MCQ']

c1, c2, c3 = '#d73027', '#fdae61', '#1c9099'
markers = ['o','v','8','s','p','+','x','D']







fig, axs = plt.subplots(2, sharex=True)
fig.subplots_adjust(hspace=0.5)

fig.suptitle('Raw Data; Cambell Island & Chile (1 site only) (Tree Rings), and Macquarie Island (NaOH CO2)')
axs[0].scatter(campbell['Decimal_date'], campbell['D14C'], marker = 'o', label='Cambell Island', color=c1)
axs[0].scatter(chile2['Decimal_date'], chile2['D14C'], marker = 'D', label='Baja Rosales, Isla Navarino', color=c2)
axs[0].scatter(mcq['Decimal_date'], mcq['D14C'], marker = 's', label='Macquarie Island', color=c3)
axs[0].set_xlim(1980, 2022)
axs[0].set_ylim(0, 300)

fig.suptitle('Difference to Southern Hemisphere Background (Baring Head)')
axs[1].scatter(campbell['Decimal_date'], campbell['D14C'], marker = 'o', label='Cambell Island', color=c1)
axs[1].scatter(chile2['Decimal_date'], chile2['D14C'], marker = 'D', label='Baja Rosales, Isla Navarino', color=c2)
axs[1].scatter(mcq['Decimal_date'], mcq['D14C'], marker = 's', label='Macquarie Island', color=c3)
axs[1].set_xlim(1980, 2022)
axs[1].set_ylim(0, 300)





# plt.ylabel('\u039414C (\u2030)')


plt.show()
















