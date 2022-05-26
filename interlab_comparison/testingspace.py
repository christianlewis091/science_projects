import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

array = []
for i in range(0,10000):
    rand = np.random.normal(10, 2, size=None)
    array.append(rand)

print(array)
plt.hist(array, bins=100)
plt.show()


# testing the first for loop

df = pd.read_excel(r'H:\The Science\Datasets\my_functions_examples'
                   r'\monte_carlo_loop1_test.xlsx')  # import the data
# x = df['DEC_DECAY_CORR']
# y = df['DELTA14C']
# y_err = df['DELTA14C_ERR']
x = df['test_x']
y = df['test_y']
y_err = df['test_y_err']
# def monte_carlo_randomization_trend(x_init, y_init, y_error, fake_x, cutoff, n):
new_df = monte_carlo_randomization_trend(x, y, y_err, x, 667, 10)
new_df.to_excel('testing_monte_carlo.xlsx')

rand1 = new_df.iloc[1]
rand1 = new_df.iloc[2]
rand2 = new_df.iloc[3]
rand3 = new_df.iloc[4]
rand4 = new_df.iloc[5]


colors = sns.color_palette("rocket", 6)
colors2 = sns.color_palette("mako", 6)
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['font.size'] = 10
size1 = 5

plt.errorbar(x, y, yerr=y_err, fmt='o', color='black', ecolor='black', elinewidth=1, capsize=2)
plt.scatter(x, rand1, color=colors[0], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
plt.scatter(x, rand2, color=colors[1], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
plt.scatter(x, rand3, color=colors[2], label='Monte Carlo Iteration 1', alpha=0.35, marker='x')
plt.scatter(x, rand4, color=colors[3], label='Monte Carlo Iteration 2', alpha=0.35, marker='^')
plt.show()

