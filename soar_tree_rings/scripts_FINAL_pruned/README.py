"""
21/03/25

Over the nearly 3 years of this tree-ring work, I have simultaneously learned to code while developing all the code
required for this project. While I've tried to keep it "tidy" the code has grown and shrunk over the years with us
trying different analyses or adding new processes or things to analyze such as glodap, hysplit, or thinking of different
ways to think about our tree ring measurements. Finally the journey is over as I've gone through submission, reviews, etc.
I want to finally go back through it all and remove all the unnecesary junk.

I hope that what remains is one (albeit long) script that flows throughout the work from start to finish. Because the
script involves Monte Carlo simulation (and doing that up to 10,000 iterations should remove any variability) for curve
smoothing, I will not copy or edit final numbers that come out of this script, as I'll only run it to 10 or 100 interations.
But I WILL check to make sure there are agreements and no problems.

I will attempt to ensure there is extensive commentary along side each section of the code for posterity, and for
myself 10 years from now (10 years from now me will probably think "Where are all the comments" anyway...)

"""
from PyAstronomy import pyasl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from X_miller_curve_algorithm import ccgFilter
from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.gridspec as gridspec
from scipy import stats
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

"""
Functions that appear in the script will be described in the frist section here, below
"""

"""
"long_date_to_decimal_date" function takes dates in the form of dd/mm/yyyy and converts them to a decimal. 
This was required for the heidelberg cape grim dataset, and is quite useful overall while date formatting can be in 
so many different forms. 
Arguments: 
x = column of dates in the form dd/mm/yyyy
Outputs: 
array = column of dates in the form yyyy.decimal 
To see an example, uncomment the following lines of code directly below the function definition: 
"""

def long_date_to_decimal_date(x):
    array = []  # define an empty array in which the data will be stored
    for i in range(0, len(x)):  # initialize the for loop to run the length of our dataset (x)
        j = x[i]  # assign j: grab the i'th value from our dataset (x)
        decy = pyasl.decimalYear(j)  # The heavy lifting is done via this Py-astronomy package
        decy = float(decy)  # change to a float - this may be required for appending data to the array
        array.append(decy)  # append it all together into a useful column of data
    return array  # return the new data


"""
The following two functions are quite similar, so this short explanation will apply to both. 
"monte_carlo_randomization_Trend" is used heavily in the heidelberg intercomparison project. 
This function takes some time series x and y data, smooths it using the CCGCRV FFT filter algorithm: 
( https://gml.noaa.gov/ccgg/mbl/crvfit/crvfit.html ) and returns data at the x-values that you select. 
The first "trend" gets rid of seasonality and smooths more. 
The second "smooth" includes seasonality and smooths less. 

This function has three separate for-loops: 
The first for-loop: 
Takes an input array of time-series data and randomizes each data point
within its measurements uncertainty. It does this "n" times, and vertically stacks it.
For example, if you have a dataset with 10 measurements, and "n" is 1000, you will end
up with an array of dimension (10x1000).
If you're interested in re-testing how the normal distribution randomization works, you can copy and paste the 
following few lines of code. This shows that indeed, the randomization does have a higher probability of putting the 
randomized point closer to the mean, but actually the distribution follows the gaussian curve. 
###########################
array = []
for i in range(0,10000):
    rand = np.random.normal(10, 2, size=None)
    array.append(rand)
plt.hist(array, bins=100)
plt.show()
###########################

The second for-loop: 
Takes each row of the array (each row of "randomized data") and puts it through
the ccgFilter curve smoother. It is important to define your own x-values that you want output
if you want to compare two curves (this will keep arrays the same dimension).
Each row from the fist loop is smoothed and stacked into yet another new array.

The third for-loop: 
Find the mean, standard deviation, and upper and lower uncertainty bounds of each
"point" in the dataset. This loop takes the mean of all the first measurements, then all the second, etc.

For clarty, I will define all of the arguments here below: 
FIRST 4 ARGUMENTS MUST BE EXTRACTED FROM A PANDAS DATAFRAME. If your code doesn't work, try checking the format.
x_init: x-values of the dataset that you want to smooth. Must be in decimal date format. 
fake_x: x-values of the data you want OUTPUT
y_init: y-values of the dataset that you want to smooth. 
y_error: y-value errors of the dataset that you want to smooth. 
cutoff: for the CCGCRV algoritm, lower numbers smooth less, and higher numbers smooth more. 
    See hyperlink above for more details. 
n: how many iterations do you want to run? When writing code, keep this low. Once code is solid, increase to 10,000. 

### If you want to see this function in action, refer to "MonteCarlo_Explained.py"
https://github.com/christianlewis091/radiocarbon_intercomparison/blob/dev/interlab_comparison/MonteCarlo_Explained.py

"""

def monte_carlo_randomization_trend(x_init, fake_x, y_init, y_error, cutoff, n):  # explanation of arguments above
    # THE WAY I AM WRITING THE CODE:
    # ALL VARIABLES MUST BE EXTRACTED FROM A PANDAS DATAFRAME. If your code doesn't work, try checking the format.

    x_init = x_init.reset_index(drop=True)  # ensure x-values begin at index 0
    y_init = y_init.reset_index(drop=True)  # ensure y-values begin at index 0
    y_error = y_error.reset_index(drop=True)  # ensure y err-values begin at index 0
    # fake_x_for_dataframe = fake_x.reset_index(drop=True)  # ensure output x-values at index 0
    # fake_x_for_dataframe = fake_x_for_dataframe['x']  # if not already extracted, extract the data from the DataFrame

    # First for-loop: randomize the y-values.

    # The line below: creates a copy of the y-value column. This is helpful because as I randomize the y-data, I will
    # stack each new randomized column. So if n = 10, there will 10 stacked, randomized columns. The initial column
    # was helpful to get the code running - was something to "stick the stack on". Not sure if this was required, but
    # it helped me get the for-loop to run.
    new_array = y_init

    for i in range(0, n):  # initialize the for-loop. It will run "n" times.
        empty_array = []  # initialize an empty array to add each individual value onto.
        for j in range(0, len(y_init)):  # nested loop: run through the column of y-data, length-of-y times.
            a = y_init[j]  # grab the j'th item in the y-value set
            b = y_error[j]  # grab the j'th item in the uncertainty set
            # return a random value in the normal distribution of a data point/error
            rand = np.random.normal(a, b, size=None)
            # (https://numpy.org/doc/stable/reference/random/generated/numpy.random.normal.html)
            empty_array.append(rand)  # append this randomized value to my growing list, the "empty_array"
        # the nested loop just finished filling another iteration of the empty array.
        # Now stack this onto our initialized "new_array" from line 89.
        new_array = np.vstack((new_array, empty_array))
        # The line below takes the new array and puts it into a pandas DataFrame.
        # This helps format the data in a way where it can be more quickly tested, and used in the future.
        # To plot the randomized data, index each row using randomized_dataframe.iloc[0]
    randomized_dataframe = pd.DataFrame(new_array)

    # end of first for-loop
    ##################################################################################################################
    ##################################################################################################################
    ##################################################################################################################
    # Second for-loop: smooth the randomized data using John Miller's CCGCRV.

    # Create an initial, trended array on which later arrays that are created will stack
    template_array = ccgFilter(x_init, new_array[0], cutoff).getTrendValue(fake_x)

    # this for smooths each row of the randomized array from above, and stacks it up
    for k in range(0, len(new_array)):
        row = new_array[k]  # grab the first row of the data
        smooth = ccgFilter(x_init, row, cutoff).getTrendValue(fake_x)  # outputs smooth values at my desired times, x
        template_array = np.vstack((template_array, smooth))

    # over time I have had to go between horizontal and vertical stacking of the data as I learn more about programming.
    # beacuse it could lead to confusion, I've provided both types of DataFrames here on the two following lines,
    # one where each iteration is contained as ROWS and one where each iteration is contained as a COLUMN.

    # each ROW is a new iteration. each COLUMN in a given X value
    smoothed_dataframe = pd.DataFrame(template_array)
    # each COLUMN is a new iteration. Each ROW is a given X value
    smoothed_dataframe_trans = pd.DataFrame.transpose(smoothed_dataframe)

    mean_array = []
    stdev_array = []
    for i in range(0, len(smoothed_dataframe_trans)):
        row = smoothed_dataframe_trans.iloc[i]  # grab the first row of data
        stdev = np.std(row)  # compute the standard deviation of that row
        sum1 = np.sum(row)  # take the sum, and then mean (next line) of that data
        mean1 = sum1 / len(row)  # find the mean of that row
        mean_array.append(mean1)  # append the mean it to a new array
        stdev_array.append(stdev)  # append the stdev to a new array

    summary = pd.DataFrame({"Means": mean_array, "stdevs": stdev_array})

    return randomized_dataframe, smoothed_dataframe, summary


"""
Referece1.py 
The development of the background reference. Through the years of work we decided to use the background where we simply
add the Cape Grim Data into the Baring Head data gaps, and not apply any offset corrections or anything like that.
This chunk will create the background reference. 
"""
# READ IN the BARING HEAD RECORD and UNIVERSITY of HEIDELBERG CAPE GRIM RECORD
heidelberg = pd.read_excel(r'H:\Science\Datasets\heidelberg_cape_grim.xlsx', skiprows=40)
baringhead = pd.read_excel(r'H:\Science\Datasets\BHD_14CO2_datasets_20211013.xlsx')

# adding a key that can be useful later.
heidelberg['key'] = np.ones(len(heidelberg))
baringhead['key'] = np.zeros(len(baringhead))

# the heidelbeg cape grim data set, for me, was easier to work with if I converted the dates from their YYYY-DD type
# formats to decimal date formats
x_init_heid = heidelberg['Average pf Start-date and enddate']  # x-values from heidelberg dataset
x_init_heid = long_date_to_decimal_date(x_init_heid)
heidelberg['Decimal_date'] = x_init_heid  # add these decimal dates onto the dataframe

# drop NaN's in the column I'm most interested in
heidelberg = heidelberg.dropna(subset=['D14C'])
heidelberg = heidelberg.loc[(heidelberg['D14C'] > 10)]
baringhead = baringhead.dropna(subset=['DELTA14C'])

# snip out the gaps: 1994 - 2006, and 2009 - 2012, and then merge back together
# Now as a more experienced programmer (sort of...) I know this could be done in one-line with pandas, but
# I'm now going to change it now. This effort is get rid of code that is wholly unused in the final work.
snip = baringhead.loc[(baringhead['DEC_DECAY_CORR'] < 1994)]
snip2 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2006) & (baringhead['DEC_DECAY_CORR'] < 2009)]
snip3 = baringhead.loc[(baringhead['DEC_DECAY_CORR'] > 2012)]
snip = pd.merge(snip, snip2, how='outer')
snip = pd.merge(snip, snip3, how='outer')
baringhead = snip.reset_index(drop=True)

cgo = heidelberg.loc[(heidelberg['Decimal_date'] > 1994) & (heidelberg['Decimal_date'] < 2006)]
cgo2 = heidelberg.loc[(heidelberg['Decimal_date'] > 2009) & (heidelberg['Decimal_date'] < 2012)]
cgo = pd.merge(cgo, cgo2, how='outer')

# drop some of the unnecessary columns that add clutter to the process
heidelberg = heidelberg.drop(columns=['#location', 'sampler_id', 'samplingheight', 'startdate', 'enddate',
                                      'Average pf Start-date and enddate', 'date_d_mm_yr', 'date_as_number',
                                      'samplingpattern',
                                      'wheightedanalyticalstdev_D14C', 'nbanalysis_D14C', 'd13C', 'flag_D14C',
                                      ], axis=1)
baringhead = baringhead.drop(columns=['SITE', 'NZPREFIX', 'NZ', 'DATE_ST', 'DATE_END', 'DAYS_EXP',
                                      'DATE_COLL', 'date_as_number', 'DELTA13C_IRMS',
                                      'F14C', 'F14C_ERR', 'FLAG', 'METH_VESSEL',
                                      'METH_COLL'])

# for simplicity (and because I'm indexing the Heidelberg dataset much more than the Baring Head dataset right now, I'm going to change the
# baringhead column names to match those of the Heidelberg dataset
baringhead = baringhead.rename(columns={"DEC_DECAY_CORR": "Decimal_date"})
baringhead = baringhead.rename(columns={"DELTA14C": "D14C"})
baringhead = baringhead.rename(columns={"DELTA14C_ERR": "weightedstderr_D14C"})

reference1 = pd.merge(baringhead, cgo, how='outer')
reference1 = reference1.loc[(reference1['weightedstderr_D14C'] > 0)]

reference1.sort_values(by=['Decimal_date'], inplace=True)
# reference1.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference1/reference1.xlsx')
# changing output location to final place Dec 4, 2024
reference1.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_pruned/reference1.xlsx')


"""
Tree_Ring_Analysis.py
In reading in the file, the comment says 'manually edited from Pene's work'. This refers to extra runs 
of Raul Marin Balmaceda. Those extra runs were added into the SOAR tree ring excel sheet after Jocelyn wanted to double
check that there were any ring count errors. 
"""

# read in the Tree Ring data. Pene's data from tree_rings_second_check was manually added to this file before read-in.
df = pd.read_excel(r'H:\Science\Datasets\SOARTreeRingData2022-02-01_August_1_2024.xlsx', comment='#')

# replace the site "names" from people's addresses to more generic names for a publication:
df = df.replace({'19 Nikau St, Eastbourne, NZ': "Eastbourne 1, NZ",
                 '23 Nikau St, Eastbourne, NZ': "Eastbourne 2, NZ",
                 'Bahia San Pedro, Chile': 'Bahia San Pedro, CH',
                 'Baja Rosales, Isla Navarino':'Baja Rosales, Isla Navarino, CH',
                 'Baring Head, NZ':'Baring Head, NZ',
                 'Haast Beach, paddock near beach':'Haast Beach, NZ',
                 "Mason's Bay Homestead":"Mason's Bay, NZ",
                 'Monte Tarn, Punta Arenas':'Monte Tarn, Punta Arenas, CH',
                 'Muriwai Beach Surf Club':'Muriwai Beach, NZ',
                 'Oreti Beach': 'Oreti Beach, NZ',
                 'Puerto Navarino, Isla Navarino':'Puerto Navarino, Isla Navarino, CH',
                 'Raul Marin Balmaceda': 'Raul Marin Balmaceda, CH',
                 'Seno Skyring': 'Seno Skyring, CH',
                 'Tortel island': 'Tortel Island, CH',
                 'Tortel river': 'Tortel River, CH',
                 "World's Loneliest Tree, Camp Cove, Campbell island": "Campbell Island, NZ",
                 'near Kapuni school field, NZ': 'Taranaki, NZ'})

# On January 2, 2025, I noticed that the line below was commented out. I don't know why this was the case, and
# Obviously it was an error. Currnetly the duplicates are removed near line 141. # df = df.drop_duplicates(subset='Ring code')
df = df.dropna(subset='∆14C').reset_index(drop=True)  # drop any data rows that doesn't have 14C data.

# Extract the Tree and Core data which can be used to filter and plot during the next phase.
# This helps us see each core individually even if there are multiple by site.
newdesc = []
for i in range(0, len(df)):
    row = df.iloc[i]

    if row['Site'] == "19 Nikau St, Eastbourne, NZ":
        ringcode = row['Ring code']
        ringcode = ringcode[6:11]
    elif row['Site'] == "23 Nikau St, Eastbourne, NZ":
        ringcode = row['Ring code']
        ringcode = ringcode[6:11]
    elif row['Site'] == "near Kapuni school field, NZ":
        ringcode = row['Ring code']
        ringcode = ringcode[8:13]
    else:
        ringcode = row['Ring code']
        ringcode = ringcode[4:9]

    newdesc.append(ringcode)

df['TreeandCore'] = newdesc

# Lets plot each site, and see where there are obvious bad rings counts...
# 21/03/25
# During this process of quality checking etc, I also discovered for instance that there are 3 points in Campbell Island
# 2 from the same core. Upon closer inspection, WLT-T2-C2-R9 was measured twice, once at RRL, and once at Australian tiol University AMS facility
sites = np.unique(df['Site'])
for i in range(0, len(sites)):

    # loop into the first site
    this_site = df.loc[df['Site'] == sites[i]]

    # how many unique tree cores are in this site?
    cores = np.unique(this_site['TreeandCore'])
    fig = plt.figure()
    for j in range(0, len(cores)):
        this_core = this_site.loc[this_site['TreeandCore'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.scatter(this_core['DecimalDate'], this_core['∆14C'], label=f'{cores[j]}')
    plt.plot(reference1['Decimal_date'], reference1['D14C'], label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
    plt.legend()
    plt.xlabel('Date', fontsize=14)
    plt.title(f'{sites[i]}')
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/unfiltered_{sites[i]}.png', dpi=300, bbox_inches="tight")
    plt.close()

# We decided the following samples were bad, so we first apply a broad 'CBL' flag of '...' and then selectively apply
# specific flags where the data does indeed have problems.
df['CBL_flag'] = '...'
df.loc[(df['C14Flag'] != '...'), 'CBL_flag'] = 'Already flagged by JCT in original database.'
df.loc[(df['Site'] == "Bahia San Pedro, CH") & (df['DecimalDate'] <= 2005), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 1 and Tree 2 deviate before 2005. Therefore I am removing all data < 2005'
df.loc[(df['Site'] == "Mason's Bay, NZ"), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only one record exists, and is post-bomb spike - therefore cannot be validated.'
df.loc[(df['Site'] == "Monte Tarn, Punta Arenas, CH") & (df['TreeandCore'] == 'T5-C1'), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Tree 5 Core 1 does not match bomb spike.'
df.loc[(df['Site'] == "Muriwai Beach, NZ"), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only one record exists, and is post-bomb spike - therefore cannot be validated.'
# df.loc[(df['Site'] == "Raul Marin Balmaceda") & (df['TreeandCore'] != 'T7-C1'), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only Tree 7 Core 1 matches bomb spike, all others from this site are wrong.'
# the line below was added to simply remove all data from Raul Marin since we found in 2024 from Pene's work that there was a ring count error in the ones we thought were OK.
df.loc[(df['Site'] == "Raul Marin Balmaceda, CH"), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: Only Tree 7 Core 1 matches bomb spike, all others from this site are wrong.'
df.loc[(df['Site'] == "Oreti Beach, NZ") & (df['C14Flag'] == '.X.'), 'CBL_flag'] = 'REMOVED FROM ANALYSIS: This was flagged by JCT as potentially bad count.'
df.loc[(df['Site'] == "Taranaki, NZ"), 'CBL_flag'] = 'Not included further. Not close enough to coastline and weird winds around taranaki,Tree 1 Core 4 does not match bomb spike.'

# select only the GOOD DATA to work with from now on.
df_cleaned = df.loc[(df['CBL_flag']) == '...']

print(f'I discovered an issue during reviews (2/2/25), that duplicates and triplicates exist in the tree ring records due to a bug in RLIMS. How long was it before? {len(df_cleaned)}')
df_cleaned = df_cleaned.drop_duplicates(subset='Ring code')
df_cleaned.to_excel('C:/Users\clewis\IdeaProjects\GNS\soar_tree_rings\output_EGU_pruned/SOARTreeRingData_CBL_cleaned_aug_1_2024.xlsx')
print(f'I discovered an issue during reviews(2/2/25), that duplicates and triplicates exist in the tree ring records due to a bug in RLIMS. How long is it after? {len(df_cleaned)}')


# re-write the plots with only the cleaned data
sites = np.unique(df_cleaned['Site'])
for i in range(0, len(sites)):

    # loop into the first site
    this_site = df_cleaned.loc[df_cleaned['Site'] == sites[i]]

    # how many unique tree cores are in this site?
    cores = np.unique(this_site['TreeandCore'])
    fig = plt.figure()
    for j in range(0, len(cores)):
        this_core = this_site.loc[this_site['TreeandCore'] == cores[j]]
        # used to do errorbar but they're too small to se anyway compared to the data
        plt.scatter(this_core['DecimalDate'], this_core['∆14C'], label=f'{cores[j]}')
    plt.plot(reference1['Decimal_date'], reference1['D14C'], label='SH Atmosphere \u0394$^1$$^4$CO$_2$ (\u2030)', color='black', alpha=0.2)
    plt.legend()
    plt.xlabel('Date', fontsize=14)
    plt.title(f'{sites[i]}')
    plt.ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)', fontsize=14)  # label the y axis
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/CLEANED_{sites[i]}.png',
        dpi=300, bbox_inches="tight")
    # changing output location for final checks
    plt.savefig(
        f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Images_and_Figures/tree_ring_analysis/cleaned_plots/{sites[i]}.png', dpi=300, bbox_inches="tight")
    plt.close()

"""
Reference_to_xvals.py and reference_to_xvals2.py
Now, we've made the Southern Hemisphere background (SHB) (Cape Grim + Baring Head; Reference1.py); we've made sure we're 
happy with all the tree ring measurements (tree_ring_analysis.py (above) 
and now we want to find the difference between the background reference and the tree-rings. 
"""

# in a previous version of the script, I read in the cleaned tree ring data as samples, so I'm going to just change the
# name here. I want to avoid as much reading in and out as possible.
samples = df_cleaned

# in terms of "samples", during the paper reviews, I was asked to compare our data with that of the Univesrity of Heidelberg's
# Macquarie Island data, and Chris Turney's 2018 Campbell Island record.
# In order to compare those, I had to -in post, add them to the sample set to get them through the analysis.
# In this "culling"/"trimming" of code, I'm going to stitch them all together here.
# The MCQ (Macquarie Island) record also needs the data to be edited into Decimal date to be adaptable in the curve smoothing step.
mcq = pd.read_excel('H:/Science/Datasets/heidelberg_MQA.xlsx')
res = []
# need to convert MCQ dates to decimal dates
for i in range(0, len(mcq)):
    row = mcq.iloc[i]
    date_string = str(row['Average of Dates'])
    date_string = date_string[:10]
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    decimal_date = date_object.year + (date_object.timetuple().tm_yday - 1) / 365.25
    res.append(decimal_date)
mcq['Average of Dates'] = res

mcq = mcq[['#location', 'Average of Dates', 'D14C','1sigma_error']]
mcq = mcq.rename(columns={'#location': 'Site', 'Average of Dates': 'DecimalDate', '1sigma_error':'∆14Cerr','D14C':'∆14C'})
samples = pd.concat([samples, mcq])

# Also add Turney's data and adjust so it fits the form of our dataframe
ct = pd.read_excel('H:/Science/Datasets/Turney2018.xlsx', comment='#')
ct = ct.loc[ct['Year'] > 1979]
ct = ct.rename(columns={'location': 'Site', 'Year': 'DecimalDate', '1sigma':'∆14Cerr','14C':'∆14C'})
samples = pd.concat([samples, ct])

# Now we're ready to start smoothing the curve so we can interface the samples with the SHB. In past code, I've re-loaded reference1 and called it ref1
# lets simply rename it now. In the past, I've also been using the "smooth" and "trend" version of CCGCRV, but we only use "trend" in the end, so I'm going
# to remove references to smooth, AND I'm going to remove references that use an offset-corrected SHB.
ref1 = reference1

# set some parameters for the CCGCRV smoothing algortih
output_xvals = pd.concat([ref1['Decimal_date'], samples['DecimalDate']]).reset_index(drop=True)
output_xvals = pd.DataFrame({'x': output_xvals}).sort_values(by=['x'], ascending=True).reset_index(drop=True)

n = 5  # set the amount of times the code will iterate (set to 10,000 once everything is final)
cutoff = 667  # FFT filter cutoff

# an important point is that, in the previous years we had been trying loads of different iterations for SHB.
# At one point, some were dropped and reference 3 and reference 1 were the same. This is why I'm referring to ref3
# but calling dates and D14C values for ref1.
reference3_trend = monte_carlo_randomization_trend(ref1['Decimal_date'], output_xvals['x'], ref1['D14C'], ref1['weightedstderr_D14C'], cutoff, n)
reference3_trend = reference3_trend[2]
montes = pd.DataFrame({'Decimal_date': output_xvals['x'], 'D14C_ref3t_mean': reference3_trend['Means'], 'D14C_ref3t_std': reference3_trend['stdevs']}).drop_duplicates(subset='Decimal_date')
# montes.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output/test.xlsx')
montes.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_REVIEW/Data_Files/monte_output.xlsx')

# Now you kind of have to extract the data and associate a given REFERENCE POINT with a sample tree-ring D14C value by matching the dates
D14C_ref3t_mean = []  # initialize an empty array
D14C_ref3t_std = []  # initialize an empty array

for i in range(0, len(samples)):
    samples_row = samples.iloc[i]
    sample_date = samples_row['DecimalDate']

    for k in range(0, len(montes)):
        df_row = montes.iloc[k]
        df_date = df_row['Decimal_date']

        if sample_date == df_date:
            D14C_ref3t_mean.append(df_row['D14C_ref3t_mean'])
            D14C_ref3t_std.append(df_row['D14C_ref3t_std'])

samples['D14C_ref3t_mean'] = D14C_ref3t_mean
samples['D14C_ref3t_std'] = D14C_ref3t_std

# samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/from_reference_to_sample_xvals2/samples_with_references10000.xlsx')
# changing new output location to the EGU submission folder
samples.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/samples_with_references5_210325.xlsx')

"""
Main_analysis.py
Now we'll actually calculate the differences and then make the main figures that go into the paper. 
"""
# In main_analysis.py, I referred to the samples at "df", so I'm going to rename that here so I don't have
# to edit the names and introduce new bugs.
# I also need to read in the 2 year site-site comparison between BHD and Cape Grim
df = samples
bhdcgo = pd.read_excel(r'H:\Science\Datasets\CGOvBHD.xlsx')

# ensure all data are sliced for after 1980. We're interested in 1980 to the present
df = df.loc[df['DecimalDate'] > 1980].reset_index(drop=True)
ref1 = ref1.loc[ref1['Decimal_date'] > 1980].reset_index(drop=True)
df = df.sort_values(by=['DecimalDate'])

# December 4, 2023: Removing Kapuni and Raul Marin after it was deemed that these sites have bad ring counts.
# Raul Marin was determined so by Pene's work
df = df.loc[df['Site'] != 'Raul Marin Balmaceda']
df = df.loc[df['Site'] != 'near Kapuni school field, NZ']

#
#
#
# FOR METHODS SECTION: DEVELOPMENT OF BACKGROUND REFERENCE:
# WE WANT TO SHOW THE DEVELOPMENT OF REFERENCE, WITH A MAP, AND PLOT OF THE DATA TOGETHER
#
#
#

fig = plt.figure(figsize=(16, 4))
gs = gridspec.GridSpec(1, 3)
gs.update(wspace=.15, hspace=0.1)

# BHD MAP
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
maxlat = -40+20
minlat = -40-20
nz_max_lon = 180
nz_min_lon = 140
ax1.set_extent([nz_min_lon, nz_max_lon, minlat, maxlat], crs=ccrs.PlateCarree())  # Set map extent
ax1.add_feature(cf.OCEAN)
ax1.add_feature(cf.LAND, edgecolor='black')
ax1.gridlines()

# Plot points
baring_head = (174.866, -41.4)
cape_grim = (144.6883, -40.6822)

ax1.scatter(*baring_head, color='red', edgecolor='black', transform=ccrs.PlateCarree(), label="Baring Head", s=50)
ax1.scatter(*cape_grim, color='blue', edgecolor='black', transform=ccrs.PlateCarree(), label="Cape Grim", s=50)

ax1.legend(loc='lower left')

ax2 = fig.add_subplot(gs[0, 1])

ax2.set_title("Background Reference")
ax2.set_xlabel("Year")
ax2.set_ylabel('\u0394$^1$$^4$C (\u2030)')

cgo = ref1.loc[ref1['#location'] == 'CGO']
bhd = ref1.loc[ref1['#location'] != 'CGO']

ax2.plot(df['DecimalDate'], df['D14C_ref3t_mean'], zorder=10, label='CCGCRV Trend Reference', color='black')
ax2.errorbar(cgo['Decimal_date'], cgo['D14C'], yerr=cgo['weightedstderr_D14C'], fmt='D',  elinewidth=1, capsize=2, label='Heidelberg Uni. Cape Grim Record', color='blue',  markersize = 2, alpha=0.75)
ax2.errorbar(bhd['Decimal_date'], bhd['D14C'], yerr=bhd['weightedstderr_D14C'], fmt='o',  elinewidth=1, capsize=2, label='RRL/NIWA Wellington Record', color='red',  markersize =2, alpha=0.75)
ax2.legend()

ax3 = fig.add_subplot(gs[0, 2])

x = bhdcgo['Date']
x = long_date_to_decimal_date(x)
bhdcgo['Date'] = x
c = stats.ttest_rel(bhdcgo['BHD_D14C'], bhdcgo['CGO_D14C'])
ax3.errorbar(bhdcgo['Date'], bhdcgo['BHD_D14C'], yerr=bhdcgo['standard deviation1'], fmt='o',  elinewidth=1, capsize=2, label='Baring Head measured by RRL/NIWA', color='green',  markersize = 4)
ax3.errorbar(bhdcgo['Date'], bhdcgo['CGO_D14C'], yerr=bhdcgo['standard deviation2'], fmt='x',  elinewidth=1, capsize=2, label='Cape Grim measured by RRL/NIWA', color='purple',  markersize = 4)
ax3.set_title('Site Intercomparison')
ax3.set_ylabel('\u0394$^1$$^4$C (\u2030)')  # label the y axis
ax3.set_xlabel('Year')
ax3.legend()
ax3.locator_params(axis='x', nbins=4)
ax3.set_xlim(2017, 2019)

plt.savefig(
    f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/New_Figure1.png',
    dpi=300, bbox_inches="tight")
plt.close()

""" 
The following code block adds lats and lons to certain cites that were missing data
Need to add a flag for the "Chile" versus "NZ" datasets
Also, all the Lon data are not systematically E or W so the Chilean data needs to be *-1 for the lon. 
This block of code cleans up all the messiness in the lats and lons, and gives us flags to index later based on country
"""

df.loc[df['Site'] == 'Eastbourne 1, NZ', 'Lat'] = -41.2923
df.loc[df['Site'] == 'Eastbourne 1, NZ', 'Lon'] = 174.8971
df.loc[df['Site'] == 'Eastbourne 2, NZ', 'Lat'] = -41.2923
df.loc[df['Site'] == 'Eastbourne 2, NZ', 'Lon'] = 174.8971
df['Country'] = -999
# Turney's data and MCQ data are not applicable to the following lines since they haven't been assigned a lat or lon
df.loc[df['Lon'] > 90, 'Country'] = 1 # new zealand
df.loc[(df['Lon'] > 50) & (df['Lon'] < 90) , 'Country'] = 0 # chile
df.loc[df['Country'] == 0, 'Lon'] *= -1

df = df.drop_duplicates().reset_index(drop=True)

# renaming columns
df = df.rename(columns={'∆14C':'D14C_1'})
df = df.rename(columns = {'∆14Cerr':'weightedstderr_D14C_1'})

# Finally calculate the differnece and propogated error between samples and reference
df['r3_diff_trend'] = df['D14C_1'] - df['D14C_ref3t_mean']
df['r3_diff_trend_errprop'] = np.sqrt(df['weightedstderr_D14C_1'] ** 2 + df['D14C_ref3t_std'] ** 2)

df = df.sort_values(by=['Site','DecimalDate'])

df.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/final_results.xlsx')

# SORT VALUES BY LATITUDE SO THEY APPEAR IN ORDER ON THE PLOTS LATER
df = df.sort_values(by=['Lat', 'DecimalDate'], ascending=False).reset_index(drop=True)

# first we'll extract the data by country flags that we've added above
chile = df.loc[df['Country'] == 0].reset_index(drop=True)
nz = df.loc[df['Country'] == 1].reset_index(drop=True)

# GETS "LOCS", LOCATIONS, WHILE PRESERVING LATITUDES IN PREVIOUSLY SORTED ORDER
# u, indices = np.unique(a, return_index=True) # https://numpy.org/doc/stable/reference/generated/numpy.unique.html
u1, locs1 = np.unique(chile['Site'], return_index=True)
temp = pd.DataFrame({"ind": u1, "locs":locs1}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs1 = temp['ind']
u2, locs2 = np.unique(nz['Site'], return_index=True)
temp2 = pd.DataFrame({"ind": u2, "locs":locs2}).sort_values(by=['locs'], ascending=True).reset_index(drop=True)
locs2 = temp2['ind']


# PREPARE THE FIGURE
# SELECT COLORS WE"LL USE FOR THE PAPER:
c1, c2, c3, c4, c5, c6, c7, c8 = '#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'
colors = [c1, c2, c3, c4, c5, c6, c7, c8]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']
size1 = 8

site_array = []
lat_array = []
stat_array = []
mean_array = []
std_array = []
region_array = []

for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    # print(slice)
    latitude = slice['Lat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    mean_array.append(np.nanmean(slice['r3_diff_trend']))
    std_array.append(np.nanstd(slice['r3_diff_trend']))
    lat_array.append(latitude)
    site_array.append(str(locs1[i]))
    region_array.append("Chile")

for i in range(0, len(locs2)):
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['Lat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    mean_array.append(np.nanmean(slice['r3_diff_trend']))
    std_array.append(np.nanstd(slice['r3_diff_trend']))
    lat_array.append(latitude)
    site_array.append(str(locs2[i]))
    region_array.append("NZ")

results_array = pd.DataFrame({"Site": site_array, "Region": region_array, "Lat": lat_array, "Mean": mean_array, "Std": std_array})
results_array.to_excel('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/summary_means_March17_2025.xlsx')


"""
NOW CREATE FIGURE 2
"""

# set some parameters
maxlat = -30
minlat = -60
nz_max_lon = 180
nz_min_lon = 155
chile_max_lon = -55
chile_min_lon = -85
res = 'l'
c1, c2, c3, c4, c5, c6, c7, c8 = '#b2182b','#d6604d','#f4a582','#fddbc7','#d1e5f0','#92c5de','#4393c3','#2166ac'
colors = [c1, c2, c3, c4, c5, c6, c7, c8]
markers = ['o', '^', '8', 's', 'p', '*', 'X', 'D']
size1 = 8


# Create a figure
fig = plt.figure(figsize=(10, 10))

# Create a GridSpec with 3 rows and 2 columns
gs = gridspec.GridSpec(3, 2)
gs.update(wspace=0.1, hspace=0.2)
# Add subplots to the GridSpec
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree())
ax1.set_extent([chile_min_lon, chile_max_lon, minlat, maxlat], crs=ccrs.PlateCarree())  # Set map extent
ax1.add_feature(cf.OCEAN)
ax1.add_feature(cf.LAND, edgecolor='gray')
gl = ax1.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False

for i in range(0, len(locs1)):

    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = slice['Lat']
    lat = lat[0]
    lon = slice['Lon']
    lon = lon[0]
    location_cartopy = (lon, lat)
    # print(x, y)
    ax1.scatter(*location_cartopy, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')
ax1.legend()


ax2 = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree())
ax2.set_extent([nz_min_lon, nz_max_lon, minlat, maxlat], crs=ccrs.PlateCarree())  # Set map extent
ax2.add_feature(cf.OCEAN)
ax2.add_feature(cf.LAND, edgecolor='gray')
gl = ax2.gridlines(draw_labels=True)
gl.top_labels = False
gl.right_labels = False

for i in range(0, len(locs2)):

    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    lat = slice['Lat']
    lat = lat[0]
    lon = slice['Lon']
    lon = lon[0]
    location_cartopy = (lon, lat)
    # print(x, y)
    ax2.scatter(*location_cartopy, marker=markers[i],color=colors[i], s=size1*10, edgecolor='black')


ax3 = fig.add_subplot(gs[1, 0])
# df = df.reset_index(drop=True)
df = df.sort_values(by=['DecimalDate'])
ax3.plot(df['DecimalDate'], df['D14C_ref3t_mean'], zorder=10, label='CCGCRV Trend Reference', color='black')
for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    ax3.errorbar(slice['DecimalDate'], slice['D14C_1'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=.3, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor=colors[i])
ax3.set_xticks([], [])
ax3.set_ylim(0, 300)
ax3.set_xlim(1980, 2020)
ax3.set_ylabel('\u0394$^1$$^4$CO$_2$ (\u2030)')
ax3.legend()

ax4 = fig.add_subplot(gs[1, 1])
ax4.plot(df['DecimalDate'], df['D14C_ref3t_mean'], zorder=10, label='Southern Hemisphere Background', color='black')
for i in range(0, len(locs2)):
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.errorbar(slice['DecimalDate'], slice['D14C_1'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=.3, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor=colors[i])
ax4.set_xticks([], [])
ax4.set_yticks([], [])
ax4.set_ylim(0, 300)
ax4.set_xlim(1980, 2020)

ax5 = fig.add_subplot(gs[2, 0])
for i in range(0, len(locs1)):
    slice = chile.loc[chile['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    # print(slice)
    latitude = slice['Lat']
    latitude = latitude[0]
    latitude = round(latitude, 1)
    ax5.errorbar(slice['DecimalDate'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

ax5.set_ylim(-15, 15)
ax5.set_xlim(1980, 2020)
ax5.axhline(0, color='black')
ax5.set_ylabel('\u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
ax5.set_xlabel('Year of Growth')


ax6 = fig.add_subplot(gs[2, 1])
for i in range(0, len(locs2)):
    slice = nz.loc[nz['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    latitude = slice['Lat']
    latitude = latitude[0]
    latitude = round(latitude, 1)

    ax6.errorbar(slice['DecimalDate'], slice['r3_diff_trend'], 0.01, markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(latitude)} N", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')

ax6.set_ylim(-15, 15)
ax6.set_xlim(1980, 2020)
ax6.axhline(0, color='black')
ax6.set_xlabel('Year of Growth')
ax6.set_yticks([], [])


# EB asked for an inset histogram to help vizualize the data...
inset_ax5 = inset_axes(ax5, width="25%", height="25%", loc='upper right')
# Create a histogram
counts, bins, patches = inset_ax5.hist(chile['r3_diff_trend'], bins=10, edgecolor='black', color='gray')
for count, bin_start, bin_end in zip(counts, bins[:-1], bins[1:]):
    print(f"Bin range: {bin_start:.2f} to {bin_end:.2f}, Count: {count}")
inset_ax5.set(xlim=(-10, 10))
print('space')
inset_ax6 = inset_axes(ax6, width="25%", height="25%", loc='upper right')
# Create a histogram
counts, bins, patches = inset_ax6.hist(nz['r3_diff_trend'], bins=10, edgecolor='black', color='gray')
for count, bin_start, bin_end in zip(counts, bins[:-1], bins[1:]):
    print(f"Bin range: {bin_start:.2f} to {bin_end:.2f}, Count: {count}")
inset_ax5.set(xlim=(-10, 10))

# plot trends
ch_x = chile['DecimalDate']
ch_x = np.array(ch_x)
ch_y = chile['r3_diff_trend']
ch_y = np.array(ch_y)

nz_x = nz['DecimalDate']
nz_x = np.array(nz_x)
nz_y = nz['r3_diff_trend']
nz_y = np.array(nz_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch_x, ch_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(nz_x, nz_y)

# I just want the line to go across the plot for easier vizualization...
ch_x = np.append(ch_x, 1980)
ch_x = np.append(ch_x, 2020)
nz_x = np.append(nz_x, 1980)
nz_x = np.append(nz_x, 2020)

ax5.plot(ch_x, slope*ch_x+intercept, color='gray')
ax6.plot(nz_x, sslope*nz_x+sintercept, color='gray')

print("Chile: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))
print("NZ: y=%.3fx+%.3f\R$^2$=%.3f"%(sslope, sintercept,srvalue**2))

plt.savefig(
    f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/New_Figure2.png',
    dpi=300, bbox_inches="tight")

nz1 =  results_array.loc[results_array['Region'] == 'NZ']
nz1_x = nz1['Lat']
nz1_x = np.array(nz1_x)
nz1_y = nz1['Mean']
nz1_y = np.array(nz1_y)

ch1 =  results_array.loc[results_array['Region'] == 'Chile']
ch1_x = ch1['Lat']
ch1_x = np.array(ch1_x)
ch1_y = ch1['Mean']
ch1_y = np.array(ch1_y)

# regress the data
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch1_x, ch1_y)
sslope, sintercept, srvalue, spvalue, sstderr = stats.linregress(nz1_x, nz1_y)

print("ChileMEANS: y=%.3fx+%.3f\R$^2$=%.3f__%.3f"%(slope, intercept,rvalue**2, pvalue))
print("NZMEANS: y=%.3fx+%.3f\R$^2$=%.3f__%.3f"%(sslope, sintercept,srvalue**2, spvalue))

# what is the CHILE_MEAN_regresiion without Monte Tarn?
ch2 =  results_array.loc[(results_array['Region'] == 'Chile') & (results_array['Site'] != 'Monte Tarn, Punta Arenas, CH')]
ch2_x = ch2['Lat']
ch2_x = np.array(ch2_x)
ch2_y = ch2['Mean']
ch2_y = np.array(ch2_y)
slope, intercept, rvalue, pvalue, stderr = stats.linregress(ch2_x, ch2_y)
print("ChileMEANS_NOTARN: y=%.3fx+%.3f\R$^2$=%.3f"%(slope, intercept,rvalue**2))


"""
PLOTTING THE AVERAGES> Trying to get the symbols to match first figure
"""

fig = plt.figure(figsize=(8, 8))
gs = gridspec.GridSpec(4, 4)
gs.update(wspace=1, hspace=0.25)

xtr_subsplot = fig.add_subplot(gs[0:2, 0:4])
chile1 = results_array.loc[results_array['Region'] == 'Chile']
for i in range(0, len(chile1)):
    slice = chile1.loc[chile1['Site'] == str(locs1[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=f"{str(slice['Site'])}", ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
    plt.plot(ch1_x, slope*ch1_x+intercept, color='gray', alpha=0.05)
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.xticks([], [])
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.text(-60+2, 7, '[A] Chile', horizontalalignment='center', verticalalignment='center', fontweight="bold")

xtr_subsplot = fig.add_subplot(gs[2:4, 0:4])
chile1 = results_array.loc[results_array['Region'] == 'NZ']
for i in range(0, len(chile1)):
    slice = chile1.loc[chile1['Site'] == str(locs2[i])].reset_index(drop=True)  # grab the first data to plot, based on location
    label = slice['Site']
    plt.errorbar(slice['Lat'], slice['Mean'], slice['Std'], markersize = size1, elinewidth=1, capsize=2, alpha=1, label=label, ls='none', fmt=markers[i], color=colors[i], ecolor=colors[i], markeredgecolor='black')
    plt.plot(nz1_x, sslope*nz1_x+sintercept, color='gray', alpha=0.05)
#
plt.xlim(-60, -35)
plt.ylim(-8, 8)
plt.axhline(0, color='black', linewidth = 0.5)
plt.ylabel('Mean \u0394\u0394$^1$$^4$CO$_2$ (\u2030)')
plt.xlabel('Latitude (N)')
plt.text(-60+3.5, 7, '[B] New Zealand', horizontalalignment='center', verticalalignment='center', fontweight="bold")

# plt.savefig('C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_OPEN_ACCESS/main_analysis/MainFig2.5.png',
#             dpi=300, bbox_inches="tight")
plt.savefig(
    f'C:/Users/clewis/IdeaProjects/GNS/soar_tree_rings/output_EGU_pruned/New_Figure3.png',
    dpi=300, bbox_inches="tight")
plt.close()

"""
Stopping here as of 23:50 PM on 21/3/25. I may continue if I see fit, but the GLOPDAP and HYSPLIT are more standalone, 
and the specific changes requested by reviewers are tackled in another subfolder which I dont need to hash out again. 
I just wanted to ensure again for the 4th time, that this main analysis works robustly.
"""



































