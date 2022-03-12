import pandas as pd
import random
import numpy as np
""" 
I want to test the logic of a monte carlo analysis using a simpler set of data. 
I need data, and standard deviations.

I'm going to just work with a simple calculation first - adding the data up. 
 """
# create random measurements and standard deviations to test
measurements = []
for i in range(0, 100):
    measurement = random.uniform(10.5, 75.5)
    measurements.append(measurement)
# print(measurements)

stdevs = []
for i in range(0, 100):
    stdev = random.uniform(0, 1)
    stdevs.append(stdev)
# print(stdevs)

# First step is to get the measurement to randomize within its uncertainty
list1 = []
list2 = []
list3 = []
n = 21
# obj = {}
# for i in range(1, n):
#     obj['l'+str(i)] = []   # use a dictionary to initialize many lists
#
# for item in obj:
#     list1 = []
#     for j in range(0, len(measurements)):
#
#         a = measurements[j]  # grab the first item in the set
#         b = stdevs[j]  # grab the uncertainty
#         rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
#         c = a + rand  # add this to the number
#         list1.append(c)
#     item = list1


for j in range(0, len(measurements)):
    a = measurements[j]  # grab the first item in the set
    b = stdevs[j]  # grab the uncertainty
    rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
    c = a + rand  # add this to the number
    list1.append(c)
print(list1)
for j in range(0, len(measurements)):
    a = measurements[j]  # grab the first item in the set
    b = stdevs[j]  # grab the uncertainty
    rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
    c = a + rand  # add this to the number
    list2.append(c)
print(list2)
for j in range(0, len(measurements)):
    a = measurements[j]  # grab the first item in the set
    b = stdevs[j]  # grab the uncertainty
    rand = random.uniform(b, b * -1)  # create a random uncertainty within the range of the uncertainty
    c = a + rand  # add this to the number
    list3.append(c)
print(list3)

# tack the lists together using vertically stack
out_arr = np.vstack((list1, list2, list3))
print(out_arr)

# tack the lists together into a dataframe
d = [list1, list2, list3]
df = pd.DataFrame(data=d)  # create a dataframe to make future manipulation of data simpler
print(df)










""" 
The above seems to work so far, magically...
 """
