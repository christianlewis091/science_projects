"""
November 20, 2025
Mergeing DIC 14C data with sampling data from bobn
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ams_data = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\TW3584_SFCS2505_May.xlsx")
ship_data = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\raw\sfcs2505_gpkg_waterSamples_202508111535_EDITED.xlsx", comment='#')

df = ams_data.merge(ship_data, on='Samples::Sample ID')
df.to_excel('C:/Users\clewis\IdeaProjects\GNS\Fiordland_DIC_14C_paper\data\processed/SFCS2505_DIC_14C_FINAL.xlsx')

