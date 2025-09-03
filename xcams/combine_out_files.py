import pandas as pd
import shutil
import os
import csv

"""
# example of directory1 = r"I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3562"
# example of file1: TW3652_p1
# example of file1: TW3652_p2
"""

def combined_out_files(directory1, file1, file2):

    # create a new out file for the combined csv data to be added into.
    filepath1 = os.path.join(directory1, f"{file2}.out")
    filepath2 = os.path.join(directory1, "COMBINED_paste_here.out")
    shutil.copy(filepath1, filepath2)

    # read in the outfiles
    df1 = pd.read_csv(f"{directory1}/{file1}.out", delim_whitespace=True, skiprows=2)
    df2 = pd.read_csv(f"{directory1}/{file2}.out", delim_whitespace=True, skiprows=2)

    df3 = pd.concat([df1, df2]).reset_index(drop=True)
    # set the index equal to the run number. This gets around the reset of second run at 0 and import into RLIMS
    df3["run"] = df3.index

    # Define your metadata/preamble row
    preamble = [
        ['start date', 'wheel', '(isotope)', '', '', '', '', '', '', 'version', 'test_pulses_gen_per_cycle', '', '', '', '', '', '', ''],
        ['6/05/2025', 'TW3562', '14C', '0', '0', '0', 'N', 'N', 'N', '2.04', '2', '0', '0', '0', '0', '0', '0', '0'],
        [],]

    # Define output path
    output_file = f"{directory1}\COMBINED.csv"

    # Write preamble and DataFrame to the file
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(preamble)
        df3.to_csv(f, index=False)

combined_out_files(r"I:\XCAMS/3_measurements\C-14 AMS\TW data analysis\TW3550-3599\TW3562", 'TW3562_p1', 'TW3562_p2')

