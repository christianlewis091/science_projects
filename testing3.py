import pandas as pd
import random
import numpy as np


x = [1,2,4,6,7]
y = [1,5,15,5,6]
z = [1,6,9,5,7]

array1 = np.vstack((x,y))
array1 = np.vstack((array1, z))
cols = np.linspace(0, len(array1[1]))
dataf = pd.DataFrame(array1)  # output the results from for loop into dataframe
print(dataf)
element1 = np.sum(dataf[0])
print(element1)

mean_array = []
for i in range(0, len(array1[1])):
    element1 = np.sum(dataf[i])
    element1 = element1 / len(array1)
    mean_array.append(element1)
    print(mean_array)


    # print(df.head(3))

#

#
# #         empty_array.append(p)
# #
# # coeff = pd.DataFrame(empty_array, columns=cols)  # output the results from for loop into dataframe
# # coeffs = pd.DataFrame(empty_array, columns=['0', '1', '2', '3'])  # output the results from for loop into dataframe
# #
# #     # grab the first item
# #     # put it into an array
# cols = []
# test = []
# for i in range(len(array1)):
#     a = array1[i]  # extract the i'th row of the master matrix
#     test = []
#     for j in range(len(array1[1])):
#         b = a[j]       # grab the j'th element of that row
#         test.append(b)  # append that element to a an array
#         cols.append(j)  # associate it with column "j"
#     print(test)
#     # dataf = pd.DataFrame(test, columns=cols)  # output the results from for loop into dataframe
