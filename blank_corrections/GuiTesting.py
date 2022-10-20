
# # https://www.youtube.com/watch?v=YXPyB4XeYLA&t=2640s&ab_channel=freeCodeCamp.org
from tkinter import *
from tkinter import ttk
from blank_corr_functions import blank_corr_101922

"""
Update: October 19, 2022
I've begun building the second iteration of the blank correction code. 
This next iteration of the blank correction function was initiated after a conversation with Margaret, Cathy, and Jenny, 
as well as after TW3435 to resolve multiple issues with the initial script. 
1. We really need to deal directly with the pretreatment Process list, rather than assuming the same pretreatment 
for any given material, because for example, Wood treated with AAA and not cellulose is prone to manual error, which 
this entire excercise is meant to avoid. 
2. It would be helpful for Jenny Cathy and Margaret if the blanks that were used were deposited into the Blank Values 
Used Table, so it looks like it always did before. 
3. I need to slightly reformat the .txt file writing to suit what Jenny and Cathy look for, which is a more itemized list
of certain types of metadata (see binder)

Update: October 17, 2022
Blank_corr_101322 has been updated to also EXCLUDE anything with category Background Inorganic, Background Organic, and Background Air. 
Blank_corr_101322 has been updated to have MCC error as 45% of MCC value.
Blank_corr_101322 has been updated to have OXALICS MCC set to 0.
Blank_corr_101322 has been updated to INCLUDE ANU sucrose.

Update: October 13, 2022
It seems I can't turn the script "BlankCorrection_101022.py" into an exe file without actully wrapping it up into
a GUI. That's fine I can do that here. Will try that today. 

Update: September 7, 2022
This code is the GUI form of Iteration3.
In this GUI form, the execute button calls a function in "blank_corr_functions" called "blank_corr_normal" which
is a literal copy of Iteration3. I only wanted to make a GUI so I can make an executable so someone else can run it.

"""
root = Tk()

hello_message = Label(root, text="Blank Correction GUI: Last Updated October 13, 2022 (Author: Christian B. Lewis)")
hello_message.grid(row=0, rowspan=1, column=0, columnspan=5)


tw = Label(root, text="Please enter wheel TW #:")
tw.grid(row=4, column=0)
entry1 = StringVar()                                # initialize a variable where the input will be stored
entry1_box = ttk.Entry(root,textvariable = entry1)  # This creates the input box
entry1_box.grid(row=4, column=1)                    # This tells the input box where to sit.

# If some standards wish to be exluded, I will have a new box pop up where they can be input
stds_exclude = Label(root, text="List here any standards you'd like to exclude from blank correction:")
stds_exclude.grid(row=6, column=0)
entry2 = StringVar()                                  # initialize a variable where the input will be stored
entry2_box = ttk.Entry(root,textvariable = entry2)  # This creates the input box
entry2_box.grid(row=6, column=1)                    # This tells the input box where to sit.

duration = Label(root, text="How far back do you want the std's to go? Type 0.5 for 1/2 year, and 1 for 1 year.")
duration.grid(row=8, column=0)
entry3 = StringVar()                                # initialize a variable where the input will be stored
entry3_box = ttk.Entry(root,textvariable = entry3)  # This creates the input box
entry3_box.grid(row=8, column=1)                    # This tells the input box where to sit.

"""
This block of code defines how, when the Submit button is pressed, it executes the code in Iteration3.
"""

def execute():
    value1 = str(entry1.get())    # this grabs the data in TW entry box when button is pressed
    value2 = str(entry2.get())    # List of TP #'s to exclude from standards used.
    value3 = str(entry3.get())    # This grabs the data in Time duration box when button is pressed

    value2 = value2.split()  # This line takes the input from the "Standards you don't want" box and splits it into a list, but a string-list
    value2 = list(value2)   # this takes it from a string list to a list

    x = blank_corr_101922(value1, value3, value2)  # This calls the function written in Iteration4 which actually runs the script.
    print(x)

    end_message = Label(root, text="Done! Please check I:\C14Data\C14_blank_corrections_dev\PythonOutput for your data. ")
    end_message.grid(row=14, rowspan=1, column=0, columnspan=5)


myButton = Button(root, text="Execute MCC Calculation", command=execute, fg='blue')
myButton.grid(row=12, column=0, columnspan=5)



root.mainloop()