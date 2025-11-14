"""
fILE BECAME OBSOLETE AFTER NOV 14 xcams MEETING

"""

# """
# This file branches off of Data_quality_paper_1 -> Data_quality_paper_2_2025 -> here.
# The previous file did the analysis and spit out statistics.
# Here, I want to make the final pretty graphs we'll include in the paper
# """
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
# # df = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_Paper_1_output/12_manual_plotly_drop.xlsx', sheet_name= 'Whole Dataframe')
# #
# # """
# # In the previous file, I got the summary statistics like the Chi2 to find the sigma_bw, so the FM and delta 14C were all calculated using the mean
# # Therefore, I couldn't plot "data" in the same way.
# # Here, I'll try to carefully convert RTS -> FM -> D14C and the I can use those to plot.
# # Below, I'll repeat a whole chunk of the previous script, and then perform these calculations and conversions.
# # Then I'll save the excel file so I can read it in and not have to rerun everything when tweaking the figures.
# # """
# #
# # print(f"Dataframe length at t0 for this script: {len(df)}")
# # df = df.loc[df['Keep_Remove'] == 'Keep']
# # df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/check1.xlsx') # wanted to check that TP 67815 was removed...
# # print(f"Dataframe length at t1, after selecting only !Keeps!: {len(df)}")
# #
# #
# # """
# # Please find the scanned derivation of these formulas in place TBD by CBL
# # """
# # #  Strongest check: try converting to numeric and see if anything fails
# # pd.to_numeric(df['RTS_corrected_error'], errors='raise')
# # pd.to_numeric(df['RTS_corrected'], errors='raise')
# # pd.to_numeric(df['DELTA 14C'], errors='raise')
# #
# # """
# # Below is some code copied from Data Quality 4.py but edited with more comments for clarity
# # """
# # """
# # I output all oxalics, alongside their preparation (sealed tube or flask). We were asked to only use data from
# # secondaries that use the flask OX, beacuse they're better. This code below adds the prep label onto the dataframe that
# # we're working with
# # """
# # # September 12, merge with STD prep type: We only want air secondaries run with Flask OX
# # spt = pd.read_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/flask_ox_label.xlsx')
# # spt = spt.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
# # df = df.merge(spt, on='TP')
# # df.to_excel('C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/ox_prep_labels_added.xlsx')
# # print(f"Dataframe length at t2, after adding prep types: {len(df)}")
# #
# # #
# # """
# # I need to parse between the different types of FIRI pretreatments from albert's TABLES.xlsx and see if I can find the same difference
# # after getting rid of flagged data.
# # FIRI-D is cellulose pretreated.
# # FIRI-E is AAA
# # FIRI-I is AAA
# # TIRL-L only has 2 measurements in RLIMS so lets forget about this.
# # I'm going to EDIT the R numbers for those names which may have EA and ST to look at these differences. This will be shown below. "EA Combustion::Run Numner"
# # After spending a bunch of July 4, 2024 on this: I just have to manually go through and check the pre-treatments for all FIRIs that were in Alberts sheet
# # """
# # firilist = ['24889/4','24889/5','24889/9','26281/1'] # here is the list of R numbers I want to check
# # firis = df.loc[(df['Job::R'].isin(firilist))]        # make a subset dataframe where these FIRIs are found
# # firis.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis.xlsx')  # write it to excel
# # firis = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/firis_edited.xlsx', comment='#') # I edited it by checking RLIMS. Read it back in
# # firis = firis[['TP','EA_ST','AAA_CELL']]  # drop columns to prep for merge
# # firis = firis.drop_duplicates(subset='TP', keep='first') # get rid of duplicates on the prep type output from RLIMS
# # df = df.merge(firis, on='TP', how='left')  # merge
# # df.to_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/mergecheck.xlsx') # output to recheck
# # print(f"Dataframe length at t3, after checking FIRI prep types and mergeing: {len(df)}")
# #
# # # edit the R numbers to fit that of "seconds.xlsx" and prep for the mathematics below:
# # df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/4_AAA_EA'
# # df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='AAA') & (df['EA_ST'].isna()), 'Job::R'] = '24889/4_AAA_ST'
# # df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'] =='EA'), 'Job::R'] = '24889/4_CELL_EA'
# # df.loc[(df['Job::R'] == '24889/4') & (df['AAA_CELL'] =='Cellulose') & (df['EA_ST'].isna()), 'Job::R'] = '24889/4_CELL_ST'
# #
# # #make distinction between pre and post flask ox according to JCT comments September 11, 2024
# # df.loc[(df['Job::R'] == '40430/2') & (df['preptype'] == 'FLASK') & (df['TW'] >= 3211) & (df['TW'] <= 3533), 'Job::R'] = '40430/2_flask'
# # df.loc[(df['Job::R'] == '40430/1') & (df['preptype'] == 'FLASK') & (df['TW'] >= 3211) & (df['TW'] <= 3533), 'Job::R'] = '40430/1_flask'
# # #
# #
# # """
# # add collection dates for secondaries where its listed:
# # """
# # # "C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_2_2025_output\seconds.xlsx"
# # df['Collection_Date'] = -999
# # df.loc[(df['Job::R'] == '40430/2_flask'),'Collection_Date'] = 2013
# # df.loc[(df['Job::R'] == '40430/1_flask'),'Collection_Date'] = 2013
# # df.loc[(df['Job::R'] == '14047/2'),'Collection_Date'] = 1950
# # df.loc[(df['Job::R'] == '14047/12'),'Collection_Date'] = 1950
# #
# # df.loc[(df['Job::R'] == '24889/4_AAA_EA'),'Collection_Date'] = 1950
# # df.loc[(df['Job::R'] == '24889/4_AAA_ST'),'Collection_Date'] = 1950
# # df.loc[(df['Job::R'] == '24889/4_CELL_EA'),'Collection_Date'] = 1950
# # df.loc[(df['Job::R'] == '24889/4_CELL_ST'),'Collection_Date'] = 1950
# # df.loc[(df['Job::R'] == '24889/14'),'Collection_Date'] = 1950
# #
# # df.loc[(df['Job::R'] == '24889/14'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '24889/4_AAA_EA'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '24889/4_AAA_ST'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '24889/4_CELL_EA'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '24889/4_CELL_ST'),'Collection_Date'] = 1991
# #
# # df.loc[(df['Job::R'] == '41347/12'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '41347/13'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '41347/2'),'Collection_Date'] = 1991
# # df.loc[(df['Job::R'] == '41347/3'),'Collection_Date'] = 1991
# #
# # # # data with the secondaries to filter on: THIS LINE IMPORTS THE CONCENSUS VALUES
# # df2 = pd.read_excel('H:/Science/Papers/In Prep Work/2023_Zondervan_DataQuality/seconds.xlsx', comment='#')
# # rs = np.unique(df2['R_number'])
# #
# # df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting.xlsx")
# #
# # """
# # EVERYTHING ABOVE WAS A COPY OF PREVIOUS SCRIPT
# # THE OUTPUT FILE ALREADY HAS FM AND FM ERROR, WE ONLY NEED TO CONVERT TO DELTA14C AGAIN WHERE THE DATE WAS MISSING
# # """
# df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting.xlsx")
# df2 = pd.read_excel(f'C:/Users/clewis/IdeaProjects/GNS/xcams/Data_Quality_paper_2_2025_output/statistics.xlsx')
#
# # calculate D14C for all samples
# cols = ['Collection_Date', 'F_corrected_normed', 'F_corrected_normed_error']
# df[cols] = df[cols].apply(pd.to_numeric, errors='coerce').astype(float)
# df['delta_14C_new'] =  1000*(df['F_corrected_normed']*np.exp((1950-df['Collection_Date'])/8267)-1)
# df['delta_14C_err_new'] = 1000*(df['F_corrected_normed_error']*np.exp((1950-df['Collection_Date'])/8267))
#
# # merge dataframe with summary statistics so i can calculate residual
# df2 = df2.rename(columns={"R_number": "Job::R"})
# df2_merge = df2[["Job::R",'RTS (wmean)','RTS_err (mean)']]
# df = df.merge(df2_merge, on="Job::R", how='left')
#
# df['residual'] = ( df['RTS_corrected'] - df['RTS (wmean)'] ) / df['RTS_corrected_error']
# df = df.loc[df['residual'].notna()]
#
# df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting2.xlsx")
#
# """
# Dont change above
# """
#
# df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting2.xlsx")
#
#
#
#
# # SPLIT AXES DOCUMENTATION
# # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
#
# air1 = df.loc[df['Job::R'] == '40430/1_flask']
# air2 = df.loc[df['Job::R'] == '40430/2_flask']
#
#
# # Create figure and 3 vertical subplots
# fig, axs = plt.subplots(3, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column
#
# # First subplot
# axs[0].scatter(air1['TP'], air1['residual'], color='black', linestyle='', label = 'BHDamb')
# axs[0].scatter(air2['TP'], air2['residual'], color='gray', linestyle='', label = 'BHDspike')
# axs[0].axhline(y=0, color='black')
# axs[0].legend()
#
# # Second subplot
# axs[1].errorbar(air1['TP'], air1['delta_14C_new'], yerr=air1['delta_14C_err_new'], color='black', linestyle='', label = 'BHDamb', marker='o')
# axs[2].errorbar(air2['TP'], air2['delta_14C_new'],  yerr=air2['delta_14C_err_new'], color='gray', linestyle='', label = 'BHDspike', marker='o')
#
# axs[1].set_ylim(25, 37)
# axs[2].set_ylim(-77, -66)
#
# # hide the spines between ax and ax2
# axs[1].spines.bottom.set_visible(False)
# axs[2].spines.top.set_visible(False)
# axs[1].xaxis.tick_top()
# axs[1].tick_params(labeltop=False)  # don't put tick labels at the top
# axs[2].xaxis.tick_bottom()
#
# # Now, let's turn towards the cut-out slanted lines.
# # We create line objects in axes coordinates, in which (0,0), (0,1),
# # (1,0), and (1,1) are the four corners of the Axes.
# # The slanted lines themselves are markers at those locations, such that the
# # lines keep their angle and position, independent of the Axes size or scale
# # Finally, we need to disable clipping.
#
# d = .5  # proportion of vertical to horizontal extent of the slanted line
# kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
#               linestyle="none", color='k', mec='k', mew=1, clip_on=False)
# axs[1].plot([0, 1], [0, 0], transform=axs[1].transAxes, **kwargs)
# axs[2].plot([0, 1], [1, 1], transform=axs[2].transAxes, **kwargs)
#
# axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
# axs[1].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[2].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# # Adjust layout so titles and labels don't overlap
# plt.tight_layout()
#
# plt.savefig(
#     r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output/Fig1_airs.png',
#     dpi=300, bbox_inches="tight")
# plt.close()
#
#
# """
# REPEAT THE ABOVE FOR THE ORGANICS PLOT!
# """
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# # SPLIT AXES DOCUMENTATION
# # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
#
# carb1 = df.loc[df['Job::R'] == '14047/12'] # IAEA-C2: Freshwater Travertine waterline
# carb2 = df.loc[df['Job::R'] == '14047/2'] # IAEA-C2: Freshwater Travertine carbonate
#
# carb3 = df.loc[df['Job::R'] == '41347/12'] # LAC1 coral water
# carb4 = df.loc[df['Job::R'] == '41347/2'] # LAC1 coral carbonate
#
# carb5 = df.loc[df['Job::R'] == '41347/13'] # LAA1 coral water
# carb6 = df.loc[df['Job::R'] == '41347/3'] # LAC1 coral carbonate
#
# # Create figure and 3 vertical subplots
# fig, axs = plt.subplots(4, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column
#
# # First subplot
# axs[0].scatter(carb1['TP'], carb1['residual'], color='black', linestyle='', label = 'IAEA-C2: Water line')
# axs[0].scatter(carb2['TP'], carb2['residual'], color='gray', linestyle='', label = 'IAEA-C2: Carbonate Line')
#
# axs[0].scatter(carb3['TP'], carb3['residual'], color='red', linestyle='', label = 'LAC1 coral water')
# axs[0].scatter(carb4['TP'], carb4['residual'], color='green', linestyle='', label = 'LAC1 coral carbonate')
#
# axs[0].scatter(carb5['TP'], carb5['residual'], color='yellow', linestyle='', label = 'LAA1 coral water')
# axs[0].scatter(carb6['TP'], carb6['residual'], color='orange', linestyle='', label = 'LAC1 coral carbonate')
#
# axs[0].axhline(y=0, color='black')
#
#
# # Second subplot
# axs[3].errorbar(carb1['TP'], carb1['delta_14C_new'], yerr=carb1['delta_14C_err_new'], color='black', linestyle='', label = 'IAEA-C2: Waterline', marker='o')
# axs[3].errorbar(carb2['TP'], carb2['delta_14C_new'],  yerr=carb2['delta_14C_err_new'], color='gray', linestyle='', label = 'IAEA-C2: Carbonate Line', marker='o')
#
# # Second subplot
# axs[1].errorbar(carb3['TP'], carb3['delta_14C_new'], yerr=carb3['delta_14C_err_new'], color='red', linestyle='', label = 'LAC1 coral water', marker='o')
# axs[1].errorbar(carb4['TP'], carb4['delta_14C_new'],  yerr=carb4['delta_14C_err_new'], color='green', linestyle='', label = 'LAC1 coral carbonate', marker='o')
#
# # Second subplot
# axs[2].errorbar(carb5['TP'], carb5['delta_14C_new'], yerr=carb5['delta_14C_err_new'], color='yellow', linestyle='', label = 'LAA1 coral water', marker='o')
# axs[2].errorbar(carb6['TP'], carb6['delta_14C_new'],  yerr=carb6['delta_14C_err_new'], color='orange', linestyle='', label = 'LAC1 coral carbonate', marker='o')
#
#
# axs[1].spines.bottom.set_visible(False)  # removes spine on bottom of 1
# axs[2].spines.bottom.set_visible(False)  # removes spine on bottom of 2
# axs[2].spines.top.set_visible(False)  # removes spine on top of 2
# axs[3].spines.top.set_visible(False)  # removes spine on top of 3
# axs[1].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
# axs[2].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
# axs[3].tick_params(axis='x', which='both', top=False, labeltop=False)
# axs[1].legend()
# axs[2].legend()
# axs[3].legend()
#
#
# # axs[1].tick_params(labeltop=False)  # don't put tick labels at the top
# # # axs[2].tick_params(labelbottom=False)  # don't put tick labels at the top
#
# d = .5  # proportion of vertical to horizontal extent of the slanted line
# kwargs = dict(marker=[(-1, -d), (1, d)], markersize=12,
#               linestyle="none", color='k', mec='k', mew=1, clip_on=False)
# axs[1].plot([0, 1], [0, 0], transform=axs[1].transAxes, **kwargs)
# axs[2].plot([0, 1], [1, 1], transform=axs[2].transAxes, **kwargs)
# axs[2].plot([0, 1], [0, 0], transform=axs[2].transAxes, **kwargs)
# axs[3].plot([0, 1], [1, 1], transform=axs[3].transAxes, **kwargs)
#
#
# axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
# axs[1].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[2].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# axs[3].set_ylabel('\u0394$^1$$^4$C (\u2030)')
# # Adjust layout so titles and labels don't overlap
# plt.tight_layout()
#
# plt.savefig(
#     r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output/Fig1_inorganic.png',
#     dpi=300, bbox_inches="tight")
# plt.close()
#
# """
# ORGANICS
# """
#
# # SPLIT AXES DOCUMENTATION
# # https://matplotlib.org/stable/gallery/subplots_axes_and_figures/broken_axis.html
#
# o1 = df.loc[df['Job::R'] == '24889/14']
# o2 = df.loc[df['Job::R'] == '24889/4_AAA_EA']
# o3 = df.loc[df['Job::R'] == '24889/4_AAA_ST']
# o4 = df.loc[df['Job::R'] == '24889/4_CELL_EA']
# o5 = df.loc[df['Job::R'] == '24889/4_CELL_ST']
#
# # Create figure and 3 vertical subplots
# fig, axs = plt.subplots(2, 1, figsize=(6, 8), sharex=True)  # 3 rows, 1 column
#
# # First subplot
# axs[0].scatter(o1['TP'], o1['residual'], color='black', linestyle='', label = 'RPO')
# axs[0].scatter(o2['TP'], o2['residual'], color='gray', linestyle='', label = 'AAA EA')
# axs[0].scatter(o3['TP'], o3['residual'], color='blue', linestyle='', label = 'AAA ST')
# axs[0].scatter(o4['TP'], o4['residual'], color='red', linestyle='', label = 'CELL EA')
# axs[0].scatter(o5['TP'], o5['residual'], color='yellow', linestyle='', label = 'CELL ST')
# axs[0].axhline(y=0, color='black')
# axs[0].legend()
#
# # Second subplot
# axs[1].errorbar(o1['TP'], o1['delta_14C_new'], yerr=o1['delta_14C_err_new'], color='black', linestyle='', label = 'BHDamb', marker='o')
# axs[1].errorbar(o2['TP'], o2['delta_14C_new'],  yerr=o2['delta_14C_err_new'], color='gray', linestyle='', label = 'BHDspike', marker='o')
# axs[1].errorbar(o3['TP'], o3['delta_14C_new'], yerr=o3['delta_14C_err_new'], color='blue', linestyle='', label = 'BHDamb', marker='o')
# axs[1].errorbar(o4['TP'], o4['delta_14C_new'],  yerr=o4['delta_14C_err_new'], color='yellow', linestyle='', label = 'BHDspike', marker='o')
# axs[1].errorbar(o5['TP'], o5['delta_14C_new'], yerr=o5['delta_14C_err_new'], color='red', linestyle='', label = 'BHDamb', marker='o')
#
# #
# # axs[1].set_ylim(25, 37)
# # axs[2].set_ylim(-77, -66)
#
#
# axs[0].set_ylabel('residual: (x$_i$ - mean) / \u03C3')
# axs[1].set_ylabel('\u0394$^1$$^4$C (\u2030)')
#
# # Adjust layout so titles and labels don't overlap
# plt.tight_layout()
# plt.show()
# plt.savefig(
#     r'C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output/Fig1_organics.png',
#     dpi=300, bbox_inches="tight")
# plt.close()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# # """
# # Calculate the weighted mean (again) to calculate the residuals to make a residual plot
# # """
# # wmean_num = np.sum(df['delta_14C_new']/df['delta_14C_err_new']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
# # wmean_dem = np.sum(1/df['delta_14C_err_new']**2)
# # df['wmean'] = wmean_num / wmean_dem
# # """
# # Calculate residual
# # """
# # df['residual'] = ( df['delta_14C_new'] - df['wmean'] ) / df['delta_14C_err_new']
# #
# # df.to_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting.xlsx")
#
#
#
#
#
#
#
# #
# #
# #
# #
# #
# #
# #
# # """
# # Now I'll make the figures
# # Now we have FM, Detla 14C ready to go
# # """
# #
# # df = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_3_2025_output\subset_for_plotting.xlsx")
# #
# # """
# # Calculate the weighted mean (again) to calculate the residuals to make a residual plot
# # """
# # wmean_num = np.sum(df['delta_14C_new']/df['delta_14C_err_new']**2)  #  "I:\C14Data\Data Quality Paper\AZ_V0\Fig 1.xlsx"
# # wmean_dem = np.sum(1/df['delta_14C_err_new']**2)
# # df['wmean'] = wmean_num / wmean_dem
# # """
# # Calculate residual
# # """
# # df['residual'] = ( df['delta_14C_new'] - df['wmean'] ) / df['delta_14C_err_new']
# #
# #
# #
# # # # I only want to have a look at the secondary standards with R number we care about, from this sheet.
# # df2 = pd.read_excel(r"C:\Users\clewis\IdeaProjects\GNS\xcams\Data_Quality_paper_2_2025_output\seconds.xlsx", comment='#')
# # df2 = df2.sort_values(by='Expected FM')
# # rs = pd.unique(df2['R_number'])
# # plt.close()
# # for i in range(0, len(rs)):
# #     subset1 = df.loc[df['Job::R'] == rs[i]]
# #     plt.scatter(subset1['TP'], subset1['residual'])
# #     plt.show()
# #
#
#
#
#
#
#
#
#
