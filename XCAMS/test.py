import os

import pandas as pd


"""
Have a look through all the directories and find where there are _2's. When did we restart the measurement"
"""

def find_directories_with_file(directory):
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith("_2.csv"):
                # print(file)
                result.append(str(file))
                break  # Break the loop if at least one matching file is found in the directory
    return result

# Example usage
directory4 = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3450-3499"
directory3 = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3350-3399"
directory2 = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3300-3349"
directory1 = r"I:\XCAMS\3_measurements\C-14 AMS\TW data analysis\TW3250-3299"

list1 = [directory1, directory2, directory3, directory4]

database = pd.DataFrame()
for i in range(0, len(list1)):
    directories_with_file = find_directories_with_file(list1[i])
    data = pd.DataFrame({"List": directories_with_file})
    database = pd.concat([database, data]).reset_index(drop=True)

database.to_excel(r'H:\Science\Datasets\Underscore2s.xlsx')
