import matplotlib.pyplot as plt
import numpy as np

# Example data
x = np.linspace(0, 10, 100)
ys = [np.sin(x + i) for i in range(13)]

# Create figure and axes
fig, axes = plt.subplots(
    nrows=13, ncols=1,
    figsize=(6, 10),
    sharex=True,
    constrained_layout=False
)

# Adjust spacing between subplots
plt.subplots_adjust(hspace=0.05, left=0, right=1, top=1, bottom=0)

# Plot each subplot
for ax, y in zip(axes, ys):
    ax.plot(x, y, color='black', linewidth=1)
    ax.set_xlim(x.min(), x.max())

    # Remove all borders and ticks
    # ax.axis('off')

# # Optional: remove outer figure border
# for spine in fig.spines.values():
#     spine.set_visible(False)

plt.show()
