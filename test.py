# https://www.youtube.com/watch?v=YXPyB4XeYLA&t=2640s&ab_channel=freeCodeCamp.org
from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np

df = pd.read_excel(r'C:\Users\clewis\Desktop\recipebookV4.xlsx')
root = Tk()
names = df.Recipe_Title.unique()
print(names)

e1 = StringVar()
e2 = StringVar()
e3 = StringVar()
e4 = StringVar()
e5 = StringVar()
e6 = StringVar()
e7 = StringVar()
e8 = StringVar()
e9 = StringVar()
e10 = StringVar()
e11 = StringVar()
e12 = StringVar()
e13 = StringVar()
e14 = StringVar()
e15 = StringVar()
e16 = StringVar()
e17 = StringVar()
e18 = StringVar()
e19 = StringVar()
e20 = StringVar()
e21 = StringVar()
e22 = StringVar()
e23 = StringVar()
e24 = StringVar()
e25 = StringVar()
e26 = StringVar()
e27 = StringVar()
e28 = StringVar()

bfast = df.loc[df['Meal'] == 'breakfast']
mid = df.loc[df['Meal'] == 'lunch']
dinn = df.loc[df['Meal'] == 'dinner']
all = ['all']+ list(df.Recipe_Title.unique())  # CREATES THE ITEMS IN DROPDOWN LIST
bfast = ['breakfast recipes'] + list(bfast.Recipe_Title.unique())  # CREATES THE ITEMS IN DROPDOWN LIST
mid = ['lunch recipes'] + list(mid.Recipe_Title.unique())  # CREATES THE ITEMS IN DROPDOWN LIST
dinn = ['dinner recipes'] + list(dinn.Recipe_Title.unique())  # CREATES THE ITEMS IN DROPDOWN LIST

breakfast_column = 1
lunch_column = 2
dinner_column = 3

mon = Label(root, text="M")
tues = Label(root, text="Tu")
wed = Label(root, text="W")
thurs = Label(root, text="Th")
fri = Label(root, text="F")
sat = Label(root, text="Sat")
sun = Label(root, text="Sun")
breakfast = Label(root, text="Breakfast")
lunch = Label(root, text="Lunch")
dinner = Label(root, text="Dinner")
extra = Label(root, text="Else?")
mon.grid(row=1, column=0)
tues.grid(row=2, column=0)
wed.grid(row=3, column=0)
thurs.grid(row=4, column=0)
fri.grid(row=5, column=0)
sat.grid(row=6, column=0)
sun.grid(row=7, column=0)
breakfast.grid(row=0, column=breakfast_column)
lunch.grid(row=0, column=lunch_column)
dinner.grid(row=0, column=dinner_column)
extra.grid(row=0,column=4)

"""
breakfast column  
"""
e1_entry = ttk.OptionMenu(root, e1, *bfast)
e2_entry = ttk.OptionMenu(root, e2, *bfast)
e3_entry = ttk.OptionMenu(root, e3, *bfast)
e4_entry = ttk.OptionMenu(root, e4, *bfast)
e5_entry = ttk.OptionMenu(root, e5, *bfast)
e6_entry = ttk.OptionMenu(root, e6, *bfast)
e7_entry = ttk.OptionMenu(root, e7, *bfast)
e1_entry.grid(row=1, column=breakfast_column)
e2_entry.grid(row=2, column=breakfast_column)
e3_entry.grid(row=3, column=breakfast_column)
e4_entry.grid(row=4, column=breakfast_column)
e5_entry.grid(row=5, column=breakfast_column)
e6_entry.grid(row=6, column=breakfast_column)
e7_entry.grid(row=7, column=breakfast_column)
"""
lunch
"""
e8_entry = ttk.OptionMenu(root, e8, *mid)
e9_entry = ttk.OptionMenu(root, e9, *mid)
e10_entry = ttk.OptionMenu(root, e10, *mid)
e11_entry = ttk.OptionMenu(root, e11, *mid)
e12_entry = ttk.OptionMenu(root, e12, *mid)
e13_entry = ttk.OptionMenu(root, e13, *mid)
e14_entry = ttk.OptionMenu(root, e14, *mid)
e8_entry.grid(row=1, column=lunch_column)
e9_entry.grid(row=2, column=lunch_column)
e10_entry.grid(row=3, column=lunch_column)
e11_entry.grid(row=4, column=lunch_column)
e12_entry.grid(row=5, column=lunch_column)
e13_entry.grid(row=6, column=lunch_column)
e14_entry.grid(row=7, column=lunch_column)
"""
dinner
"""
e15_entry = ttk.OptionMenu(root, e15, *dinn)
e16_entry = ttk.OptionMenu(root, e16, *dinn)
e17_entry = ttk.OptionMenu(root, e17, *dinn)
e18_entry = ttk.OptionMenu(root, e18, *dinn)
e19_entry = ttk.OptionMenu(root, e19, *dinn)
e20_entry = ttk.OptionMenu(root, e20, *dinn)
e21_entry = ttk.OptionMenu(root, e21, *dinn)
e15_entry.grid(row=1, column=dinner_column)
e16_entry.grid(row=2, column=dinner_column)
e17_entry.grid(row=3, column=dinner_column)
e18_entry.grid(row=4, column=dinner_column)
e19_entry.grid(row=5, column=dinner_column)
e20_entry.grid(row=6, column=dinner_column)
e21_entry.grid(row=7, column=dinner_column)

"""
else
"""
e22_entry = ttk.OptionMenu(root, e22, *all)
e23_entry = ttk.OptionMenu(root, e23, *all)
e24_entry = ttk.OptionMenu(root, e24, *all)
e25_entry = ttk.OptionMenu(root, e25, *all)
e26_entry = ttk.OptionMenu(root, e26, *all)
e27_entry = ttk.OptionMenu(root, e27, *all)
e28_entry = ttk.OptionMenu(root, e28, *all)
e22_entry.grid(row=1, column=4)
e23_entry.grid(row=2, column=4)
e24_entry.grid(row=3, column=4)
e25_entry.grid(row=4, column=4)
e26_entry.grid(row=5, column=4)
e27_entry.grid(row=6, column=4)
e28_entry.grid(row=7, column=4)




version_message = Label(root, text="Created by: Dr. Christian B. Lewis, Version 3.0, September 28, 2022")
version_message.grid(row=11, column=0, columnspan=5)
version_message = Label(root, text="For issues reach out to christian.lewis091@gmail.com")
version_message.grid(row=12, column=0, columnspan=5)


def executeList():

    # grab all the variables
    value1 = str(e1.get())
    value2 = str(e2.get())
    value3 = str(e3.get())
    value4 = str(e4.get())
    value5 = str(e5.get())
    value6 = str(e6.get())
    value7 = str(e7.get())
    value8 = str(e8.get())
    value9 = str(e9.get())
    value10 = str(e10.get())
    value11 = str(e11.get())
    value12 = str(e12.get())
    value13 = str(e13.get())
    value14 = str(e14.get())
    value15 = str(e15.get())
    value16 = str(e16.get())
    value17 = str(e17.get())
    value18 = str(e18.get())
    value19 = str(e19.get())
    value20 = str(e20.get())
    value21 = str(e21.get())
    value22 = str(e22.get())
    value23 = str(e23.get())
    value24 = str(e24.get())
    value25 = str(e25.get())
    value26 = str(e26.get())
    value27 = str(e27.get())
    value28 = str(e28.get())

    varlist = [value1, value2, value3, value4, value5, value6, value7,
               value8, value9, value10, value11, value12, value13, value14,
               value15, value16, value17, value18, value19, value20, value21,
               value22, value23, value24, value25, value26, value27, value28]

    x = pd.DataFrame()
    for i in range(0, len(names)):        # for the length of the range of the unique recipe names:
        item = names[i]                   # grab the first recipe of the unique list...
        for j in range(0, len(varlist)):               # now run through the variables (each of the dropdown boxes)
            if varlist[j] == item:                 # if the input is equal to a specific item (if you find a match)
                df_new = df.loc[(df['Recipe_Title'] == item)]  # locate this item from the database,
                x = pd.concat([x, df_new])                     # concat it to our growing database

    x['Duplicate_search'] = x.duplicated(subset='Ingredient', keep=False)  # This function identifies duplicates, by adding a new column and setting all dups to True.
    duplicates = x.loc[(x['Duplicate_search'] == True)]                    # dump all the duplicates into one DataFrame (here, there are still multiples of the same things in the dataframe)
    duplicates_list = np.unique(duplicates['Ingredient'])                  # extract a list of all the duplicate ingredients
    array1 = []
    array2 = []
    array3 = []
    type_new = []
    for i in range(0, len(duplicates_list)):
        current = duplicates_list[i]                                     # focus on the first duplicate of all of the duplicates
        current = duplicates.loc[(duplicates['Ingredient'] == current)]  # extract a quick mini dataFrame of only the current ingredient
        quant = np.sum(current['Quantity'])
        array2.append(quant)
        string1 = ""
        string2 = ""
        for k in range(0, len(current)):
            row = current.iloc[k]  # access the first row of the mini-dataframe for the first duplicate
            string1 = string1 + str(row['Recipe_Title']) + str('_') + str('+') + str('_')  # create a longer string of all the recipes where its used
            string2 = string2 + str(row['Unit_of_Measure']) + str('_') + str('+') + str('_')  # create a longer string of all the recipes where its used
        array1.append(string1)
        array3.append(string2)

        type_new.append(row['Type'])

    cleaned_data = pd.DataFrame(
        {"Recipe_Title": array1, "Ingredient": duplicates_list, "Type": type_new, "Quantity": array2, "Unit_of_Measure": array3})
    # cleaned_data.to_excel('cleaned.xlsx')

    others = x.loc[(x['Duplicate_search'] == False)]  # all the ones where the original dup search was false.
    final_list = pd.concat([cleaned_data, others])
    final_list = final_list[['Ingredient', 'Quantity', 'Unit_of_Measure', 'Type', 'Recipe_Title']]
    final_list = final_list.sort_values(by='Type', ascending=False).reset_index(drop=True)
    final_list.to_excel('listV3_1.xlsx')

    # adding printing of the list functionality
    a = [value1, value2, value3, value4, value5, value6, value7]
    b = [value8, value9, value10, value11, value12, value13, value14]
    c = [value15, value16, value17, value18, value19, value20, value21]
    d = [value22, value23, value24, value25, value26, value27, value28]
    print_post = pd.DataFrame({"Breakfast": a, "Lunch": b, "Dinner": c, "Else": d})
    print_post.to_excel('choicesV3_1.xlsx')


myButton = Button(root, text="Run", command=executeList, fg='blue')
myButton.grid(row=10, column=0, columnspan=7)

summary = 'This app was created by Dr. Christian B Lewis. The current version is 3.0, finalized on September 29, 2022, on a train from Berlin to the Nethlands. ' \
          'Current issues, troubleshooting comments will be listed here. ' \
          'In the future, I want to add the following:' \
          '1. I want to sort the ingredients based on what I can by at Bin Inn, and at the Farmers Market.'

def in_dev():
    top = Toplevel()
    top.geometry('500x500')
    myLabel = Label(top, text=summary, justify=LEFT, wraplength=300).pack()

myButton2 = Button(root, text="See Documentation", command=in_dev, fg='blue')
myButton2.grid(row=13, column=0, columnspan=7)


root.mainloop()

"""
Changes made between version 3 and version 3.1 (this version) is that I want to add the capability
to print the actual choices that you made. Otherwise, the options you selected are turned into a
list but the actual options are lost , which is quite unhelpful.
"""