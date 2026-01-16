import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pptx import Presentation
from pptx.util import Inches

# -----------------------------
# Load data + metadata
# -----------------------------
df = pd.read_csv(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\TW3586_p1.csv")

tw3586_rlim = pd.read_excel(
    r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_met.xlsx",
    sheet_name='RLIMSoutput'
)

tw3586_run = pd.read_excel(
    r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\3586_met.xlsx",
    sheet_name='runlist'
)

tw3586_metadata = tw3586_rlim.merge(tw3586_run, on='TP')

df = df.rename(columns={"position": "Position"})
df = tw3586_metadata.merge(df, on='Position')
df['lims'] = df['13Ccurr']/df['12Ccurr']

positions = np.unique(df['Position'])

# -----------------------------
# Loop through positions
# -----------------------------
for pos in positions:

    this_one = df.loc[df['Position'] == pos]

    # first-row metadata
    wtgraph = this_one['wtgraph'].iloc[0]
    desc    = this_one['Sample Name 2'].iloc[0]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    mode5 = (this_one['14Ccnts']*this_one['12Ccurr'])/(this_one['13Ccurr']**2)
    c13c12 = this_one['13Ccurr']/this_one['12Ccurr']

    # LEFT plot
    sc = axs[0].scatter(this_one['run'], mode5, c=this_one['12CLEcurr'], cmap='viridis')
    axs[0].set_xlabel('Runs Completed')
    axs[0].set_ylabel('Mode 5 Approx')
    axs[0].set_title(f'RTS Drift — Pos {pos}')
    fig.colorbar(sc, ax=axs[0], label='12CLEcurr')

    # RIGHT plot
    axs[1].scatter(this_one['run'], c13c12)
    axs[1].set_xlabel('Runs Completed')
    axs[1].set_ylabel('13C/12C')
    axs[1].set_title(f'13C/12C vs Beam — Pos {pos}')
    axs[1].set_ylim(np.min(df['lims']), np.max(df['lims']))
    fig.suptitle(
        f"wtgraph: {wtgraph}    |    sample description: {desc}",
        fontsize=14, fontweight='bold', y=1.03
    )

    plt.tight_layout()

    # -----------------------------
    # Save figure to PNG
    # -----------------------------
    out_png = fr"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3586\plots_combined\pos{pos}.png"
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()



"""
TW3587
"""

# -----------------------------
# Load data + metadata
# -----------------------------
df = pd.read_excel(r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\TW3587_p1_p2.xlsx")

tw3587_rlim = pd.read_excel(
    r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\tw3587_met.xlsx",
    sheet_name='RLIMSoutput'
)

tw3587_run = pd.read_excel(
    r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\tw3587_met.xlsx",
    sheet_name='runlist'
)

tw3587_metadata = tw3587_rlim.merge(tw3587_run, on='TP')

df = df.rename(columns={"position": "Position"})
df = tw3587_metadata.merge(df, on='Position')
df['lims'] = df['13Ccurr']/df['12Ccurr']

positions = np.unique(df['Position'])

# -----------------------------
# Loop through positions
# -----------------------------
for pos in positions:

    this_one = df.loc[df['Position'] == pos]

    # first-row metadata
    wtgraph = this_one['wtgraph'].iloc[0]
    desc    = this_one['Sample Name 2'].iloc[0]

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    mode5 = (this_one['14Ccnts']*this_one['12Ccurr'])/(this_one['13Ccurr']**2)
    c13c12 = this_one['13Ccurr']/this_one['12Ccurr']

    # LEFT plot
    sc = axs[0].scatter(this_one['run'], mode5, c=this_one['12CLEcurr'], cmap='viridis')
    axs[0].set_xlabel('Runs Completed')
    axs[0].set_ylabel('Mode 5 Approx')
    axs[0].set_title(f'RTS Drift — Pos {pos}')
    fig.colorbar(sc, ax=axs[0], label='12CLEcurr')

    # RIGHT plot
    axs[1].scatter(this_one['run'], c13c12)
    axs[1].set_xlabel('Runs Completed')
    axs[1].set_ylabel('13C/12C')
    axs[1].set_title(f'13C/12C vs Beam — Pos {pos}')
    axs[1].set_ylim(np.min(df['lims']), np.max(df['lims']))
    fig.suptitle(
        f"wtgraph: {wtgraph}    |    sample description: {desc}",
        fontsize=14, fontweight='bold', y=1.03
    )

    plt.tight_layout()

    # -----------------------------
    # Save figure to PNG
    # -----------------------------
    out_png = fr"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3587\plots_combined\pos{pos}.png"
    plt.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.close()
