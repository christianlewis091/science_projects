# check to see how much error to add to 3580
import numpy as np

ox = np.array([1.0334, 1.0376, 1.03989, 1.04442, 1.04047, 1.04198])
unc = np.array([.00234, .00239, 0.0225, 0.00226, 0.00228, 0.00223])
wmean_num = np.sum(ox/unc**2)
wmean_dem = np.sum(1/ox**2)
wmean = wmean_num / wmean_dem
"""
Optomize Chi2 to find sigma_residual
"""
sig_res = np.linspace(0.00001, 0.010, 100)

# Variables to store the best result
best_sig_res = None
closest_chi2_red = float('inf')
target_chi2_red = 1.0

for i in range(len(sig_res)):
    # Calculate chi2_red for the current sig_res
    chi2_red_num = np.sum((ox-wmean)**2 / (unc**2 + sig_res[i]**2))
    chi2_red_denom = len(ox)-1
    chi2_red = chi2_red_num / chi2_red_denom

    # Check if this chi2_red is closer to 1
    if abs(chi2_red - target_chi2_red) < abs(closest_chi2_red - target_chi2_red):
        closest_chi2_red = chi2_red
        best_sig_res = sig_res[i]

print(best_sig_res)
print(closest_chi2_red)