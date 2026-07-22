"""
After the data quality paper, we found we needed to check the WTW error progresion more, 
And how the chi2 is changeing through time. 
Also recently we've had issues with potential beam chopping.
This led me to create two scripts that, if we can work it into our normal workflow, would be benefitial. 

The first is the Running_WTW.py script, which calculated the running sigbw, so we can check if a wheel has thrown off the data
The second is the context_2.py and context_analysis.py, which use run data to assess ratios wrt currents. 
"""
"""
STEPS TO FOLLOW:
1. PUT THE WHEEL'S CONTEXT FILE IN THE FOLER HERE: 
(r"I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\context_3600_to_")

2. RUN HY'S CBL EXPORT SCRIPT 
"""

from context_2 import context_analysis

# tell if if any of the added wheels is high precision
# it needs this to find and plot the oxalics based on their position: 
hp = [3600,3601,3602,3605,3606,3607,3609,3610,3612,3613,3617,3620,3621,3623]

# run the function to make the plots. 
# find the plots here: 
# I:\C14Data\C14_blank_corrections_NEW\quality_assurance\Monthly_Data_Quality_checks\output\context_plots\
context_analysis(hp)

