"""
Because I’ll need a harmonized dataset as a reference to understand the
tree-rings, I’m going to create a python file to do dataset harmonization.
I know we may change the corrections for the later half of the available
data; however, I can at least get the code ready so we can quickly
run it later and get the answer.
"""

# What are the current offsets (these are subject to change!)
# 1986 - 1991: Add 1.80 +- 0.18 to Heidelberg Data
# 1991 - 1994: Add 1.88 +- 0.16 to Heidelberg Data
# 1994 - 2006: No offset applied
# 2006 - 2009: Add 0.49 +- 0.07 to Heidelberg
# 2009 - 2012: Apply NO offset
# 2012 - 2016: Subtract 0.52 +- 0.06 to Heidelberg.

# steps to harmonize the dataset
# 1. Check what Rachel did. (see her page 203. It seems she just applied
# the offsets that she calculated and combined the datasets.

# 2. Load up all the data.

# 3. Index them according to the times above, and apply the offsets.

# 4. Merge the datasets into one.

# 5. Create a template of x-values to output

# (in the future, users can just add their samples x-values to this template and
# get the output they need to do subtraction)

# 6. Re-smooth the data using CCGCRV getTrendValues, with specific x's in mind
# (what x-values do I want to return that will be most useful?
#test





