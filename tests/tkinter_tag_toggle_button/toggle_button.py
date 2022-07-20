# Import Module
from tkinter import *
 
# Create Object
root = Tk()
 
# Add Title
root.title('On/Off Switch!')
 
# Add Geometry
root.geometry("500x300")
 
# Keep track of the button state on/off
#global is_on
is_on = {"myTag":False,"myTag2":False,"myTag3":False}
 
# Create Label
 
# Define our switch function
def switch(key, buttons, index, is_on):
    button = buttons[index]
    if is_on[key]:
        button.config(text=key ,bg = "grey",fg="black")
        is_on[key] = False
    else:
        button.config(text = key,bg = "green",fg="white")
        is_on[key] = True
 
# Define Our Images
# on = PhotoImage(file = "on.png")
# off = PhotoImage(file = "off.png")
 
# Create A Button

on_buttons = []
mfunctions = []

# for j in range(n):
#     e = Button(my_w, text=j) 
#     e.grid(row=i, column=j) 
def getSwitchLambda(text, on_buttons, index, is_on):
    return lambda:switch(text, on_buttons, index, is_on)

for index, text in enumerate(is_on.keys()):
    # print("TEXT:", text)
    on_buttons.append(Button(root, text=text, bd = 0,bg="grey",fg="black"))
    mfunctions.append(getSwitchLambda(text, on_buttons, index, is_on))
    on_buttons[index].config(command=mfunctions[index])
    on_buttons[index].grid(row=1, column=0+index)
 
# for x in mfunctions: x()

# def getLambda(x): return lambda:print(x)
# # great. much fucking better.
# for y in [getLambda(x) for x in range(3)]: y()

# so that is what's weird about the freaking lambda!

# on_button1 = Button(root, text="myTag2", bd = 0,bg="grey",fg="black")
# # on_button1.command = lambda:switch(key="myTag", button=on_button1)
# on_button1.config(command=lambda:switch(key="myTag2", button=on_button1))

# on_button1.pack(pady = 50)
# Execute Tkinter
root.mainloop()

# so we would also like to use shotcut to manually cut videos and feed that info into the main production logic, by means of mlt xml.