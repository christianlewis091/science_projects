import numpy as np
import matplotlib.pyplot as plt


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

# --- GEOMETRY ---
theta = np.pi/2   # 90 deg sector
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


r = p / (abs(q) * B)     # THIS IS THE KEY LINE!
x_beam = r * np.sin(t)
y_beam = r * (1 - np.cos(t))

plt.figure(figsize=(7,9))

# Chamber arcs
plt.plot(y_in, x_in, "--", color="black") # label=f"Inner wall (R={R_in:.2f}\")")
plt.plot(y_out, x_out, "--", color="black") # label=f"Outer wall (R={R_out:.2f}\")")
plt.plot(y_beam, x_beam, "-", color="red", label='14C-') # label=f"Outer wall (R={R_out:.2f}\")")

plt.show()

