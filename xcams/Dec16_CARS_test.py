import matplotlib.pyplot as plt

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 3))

# Plot three number lines
for i, label in enumerate(['X', 'Y', 'Z']):
    ax.hlines(y=i, xmin=-3, xmax=3, color='black', linewidth=1)
    ax.text(-3.5, i, label, fontsize=12, ha='center', va='center')
#
# # Add ticks
# for x in range(-3, 4):
#     for i in range(3):
#         ax.plot(x, i, 'o', color='black', markersize=3)

# Customize the plot
ax.set_xlim(-4, 4)
ax.set_ylim(-1, 3)
# ax.axis('off')

plt.show()
