import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# Create a figure and a set of subplots
fig, ax = plt.subplots()

# Set the x and y scales to logarithmic
ax.set_xscale('log')
ax.set_yscale('log')

# Set the limits for x and y axes
ax.set_xlim(0.001, 10)
ax.set_ylim(0.0001, 1)

# Add labels to the axes
ax.set_xlabel('Sample Size (mg)')
ax.set_ylabel('Ratio to OX-1')
ax.xaxis.set_major_formatter(ScalarFormatter())
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.xaxis.get_major_formatter().set_scientific(False)
ax.yaxis.get_major_formatter().set_scientific(False)
# Add a grid for better readability
ax.grid(True, which="both", ls="--")

# add the diagonal lines
x = [0.001, 10]
y1 = [0.2, .00002]
y2 = [0.3, .00003]
y3 = [0.4, .00004]
y4 = [0.5, .00005]
y5 = [0.6, .00006]
y6 = [0.8, .00008]
y7 = [1, .0001]
y8 = [2, .0002]
y9 = [5, .0005]
ys = [y1, y2, y3, y4, y5, y6, y7, y8, y9]
labels = ['0.2','0.3','0.4','0.5','0.6','0.8','1','2','5']
for i in range(0, len(ys)):
    plt.plot(x, ys[i], label=f'{labels[i]}')

plt.legend()
# Show the plot
plt.show()
