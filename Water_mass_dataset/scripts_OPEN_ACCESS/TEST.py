from scipy.io import loadmat
import pandas as pd
import numpy as np

# df = pd.read_csv('H:\Science\Datasets\GLODAPv2.2023_Merged_Master_File.csv', dtype=str)
#
# # store the length of the original dataset for comparison later
# x1 = len(df)
#
# # Here are the original column names
# # df = [['G2expocode', 'G2cruise', 'G2station', 'G2region', 'G2cast', 'G2year', 'G2month', 'G2day', 'G2hour', 'G2minute',
# #        'G2latitude', 'G2longitude', 'G2bottomdepth', 'G2maxsampdepth', 'G2bottle', 'G2pressure', 'G2depth', 'G2temperature',
# #        'G2theta', 'G2salinity', 'G2salinityf', 'G2salinityqc', 'G2sigma0', 'G2sigma1', 'G2sigma2', 'G2sigma3', 'G2sigma4', 'G2gamma',
# #        'G2oxygen', 'G2oxygenf', 'G2oxygenqc', 'G2aou', 'G2aouf', 'G2nitrate', 'G2nitratef', 'G2nitrateqc', 'G2nitrite', 'G2nitritef',
# #        'G2silicate', 'G2silicatef', 'G2silicateqc', 'G2phosphate', 'G2phosphatef', 'G2phosphateqc', 'G2tco2', 'G2tco2f', 'G2tco2qc',
# #        'G2talk', 'G2talkf', 'G2talkqc', 'G2fco2', 'G2fco2f', 'G2fco2temp', 'G2phts25p0', 'G2phts25p0f', 'G2phtsinsitutp', 'G2phtsinsitutpf',
# #        'G2phtsqc', 'G2cfc11', 'G2pcfc11', 'G2cfc11f', 'G2cfc11qc', 'G2cfc12', 'G2pcfc12', 'G2cfc12f', 'G2cfc12qc', 'G2cfc113', 'G2pcfc113',
# #        'G2cfc113f', 'G2cfc113qc', 'G2ccl4', 'G2pccl4', 'G2ccl4f', 'G2ccl4qc', 'G2sf6', 'G2psf6', 'G2sf6f', 'G2sf6qc', 'G2c13', 'G2c13f',
# #        'G2c13qc', 'G2c14', 'G2c14f', 'G2c14err', 'G2h3', 'G2h3f', 'G2h3err', 'G2he3', 'G2he3f', 'G2he3err', 'G2he', 'G2hef', 'G2heerr', 'G2neon',
# #        'G2neonf', 'G2neonerr', 'G2o18', 'G2o18f', 'G2toc', 'G2tocf', 'G2doc', 'G2docf', 'G2don', 'G2donf', 'G2tdn',
# #        'G2tdnf', 'G2chla', 'G2chlaf', 'G2doi']]
#
# # I only want to keep SOME of the columns
# df = df[['G2expocode', 'G2cruise', 'G2station', 'G2region', 'G2cast', 'G2year', 'G2month', 'G2day', 'G2hour', 'G2minute', 'G2latitude', 'G2longitude','G2pressure','G2temperature','G2salinity', 'G2salinityf', 'G2salinityqc','G2c14', 'G2c14f', 'G2c14err','G2sigma0','G2oxygen']]
#
# # and I only want to see rows where 14C is greater than the NAN setting.
# df = df.loc[df['G2depth'].astype(float) < 100]
#
# df.to_csv('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP1_reboot/having_look_at_DO.csv')

df = pd.read_csv('C:/Users/clewis/IdeaProjects/GNS/Water_mass_dataset/output_OPEN_ACCESS/STEP1_reboot/having_look_at_DO.csv')