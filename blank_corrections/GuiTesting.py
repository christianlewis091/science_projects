"""
Commented out on October 10, 2022. The GUI is NOT READY, I repeat NOT READY. The normal python script works fine.

"""

# # https://www.youtube.com/watch?v=YXPyB4XeYLA&t=2640s&ab_channel=freeCodeCamp.org
# from tkinter import *
# from tkinter import ttk
# import pandas as pd
# import numpy as np
# from blank_corr_functions import blank_corr_normal
#
# """
# Last Update: September 7, 2022
# This code is the GUI form of Iteration3.
# In this GUI form, the execute button calls a function in "blank_corr_functions" called "blank_corr_normal" which
# is a literal copy of Iteration3. I only wanted to make a GUI so I can make an executable so someone else can run it.
#
# """
# """
# This block of code below just says hello. It doesn't really do anything.
# """
# root = Tk()
# root['bg'] = 'darkred'
# root.geometry("1400x1000")
# hello_message = Label(root, text="Blank Correction GUI: Last Updated October 11, 2022 (Author: Christian B. Lewis)")
# hello_message.grid(row=0, rowspan=1, column=0, columnspan=5)
#
#
# tw = Label(root, text="Please enter wheel TW #:")
# tw.grid(row=4, column=0)
# entry1 = StringVar()                                # initialize a variable where the input will be stored
# entry1_box = ttk.Entry(root,textvariable = entry1)  # This creates the input box
# entry1_box.grid(row=4, column=1)                    # This tells the input box where to sit.
#
# # If some standards wish to be exluded, I will have a new box pop up where they can be input
# stds_exclude = Label(root, text="Do you want to exclude any standards? (Y/N)")
# stds_exclude.grid(row=6, column=0)
# entry2 = StringVar()                                # initialize a variable where the input will be stored
# entry2_box = ttk.Entry(root,textvariable = entry2)  # This creates the input box
# entry2_box.grid(row=6, column=1)                    # This tells the input box where to sit.
#
#
# duration = Label(root, text="How far back do you want the std's to go? Type 0.5 for 1/2 year, and 1 for 1 year.")
# duration.grid(row=8, column=0)
# entry3 = StringVar()                                # initialize a variable where the input will be stored
# entry3_box = ttk.Entry(root,textvariable = entry3)  # This creates the input box
# entry3_box.grid(row=8, column=1)                    # This tells the input box where to sit.
#
#
# """
# This block of code defines how, when the Submit button is pressed, it executes the code in Iteration3.
# """
#
# def execute():
#     value1 = str(entry1.get())        # this grabs the data in TW entry box when button is pressed
#     value2 = str(entry2.get())    # This grabs that data in Y/N box when the button is pressed
#     value3 = str(entry3.get())  # This grabs the data in Time duration box when button is pressed
#     x = blank_corr_normal(value1, value2, value3)  # This calls the function written in Iteration4 which actually runs the script.
#     print(x)
#
#     end_message = Label(root, text="Done! Please check I:\C14Data\C14_blank_corrections_dev\PythonOutput for your data. ")
#     end_message.grid(row=10, rowspan=1, column=0, columnspan=5)
#
#
# myButton = Button(root, text="Execute MCC Calculation", command=execute, fg='blue')
# myButton.grid(row=9, column=0, columnspan=5)
#
#
#
# root.mainloop()