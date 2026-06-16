import pandas as pd
from X_miller_curve_algorithm import ccgFilter
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(r"H:\Science\Datasets\bhd_picarro_sip_co_2019-2024.csv")

# # FAKE X DATA
# t = np.linspace(0, 10, 200)
#
# # FAKE Y DATA
# input_y = np.sin(t) + 0.2 * np.random.randn(len(t))
#
# # FAKE X OUTPUT DATA
t2 = np.linspace(2019, 2025.5, 2000)

# THIS IS THE FUNCTION
output_y_smooth = ccgFilter(df['yearfraction'], df['co'], 664).getSmoothValue(df['yearfraction'])

plt.figure(figsize=(8, 4))
plt.plot(df['yearfraction'], df['co'], 'o', label='Original data', alpha=0.6)
plt.plot(df['yearfraction'], output_y_smooth, '-', label='Interpolated (smoothed)')
plt.xlabel('Time')
plt.ylabel('Signal')
plt.legend()
plt.title('Original vs. Interpolated Data')
plt.grid(True)
plt.tight_layout()
plt.show()

df['background_CO'] = output_y_smooth
df.to_excel(r"H:\Science\Datasets\bhd_picarro_sip_co_2019-2024_SmoothedCO.xlsx")



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
