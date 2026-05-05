import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# df = pd.read_excel("C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/13_AOU_plot/JOINED_DATA_wAOU.xlsx")

# wrapping the mass balance in a function means we can run it with multiple end members
def run_model(dic, dic_conc, dic_err, m_end, m_end_err, t_end_err, ts, label):
    results = []

    for t_end in ts:
        X_m_num = dic - t_end
        X_m_num_errprop = np.sqrt(dic_err**2 + t_end_err**2)

        X_m_denom = m_end - t_end
        X_m_denom_errprop = np.sqrt(m_end_err**2 + t_end_err**2)

        X_m = X_m_num / X_m_denom
        X_m_err = np.sqrt((X_m_num_errprop / X_m_num)**2 + (X_m_denom_errprop / X_m_denom)**2)

        X_t = 1 - X_m
        DICt = X_t * dic_conc

        O_min = (DICt * 0.27) * 1000
        O_mid = (DICt * 0.395) * 1000 # middle of the quotes values from Anderson 1995
        O_max = (DICt * 0.52) * 1000

        results.append({
            "t_end": t_end,
            'X_m':X_m,
            "X_t":X_t,
            "O_min_uM": O_min,
            "O_mid_uM": O_mid,
            "O_max_uM": O_max,
            "label": label
        })

    return pd.DataFrame(results)

# shared t range
ts = np.linspace(20, -50, 20)  # 13 points → step of 5

# run two scenarios
# created in order of decreasing AOU (that's why they're scrambled)
df1 = run_model(dic=20.57, dic_conc=2.43, dic_err=1.84, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Sportsman's Cove, May 2025, 31.9m (TP90816)")
df3 = run_model(dic=(23.03 + 23.67)/2, dic_conc=2.21, dic_err=0.45, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Sportsman's Cove, May 2024, 39m (TP88893") # stats come from duplicates from this Stn!

fig, axs = plt.subplots(1, 3, figsize=(9,5.5))

# DEEP COVE
df2 = run_model(dic=27.03, dic_conc=2.29, dic_err=1.86, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Deep Cove, May 2025, 91m (TP90809)")
df4 = run_model(dic=27.01, dic_conc=2.23, dic_err=1.87, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Deep Cove May 2024, 80m  (TP88864")
axs[0].set_title('Deep Cove')
axs[0].plot(df2["t_end"], df2["O_min_uM"], color='black', alpha=0)
axs[0].plot(df2["t_end"], df2["O_max_uM"], color='black', alpha=0)
axs[0].plot(df2["t_end"], df2["O_mid_uM"], color='black', alpha=.5, label='May 2025, 91m')
axs[0].fill_between(df2["t_end"],df2["O_min_uM"], df2["O_max_uM"], color='black', alpha=0.1)

axs[0].plot(df4["t_end"], df4["O_min_uM"], color='blue', alpha=0)
axs[0].plot(df4["t_end"], df4["O_max_uM"], color='blue', alpha=0)
axs[0].plot(df4["t_end"], df4["O_mid_uM"], color='blue', alpha=.5, label='May 2024, 91m')
axs[0].fill_between(df4["t_end"],df4["O_min_uM"], df4["O_max_uM"], color='blue', alpha=0.1)

# GIRLIES BASIN
df5 = run_model(dic=23.34, dic_conc=2.19, dic_err=1.86, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Girlie's Basin, May 2025, 166m (TP90813")
df6 = run_model(dic=27.93, dic_conc=2.12, dic_err=1.9, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Girlie's Basin, May 2024, 140m (TP88923")
axs[1].set_title('Girlies Basin')
axs[1].plot(df5["t_end"], df5["O_min_uM"], color='black', alpha=0)
axs[1].plot(df5["t_end"], df5["O_max_uM"], color='black', alpha=0)
axs[1].plot(df5["t_end"], df5["O_mid_uM"], color='black', alpha=0.5, label='May 2025, 166m')
axs[1].fill_between(df5["t_end"],df5["O_min_uM"], df5["O_max_uM"], color='black', alpha=0.1)

axs[1].plot(df6["t_end"], df6["O_min_uM"], color='blue', alpha=0)
axs[1].plot(df6["t_end"], df6["O_max_uM"], color='blue', alpha=0)
axs[1].plot(df6["t_end"], df6["O_mid_uM"], color='blue', alpha=0.5, label='May 2024, 140m')
axs[1].fill_between(df6["t_end"],df6["O_min_uM"], df6["O_max_uM"], color='blue', alpha=0.1)


# Sportsman's Cove
df1 = run_model(dic=20.57, dic_conc=2.43, dic_err=1.84, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Sportsman's Cove, May 2025, 31.9m (TP90816)")
df3 = run_model(dic=(23.03 + 23.67)/2, dic_conc=2.21, dic_err=0.45, m_end=30, m_end_err=0.3, t_end_err=0, ts=ts, label="Sportsman's Cove, May 2024, 39m (TP88893") # stats come from duplicates from this Stn!
axs[2].set_title('Sportsmans Cove')
axs[2].plot(df1["t_end"], df1["O_min_uM"], color='black', alpha=0)
axs[2].plot(df1["t_end"], df1["O_max_uM"], color='black', alpha=0)
axs[2].plot(df1["t_end"], df1["O_mid_uM"], color='black', alpha=0.5, label='May 2025, 31.9m')
axs[2].fill_between(df1["t_end"],df1["O_min_uM"], df1["O_max_uM"], color='black', alpha=0.1)

axs[2].plot(df3["t_end"], df3["O_min_uM"], color='blue', alpha=0)
axs[2].plot(df3["t_end"], df3["O_max_uM"], color='blue', alpha=0)
axs[2].plot(df3["t_end"], df3["O_mid_uM"], color='blue', alpha=0.5, label='May 2024, 39m')
axs[2].fill_between(df3["t_end"],df3["O_min_uM"], df3["O_max_uM"], color='blue', alpha=0.1)
#
axs[0].set_ylim(0,300)
axs[1].set_ylim(0,300)
axs[2].set_ylim(0,300)
axs[0].axhline(250, color='red', alpha=0.1)
axs[1].axhline(250, color='red', alpha=0.1)
axs[2].axhline(250, color='red', alpha=0.1)

axs[0].legend()
axs[1].legend()
axs[2].legend()

axs[0].set_ylabel('Oxygen consumed by DIC production: Modelled (uM/kg)')
axs[1].set_xlabel('Set Terrestrial End-Member \u0394$^1$$^4$$C$ (\u2030)')

plt.savefig(f"C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/14_mass_balance/fig1.png", dpi=300, bbox_inches="tight")
plt.close()

df_all = pd.concat([df1, df2, df3, df4, df5, df6])
df_all.to_excel("C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\output_V2/14_mass_balance/out.xlsx")

# # combine
# df_all = pd.concat([df1, df2, df3, df4])

# # plot
# for label, df_sub in df_all.groupby("label"):
#     plt.plot(df_sub["t_end"], df_sub["O_min_uM"], label=f"{label} O_min")
#     plt.plot(df_sub["t_end"], df_sub["O_max_uM"], linestyle="--", label=f"{label} O_max")
#
# plt.xlabel("t_end")
# plt.ylabel("Oxygen (µM)")
# plt.legend()
# plt.show()
#

# """
# I want to construct a mass-balance that makes sense, and make a plot that allow us to vizualize it.
# """
#
# dic = (23.03 + 23.67)/2 # duplicates from Sportsman's Cove, SFCS2405
# dic_conc = 2.2 #mmol/kg
# dic_err = 0.45 # stdev calculated in excel from the two duplicates
# m_end = 30 # marine end member
# m_end_err = .3 # set to 10% error, approximating here!
# # t_end = 0 # terrestrial end member
# t_end_err = 0
#
# ts = np.linspace(10, -30, 100)  # 13 points → step of 5
#
# results = []
# for i in range(0, len(ts)):
#     t_end = ts[i]
#     # I'm brekaing it up into numerator and denominator so its easier for error prop
#     X_m_num = dic-t_end
#     X_m_num_errprop = np.sqrt(dic_err**2 + t_end_err**2)
#
#     X_m_denom = m_end-t_end
#     X_m_denom_errprop = np.sqrt(m_end_err**2 + t_end_err**2)
#
#     X_m = X_m_num/X_m_denom
#     X_m_err = np.sqrt((X_m_num_errprop/X_m_num)**2 + (X_m_denom_errprop/X_m_denom)**2)
#
#     X_t = 1-X_m
#
#     # calculate DIC from remin!
#     DICt = X_t*dic_conc
#
#     # calculate min/max O requirement from Anderson 1995: 0.27, 0.52, then convert to uM
#     O_min = (DICt*0.27)*1000
#     O_max = (DICt*0.52)*1000
#
#     results.append({
#         "t_end": t_end,
#         "X_m": X_m,
#         "X_m_err": X_m_err,
#         "X_t": X_t,
#         "DICt": DICt,
#         "O_min_uM": O_min,
#         "O_max_uM": O_max
#     })
#
# df = pd.DataFrame(results)
#
# plt.plot(df['t_end'], df['O_min_uM'])
# plt.plot(df['t_end'], df['O_max_uM'])
# plt.show()
