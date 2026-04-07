"""
April 7, 2026
I want to understand how much of the improvement in our Air materials data is due to simply having MORE DATA versus the actual
improvement of flask oxalics.
"
In the current period using normalization to flask oxalics we see a 44% and 26% reduction in chi2 for BHDamb and BHDspike (ex: 1-(2/1.13)),
a reduction of σbw  for air materials by almost half, and a decrease in total uncertainty by 0.4 to 0.5
"

We can potetnially do a bootstrap to test how good our data remains at the sample volume from jocelyn's last paper.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# grab the data output from the previous file:
df = pd.read_excel(f'C:/Users\clewis\IdeaProjects\GNS/xcams\sandbox_post_April3_meeting_output/Final_results.xlsx', sheet_name='Clean Dataset')

air_r = ['40430/1','40430/2']
air_materials = df.loc[(df['Job::R'].isin(air_r)) & (df['preptype'] == 'FLASK')].copy()

# convert ratio to standard to per mil, for instance for sigma_bw calculation
def rts_to_permille_for_errors(rts, colldate):
    rts_to_FM  = (np.sqrt(rts**2)/0.95)*0.98780499
    FM_to_permille = 1000*(rts_to_FM*np.exp((1950-colldate)/8267))
    return FM_to_permille

"""
WRAP STAGE ONE OF ANALYSIS (FROM LAST SCRIPT) INTO A FUNCTION
"""
def compute_sigmabw_bootstrap(df2, colldate1):

    wmean_num = np.sum(df2['RTS_corrected'] / df2['RTS_corrected_error']**2)
    wmean_den = np.sum(1 / df2['RTS_corrected_error']**2)
    wmean = wmean_num / wmean_den

    """
    Calculate chi2 reduced
    """
    chi2_red_num = np.sum((df2['RTS_corrected']-df2['wmean'])**2/df2['RTS_corrected_error']**2)
    chi2_red_denom = len(df2)-1 # subtract number of groups in degrees of freedom calc.
    chi2_red = chi2_red_num/chi2_red_denom

    """
    calculate sigma_bw striaght up (This is the turnbull 2015 method) (if this doesn't work, its beacuse the sqrt function went negative because chi2 was less than 1)
    See Eqn at bottom of page 1 of scan file:///I:/C14Data/Data%20Quality%20Paper/CBL_V3/Data_Quality_Eqns_CBL_JCT.pdf
    """
    if chi2_red < 1:
        # according to the eqn, if chi2 is less than 1,, you'd be taking sqrt of negative number which doesn't work. So if less than 1, set to 0.
        sigbw = 0
        print('I found a zero!')

    else:
        term2 = np.sqrt(chi2_red - 1)
        #term1 = np.nanmean(df2['RTS_corrected_error'])
        term1 = np.nanmean(df2['RTS_corrected_error'])/np.nanmean(df2['RTS_corrected']) # TODO here I think is where we would put a normalization to FM/RTS
        # TODO when thinking about where to put that normalization to RTS_corrected (line above), it must be there, it one put it below, one would be normalizing
        # TODO multiple grouped sigma_bw values to one RTS, it would be too late.
        sigbw = term1*term2

    sigbw_pm = (rts_to_permille_for_errors(sigbw, colldate1))

    return {
        "wmean": wmean,
        "chi2_red": chi2_red,
        "sigbw_rts": sigbw,
        "sigbw_pm": sigbw_pm
    }

"""
APPLY THAT FUNCTION IN A BOOTSTRAP
"""

colldate1 = air_materials['Collection Date_y'].iloc[0]

n_boot = 100
sample_size = 40

bootstrap_results = []

for b in range(n_boot):
    sample = air_materials.sample(n=sample_size, replace=False)

    metrics = compute_sigmabw_bootstrap(sample, colldate1)
    metrics["bootstrap_iter"] = b

    bootstrap_results.append(metrics)

bootstrap_df = pd.DataFrame(bootstrap_results)

"""
GET SUMMARY DATA FROM THE BOOTSTRAP 
"""

summary = bootstrap_df.agg({
    "wmean": ["mean", "std"],
    "chi2_red": ["mean", "std"],
    "sigbw_rts": ["mean", "std"],
    "sigbw_pm": ["mean", "std"]
})

print(summary)

"""
SANITY CHECK PLOTS
"""

plt.figure()
plt.hist(bootstrap_df["sigbw_pm"], bins=20)
plt.axvline(bootstrap_df["sigbw_pm"].mean())
plt.title("Bootstrap distribution of σ_bw (‰)")
plt.xlabel("σ_bw (permille)")
plt.ylabel("Count")
plt.show()
plt.close(0)

plt.figure()
plt.hist(bootstrap_df["chi2_red"], bins=20)
plt.axvline(bootstrap_df["chi2_red"].mean())
plt.title("Bootstrap χ²_red distribution")
plt.xlabel("χ²_red")
plt.ylabel("Count")
plt.show()