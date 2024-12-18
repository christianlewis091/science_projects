"""
Dec 16, 24
This scripts relates to the second iteration of our tree-ring based research on Southern Ocean change.
In this script, I want to make sure that I've accumulated all relevant ocean DIC data, that we can use to udnerstand
Southern Ocean changes in radiocarbon over time. I'll incorporate the GLODAP data that I used in the first paper,
add data included in Graven et. al 2012. I'll also include JCT's drake passage data. But all the data needs to be cleaned,
processed, and live in one file for me to be happy with continuing it into a further stage of the project.
"""

import pandas as pd
from functions_v1 import glodap_C14, cchdo_C14, cchdo_cleaning, glodap_cchdo_merge, map_check

maindir = 'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings_paper2' # store the main directory for this work for ease of later use

"""
First, I'm going to read in, and clean up the GLODAP data. The function I've added above reads in the GLODAP merged
file, extracts data south of 5S, shallower than 100m, starting at 1980. Once it's verified to work, I'll comment it out, and move on.
"""

# glodap_C14('glodap_v1')

"""
I'm also interseted in the CCHDO (CLIVAR and Carbon Hydrographic Data Office); are there any cruises that are in here, 
that are not captured in GLODAP? 

I went to this website
https://cchdo.ucsd.edu/
The following was entered into the search box above to find the data in cchdo_results directory below
entered bbox -180,-90,180,-5, and 1980-2024. 
The function below concatonates all of the individual cruise data, and filters out those that don't have DELC14 in the columns

This function only concatonates the individual cruise files. The data is "cleaned" in a next step, so that I don't have 
to loop thruogh the indivudla files every times I'm trying to build the "clean" function.
"""
#
# cchdo_C14('cchdo_dataset')

"""
The function below reads in the concatonated data, removes blank rows (row with units, row with "END_DATA")
and exports a cleaned version of CCHDO expocodes without random white spaces
"""

# cchdo_cleaning()

"""
So now, overlapping datasets have been removed. it's time to merge the GLODAP and CCHDO files. 
"""

# glodap_cchdo_merge()

"""
Have a look at the maps. 
"""

# map_check()

# TODO
"""
From looking at the maps generated above, I can tell that there only a few years where CCHDO has data that GLODAP doesn't. 
That is in 2016, 2017, 2018, and 2019. For these years, I can figure out what those EXPOCODES are, and specifically include that CCHDO data, the rest will be removed. 
"""