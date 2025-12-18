import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"/Fiordland_DIC_14C_paper/data/raw/12482_screenobs.csv")

# Convert timestamp to datetime
df["OBS_DATE"] = pd.to_datetime(df["OBS_DATE"])

# Filter for April & May of 2024 and 2025
df_filtered = df[
    (
            (df["OBS_DATE"].dt.year.isin([2024, 2025])) &
            (df["OBS_DATE"].dt.month.isin([4, 5]))
    )
]

# Plot relative humidity
plt.figure(figsize=(12, 5))
plt.plot(df_filtered["OBS_DATE"], df_filtered["MEAN_RELHUM10"])
plt.xlabel("Time")
plt.ylabel("Relative Humidity (%)")
plt.title("Relative Humidity — April & May (2024–2025)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()