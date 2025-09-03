import numpy as np
import matplotlib.pyplot as plt
from math import pi

# --- MAGNET GEOMETRY ---
theta_scale = 1
theta = (np.pi/2)*theta_scale   # 90 deg sector
bore = 0.0635   # 2.5 inches
half_bore = bore/2
R_ref = 0.3048     # 12 inches # set design radius to computed bend radius
R_in = R_ref - half_bore
R_out = R_ref + half_bore

# Build chamber arcs
t = np.linspace(0, theta, 500)
x_in = R_in * np.sin(t) # x value for inner wall
x_out = R_out * np.sin(t) # x value for magent chamber outer wall
y_in = R_ref - R_in * np.cos(t) # y value for inner wall
y_out = R_ref - R_out * np.cos(t) # y value for outer wall

"""
In non-forced pathway, we set the magnet up using the physical equations/Lorentz Force. 
# --- PHYSICS ---
eV = 58000        # beam energy in eV
e = 1.602e-19     # C
Bounce = 0.5 # .5kV on the bounce for 14C
E = (eV+Bounce) * e        # J
mu = 1.66e-27     # kg
A = 14          # mass number
m = A * mu        # kg
p = np.sqrt(2*m*E)
z = -1
q = z * e         # charge
B = 4200 / 1e4    # Gauss → Tesla # This is our injection magnet voltage changes to Tesla, 10,000 Gauss = 1 Tesla
and use this equation to draw the arc: 

r = p / (abs(q) * B)     # THIS IS THE KEY LINE!
x_beam = r * np.sin(t)
y_beam = r * (1 - np.cos(t))

In the forced pathway (we force 14C through the center of the exit), we use a different set of equations. 

"""

plt.figure(figsize=(7,7))

# Chamber arcs
plt.plot(y_in, x_in, "--", color="black") # label=f"Inner wall (R={R_in:.2f}\")")
plt.plot(y_out, x_out, "--", color="black") # label=f"Outer wall (R={R_out:.2f}\")")
plt.axhline(y=0.3048, color="black", linestyle="-", label="viewing cross", alpha=0.15)
plt.axvline(x=0, color="black", linestyle="-", alpha=0.15)


# Species: (label, mass A, |q|, mark_wall)
species = [12,13,14, 55.845, 26]
label=['12C-','13C-','14C-','56Fe-','26Al']
colors = ['blue','yellow','green','red','brown']
og_size = 1
ss = [og_size, og_size, og_size, 2*og_size, og_size]
for i in range(0, len(species)):
    # R ref
    atom_ref = 14 # WE SET REFERENCE OF MASS 14 AS CENTERING EXIT
    # For other ions, it is scaled as sqrt(A/14q). For instance, 56Fe would be sqrt(56/(14*-1)) = 2.
    A = 14 # mass number of interest
    q = -1
    radius = np.sqrt(species[i] / (atom_ref * abs(q))) * R_ref  # radii are scaled to mass 14.
    x_beam = radius * np.sin(t)
    y_beam = radius * (1 - np.cos(t))

    plt.plot(y_beam, x_beam, "-", color=f'{colors[i]}', label=f'{label[i]}',  linewidth=ss[i]) # label=f"Outer wall (R={R_out:.2f}\")")

# arc length = 2pir*(theta/360)
arclength = 0.0356 #35.6cm
theta = arclength/0.33655
s = [0.387, 0.4435, 0.4955] # Hayden's measurement
h = .17 # distance between flight tube and beginning of B field
for j in range(0, len(s)):
    theta_1 = (s[j]-h) / R_out  # in radians

    x_point = R_out * np.sin(theta_1)
    y_point = R_ref - R_out * np.cos(theta_1)

    plt.scatter(y_point, x_point, color='black', marker='X', s=100, label='outer_wall_erosions')  # mark the point at s=0.356 m

# Show plot
plt.legend()
plt.xlim(-0.05, 0.35)
plt.ylim(-0.05,0.35 )
# plt.show()
plt.savefig(r"I:\XCAMS\4_maintenance\13_Beamline_Realignment\re-alignment of beamlines Sep 2025\Hands-on\September_1_2025\beam_overlay.png", dpi=300, bbox_inches="tight")
plt.close()

