import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Circle placement parameters (left subplot)
n_circles = 8
radius = 1.0
circle_size = 0.1

angles = np.linspace(0, 2*np.pi, n_circles, endpoint=False)
circle_centers = [(radius*np.cos(a), radius*np.sin(a)) for a in angles]

# List of positions for the moving circle
positions = [(.5,-.5), (.5,-.5), (-.5,.75), (0.25,.3), (-.3,.3)]
circle_radius = 0.8

# For mapping each position -> list of circles on left to highlight
# (example: indices between 0 and n_circles-1)
highlight_indices = [
    [0],        # Step 0 -> highlight circle 0
    [5],     # Step 1 -> highlight circles 1 & 2
    [4, 5],        # Step 2 -> highlight circle 4
    [6],     # Step 3 -> highlight circles 6 & 7
    [6],  # Step 4 -> highlight circles 3, 5 & 7
]

# --- Setup figure ---
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
plt.subplots_adjust(bottom=0.25)  # leave room for slider

# Left subplot: 8 circles
ax = axes[0]
left_circles = []
for (cx, cy) in circle_centers:
    circ = plt.Circle((cx, cy), circle_size, color="skyblue", ec="k")
    ax.add_patch(circ)
    left_circles.append(circ)

big_circle = plt.Circle((0, 0), radius, fill=False, ls="--", color="gray")
ax.add_patch(big_circle)
ax.set_aspect("equal")
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
ax.set_title("8 circles around a circle")

# Right subplot: crosshair + movable circle
ax2 = axes[1]
ax2.axhline(0, color="gray", lw=1)
ax2.axvline(0, color="gray", lw=1)
ax2.set_aspect("equal")
ax2.set_xlim(-2, 2)
ax2.set_ylim(-2, 2)
ax2.set_title("Crosshair + movable circle")

# Circle to move
movable_circle = plt.Circle(positions[0], circle_radius, color="tomato", alpha=0.5)
ax2.add_patch(movable_circle)

# --- Slider setup ---
ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])  # x, y, width, height
slider = Slider(ax_slider, 'Step', 0, len(positions)-1, valinit=0, valstep=1)

# Update function for slider
def update(val):
    idx = int(slider.val)

    # Move right circle
    x, y = positions[idx]
    movable_circle.center = (x, y)

    # Reset all circles to default color
    for circ in left_circles:
        circ.set_facecolor("skyblue")

    # Highlight chosen ones
    for hi in highlight_indices[idx]:
        left_circles[hi].set_facecolor("orange")

    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()
