# # https://www.youtube.com/watch?v=YXPyB4XeYLA&t=2640s&ab_channel=freeCodeCamp.org
from tkinter import *
from tkinter import ttk
from blank_corr_functions import blank_corr_050223, plot_seconds_thiswheel_new

"""
Update: Febraury 23, 2023
We're ready to implement. I've double checked the code that it works and that I'm happy with it. 
We use the GUI with function "blank_corr_022323"


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
#test
"""
root = Tk()

goldenrat = 1.618
x = 1000
y = int(x / goldenrat)
# root.geometry(f'{x}x{y}+50+50')
# root.configure(bg='brown')

# add hello message at top
hello_message = Label(root, text="Blank Correction GUI: Last Updated 13, April 2023  (Author: Christian B. Lewis)",
                      font=('Helvetica', 13, 'bold'), bd=1, background="brown", foreground="white")
hello_message.grid(row=0, rowspan=1, column=0, columnspan=5)

# add a buffer space
blank_1 = Label(root, text="")
blank_1.grid(row=1, column=0)

hello_message = Label(root, text="Blank Correction", font=('Helvetica', 12, 'bold'), bd=1, background="brown",
                      foreground="white")
hello_message.grid(row=2, column=0, columnspan=5)

blank_1 = Label(root, text="")
blank_1.grid(row=3, column=0)

tw = Label(root, text="Please enter wheel TW #:", font=("Helvetica", 11), bd=1, relief="sunken")
tw.grid(row=4, column=0)
entry1 = StringVar()  # initialize a variable where the input will be stored
entry1_box = ttk.Entry(root, textvariable=entry1)  # This creates the input box
entry1_box.grid(row=4, column=1)  # This tells the input box where to sit.

blank_1 = Label(root, text="")
blank_1.grid(row=5, column=0)

# If some standards wish to be exluded, I will have a new box pop up where they can be input
stds_exclude = Label(root,
                     text="List here any standards you'd like to exclude from blank correction:\n Write without separators (11111 11112 ....)",
                     font=("Helvetica", 11), bd=1, relief="sunken")
stds_exclude.grid(row=6, column=0)
entry2 = StringVar()  # initialize a variable where the input will be stored
entry2_box = ttk.Entry(root, textvariable=entry2)  # This creates the input box
entry2_box.grid(row=6, column=1)  # This tells the input box where to sit.

blank_1 = Label(root, text="")
blank_1.grid(row=7, column=0)

duration = Label(root, text="How far back do you want the std's to go? \n Type 0.5 for 1/2 year, and 1 for 1 year.",
                 font=("Helvetica", 11), bd=1, relief="sunken")
duration.grid(row=8, column=0)
entry3 = StringVar()  # initialize a variable where the input will be stored
entry3_box = ttk.Entry(root, textvariable=entry3)  # This creates the input box
entry3_box.grid(row=8, column=1)  # This tells the input box where to sit.

blank_1 = Label(root, text="")
blank_1.grid(row=9, column=0)

blank_1 = Label(root, text="")
blank_1.grid(row=11, column=0)

hello_message = Label(root, text="Create Data Quality Plots", font=('Helvetica', 12, 'bold'), bd=1, background="brown",
                      foreground="white")
hello_message.grid(row=12, column=0, columnspan=5)

tw_min = Label(root, text="Enter Minimum TW you want (min = 2855)",
                 font=("Helvetica", 11), bd=1, relief="sunken")

tw_min.grid(row=13, column=0)
entry_x = StringVar()  # initialize a variable where the input will be stored
entryx_box = ttk.Entry(root, textvariable=entry_x)  # This creates the input box
entryx_box.grid(row=13, column=1)  # This tells the input box where to sit.


"""
This block of code defines how, when the Submit button is pressed, it executes the code in Iteration3.
"""


def execute():
    value1 = str(entry1.get())  # this grabs the data in TW entry box when button is pressed
    value2 = str(entry2.get())  # List of TP #'s to exclude from standards used.
    value3 = str(entry3.get())  # This grabs the data in Time duration box when button is pressed
    # next two lines deal with formatting stds we want to exclude
    value2 = value2.split()  # This line takes the input from the "Standards you don't want" box and splits it into a list, but a string-list
    value2 = list(value2)  # this takes it from a string list to a list

    x = blank_corr_050223(value1, value3,
                          value2)  # This calls the function written in Iteration4 which actually runs the script.


    end_message = Label(root,
                        text="Output data created for RLIMS Import! \nPlease check I:\C14Data\C14_blank_corrections_dev\PythonOutput for your data. ",
                        anchor="e", justify=LEFT)
    end_message.grid(row=16, rowspan=1, column=0, columnspan=5)


def makesomeplots():
    value1 = str(entry1.get())
    value_x = str(entry_x.get())  # This grabs the data in Time duration box when button is pressed
    x2 = plot_seconds_thiswheel_new(value1, value_x)
    end_message2 = Label(root, text="Plots have been written and saved to \n I:\C14Data\C14_blank_corrections_dev\Quality_Assurance_Plots folder ",anchor="e", justify=LEFT)
    end_message2.grid(row=18, rowspan=1, column=0, columnspan=5)


myButton = Button(root, text="Execute MCC Calculation", command=execute, fg='blue')
myButton.grid(row=10, column=0, columnspan=5)

# blank_1 = Label(root, text="")
# blank_1.grid(row=13, column=0)

blank_1 = Label(root, text="")
blank_1.grid(row=15, column=0)

blank_1 = Label(root, text="")
blank_1.grid(row=17, column=0)

myButton2 = Button(root, text="Create Data Quality Plots and Summary Data from Selected TW #", command=makesomeplots, fg='blue')
myButton2.grid(row=14, column=0, columnspan=5)

blank_1 = Label(root, text="")
blank_1.grid(row=18, column=0)


root.mainloop()
