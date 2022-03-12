import pandas as pd
import random
import numpy as np


x = [1,2,4]
y = [1,5,15]
print(type(x))
# create random measurements and standard deviations to test
measurements = []
for i in range(0, 100):
    measurement = random.uniform(10.5, 75.5)
    measurements.append(measurement)
# print(measurements)
print(type(measurements))
stdevs = []
for i in range(0, 100):
    stdev = random.uniform(0, 1)
    stdevs.append(stdev)
# print(stdevs)

# First step is to get the measurement to randomize within its uncertainty

new_array = measurements
n = 21
cols = np.linspace(0, len(measurements))

for i in range(0, 10):
    empty_array = []
    for j in range(0, len(measurements)):
        a = measurements[j]  # grab the first item in the set
        b = stdevs[j]  # grab the uncertainty
        rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
        c = a + rand  # add this to the number
        empty_array.append(c)  # add this to a list
        print(len(empty_array))
    new_array = np.vstack((new_array, empty_array))
print(new_array)
print(len(new_array[1]))
print(np.shape(new_array))
# coeff = pd.DataFrame(empty_array, columns=cols)
# print(coeff)

#



#
# """ Data starts as a list, but by the time it gets to "p", it has become a numpy array.  """
# n = 4
# empty_array = []  # pre-allocate an array where the for loop will put the coefficient outputs
# cols = []  # empty array pre-allocated for the columns needed in new dataframe
# for i in range(0, n):
#     p = np.polyfit(x, y, i, rcond=None, full=False, w=None, cov=False)  # multiple and linear polynomial fits
#     print(type(p))
#     empty_array.append(p)
#     cols.append(i)
# coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
# coeffs = pd.DataFrame(empty_array, columns=['0', '1', '2', '3'])  # output the results from for loop into dataframe
# print(coeff)
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
# for j in range(0, len(measurements)):
#     a = measurements[j]  # grab the first item in the set
#     b = stdevs[j]  # grab the uncertainty
#     rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
#     c = a + rand  # add this to the number
#     list1.append(c)
# print(list1)
# for j in range(0, len(measurements)):
#     a = measurements[j]  # grab the first item in the set
#     b = stdevs[j]  # grab the uncertainty
#     rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
#     c = a + rand  # add this to the number
#     list2.append(c)
# print(list2)
# for j in range(0, len(measurements)):
#     a = measurements[j]  # grab the first item in the set
#     b = stdevs[j]  # grab the uncertainty
#     rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
#     c = a + rand  # add this to the number
#     list3.append(c)
# print(list3)
#
# # tack the lists together using vertically stack
# out_arr = np.vstack((list1, list2, list3))
# print(out_arr)
#
# # tack the lists together into a dataframe
# d = [list1, list2, list3]
# df = pd.DataFrame(data=d)  # create a dataframe to make future manipulation of data simpler
# print(df)




""" 
The above seems to work so far, magically...
 """
