"""
THIS FILE CREATES EXCLE SHEET THAT READS INTO CONTEXT_ANALYSIS.PY
"""

from pathlib import Path
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

def context_analysis(hp):
    
    # THIS IS A FOLDER WITH ALL CONTEXT FILES FROM 3600 to 3629, STRAIGHT FROM ACCELNET
    folder = Path(r"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\context_3600_to_")

    # make a dataframe to store imported data
    all_dfs = []

    # THIS LOOP WILL TAKE CONTEXT FILES AND APPEND THEM TO EXCEL SHEET
    for file in folder.iterdir():
        # split text based on delimitation
        lines = file.read_text().splitlines()

        # this find the word SERIAL as the beginning of the data we want, and also find the end at #1
        start = next(i for i, l in enumerate(lines) if "serial" in l)
        end = next(i for i, l in enumerate(lines[start+1:], start+1) if l.startswith("#1"))

        cols = lines[start].split()[1:]
        rows = [l.split() for l in lines[start+2:end] if l.startswith("result")]

        df = pd.DataFrame(rows, columns=["record"] + cols)
        df["file"] = file.stem

        df["TW_full"] = file.stem

        stem, excess = file.stem.split("_")

        df["TW"] = int(stem)
        df["excess"] = int(excess)

        all_dfs.append(df)

    master_df = pd.concat(all_dfs, ignore_index=True)

    master_df = master_df.rename(columns={"cup1":"12CLE",
                            "cup7":"12CHE",
                            "cup8":"13CHE",
                            "cnt2":"CnttotGT",
                            "cnt3":"CnttotBG",
                            "ratio1":"12_HE_LE",
                            "ratio2":"13_12_LE",
                            "ratio3":"13_12_HE",
                            "ratio4":"14_12_HE",
                            "ratio5":"14_13_HE",
                            "param1":"Cs_temp",
                            "param2":"P_src",
                            "param3":"I_cat",
                            "param4":"I_ext",
                            "param5":"Crlost",
                            "param6":"P_strp",
                            "param7":"GVM",
                            "param8":"BM03",
                            })

    # now I just want to save these columns 
    master_df = master_df[["serial",
                        "DMANitem",
        "TW_full",
        "TW",
        "excess",
        "12CLE",
        "12CHE",
        "13CHE",
        "CnttotGT",
        "CnttotBG",
        "12_HE_LE",
        "13_12_LE",
        "13_12_HE",
        "14_12_HE",
        "14_13_HE",
        "Cs_temp",
        "P_src",
        "I_cat",
        "I_ext",
        "Crlost",
        "P_strp",
        "GVM",
        "BM03",
    ]]

    # Now we need to tell if which wheels have which standards: 
    master_df['Pres'] = 'RP' # default to regular precision

    master_df.loc[master_df['TW'].isin(hp), 'Pres'] = 'HP'
    master_df.loc[master_df['TW'] == 3626, 'Pres'] = 'WACK'

    master_df.to_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\context_analysis2.xlsx")
    df = pd.read_excel(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\context_analysis2.xlsx")

    stands_HP = [0,5,10,15,20,25,30,35]
    stands_RP = [0,7,14,21,28,35]
    wack = [0,2,3,5,6,8,9,11,12]

    tws = np.unique(df['TW_full'])

    retunes = ['3600_1', '3613_1','3615_1', '3617_1','3622_1','3623_1', '3623_2', '3624_1','3627_1','3629_1','3629_2']

    for i in range(0, len(tws)):

        fig, axs = plt.subplots(4, 1, figsize=(8, 8))

        # grab first wheel
        subdf_i = df.loc[df['TW_full'] == tws[i]]

        # whats precision: 
        precision = subdf_i['Pres'].iloc[0]

        if precision == 'HP': 
            subdf_i = subdf_i.loc[subdf_i['DMANitem'].isin(stands_HP)]
        elif precision == 'WACK': 
            subdf_i = subdf_i.loc[subdf_i['DMANitem'].isin(wack)]
        else:
            subdf_i = subdf_i.loc[subdf_i['DMANitem'].isin(stands_RP)]

        # grab individual cathodes: 
        targets = np.unique(subdf_i['DMANitem'])

        for j in range(0, len(targets)):
            t_j = subdf_i.loc[subdf_i['DMANitem']==targets[j]]
            t_j = t_j.dropna(subset='12CLE')
            t_j = t_j.sort_values(by='12CLE')

            # grab first 
            t_j["12CLE"] = t_j["12CLE"]*1e6 
            t_j["14_12_HE"] = t_j["14_12_HE"]*1e12
            t_j["14_13_HE"] = t_j["14_13_HE"]*1e10
            

            axs[0].plot(t_j["12CLE"],t_j["13_12_HE"], label=f'{targets[j]}', linestyle='-', marker='o')
            axs[1].plot(t_j["12CLE"],t_j["14_12_HE"], linestyle='-', marker='o')
            axs[2].plot(t_j["12CLE"],t_j["14_13_HE"], linestyle='-', marker='o')
            axs[3].plot(t_j["serial"],t_j["12CLE"], linestyle='', marker='o')
            axs[0].legend
        
        if tws[i] in retunes:
            axs[0].set_title(f'{tws[i]}_RETUNED', color='red')
        else:
            axs[0].set_title(f'{tws[i]}')

        axs[0].set_ylim(0.01085,0.01125)
        axs[1].set_ylim(1.18,1.235)
        axs[2].set_ylim(1.05,1.13)
        axs[3].set_ylim(0,110)

        axs[0].set_xlim(0,110)
        axs[1].set_xlim(0,110)
        axs[2].set_xlim(0,110)

        axs[0].axvline(x=100, color='red')
        axs[1].axvline(x=100, color='red')
        axs[2].axvline(x=100, color='red')

        axs[0].set_ylabel('13/12HE')
        axs[1].set_ylabel('14/12HE')
        axs[2].set_ylabel('14/13HE')
        axs[2].set_xlabel('LEC12- (uA)')
        axs[3].set_xlabel('Run #')

        axs[0].legend()

        plt.savefig(rf"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\output\context_plots\{tws[i]}.png",
                dpi=300, bbox_inches="tight")

   









