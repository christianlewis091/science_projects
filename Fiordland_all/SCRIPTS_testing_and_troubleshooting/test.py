import matplotlib.pyplot as plt
import numpy as np

# mass balance end-member mixing model for conference
import pandas as pd

m = 24  # measured value
d1 = -30 # terrestrial end-member
d2 = 30  # marine end-member

f1 = (m-d2)/(d1-d2)
f2 = 1-f1

tDIC = 2.2 # mmol/kg
x = (tDIC*f1)
x = round(x,2)

# CH2O + O2 -> CO2 + H20
consumed = x*32  # 02 = 32 g/mol

print(f"With measured Delta14C of {m}, marine and terrestrial DIC end-members of {d2} and {d1} respectively, terrestrial fraction is {f1}")
print(f"With [DIC] of {tDIC} total, {f1} terrestrial fraction means {x} came from remineralization")
print()
print(f"In a simplified system, one can assume one mol of CO2 made from each mol of O2")
print(f"{consumed} mg/L O2 consumed")

# an terrestrial end-member of 0 overestiamtes oxygen utilization, it would be even lower
# lets do a quick model...
#
# t_ends = np.linspace(-100, 30, 40)
# res = []
# for i in range(0, len(t_ends)):
#     # mass balance end-member mixing model for conference
#     m = 24  # measured value
#     d1 = t_ends[i]  #terrestrial end-member
#     d2 = 30  # marine end-member
#
#     f1 = (m-d2)/(d1-d2)
#     f2 = 1-f1
#
#     tDIC = 2.2 # mmol/kg
#     x = (tDIC*f1)
#     x = round(x,2)
#
#     # CH2O + O2 -> CO2 + H20
#     consumed = x*32  # 02 = 32 g/mol
#     res.append(consumed)
#
# # results = pd.DataFrame({"T_end": t_ends, "O2_resp": res})
# plt.scatter(t_ends, res)
# plt.axhline(y=(8-1))
# plt.show()
#
#








