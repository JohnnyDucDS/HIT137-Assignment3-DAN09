from cProfile import label
from tkinter import *

food = ["Pizza", "Burger", "Hot Dog"]  # list of food options
prices = ['$10', '$15', '$20']          # corresponding prices

window = Tk()                           # create the main application window
window.title('FOOD MENU ORDER')         # set the window title

# load images for each food item
pizzaimage = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/pizza.png")
burgerimage = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/burger.png")
hotdogimage = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/hotdog.png")

foodimages = [pizzaimage, burgerimage, hotdogimage]  # group images into a list

# shared variable — all radio buttons update this when clicked; -1 means nothing selected yet
selection = IntVar(value=-1)
x = IntVar()  # this variable is not used in the provided code, but may be intended for tracking selections
y = IntVar()  # this variable is not used in the provided code, but may be intended for tracking selections
z = IntVar()  # this variable is not used in the provided code, but may be intended for tracking selections

count = 0  # initialize count of orders

def order():
    if selection.get() == 0:
        print("You ordered Pizza")
    elif selection.get() == 1:
        print("You ordered Burger")
    elif selection.get() == 2:
        print("You ordered Hot Dog")
    else:
        print("Please select a food")

    
# radio button for Pizza
button1 = Radiobutton(window,
                      text=food[0],          # label shown on the button
                      value=0,               # value written to `selection` when clicked
                      variable=selection,    # shared IntVar that tracks the active choice
                      padx=20,              # horizontal inner padding
                      pady=20,              # vertical inner padding
                      font="Arial, 20",
                      image=foodimages[0],   # display the pizza image
                      compound="left",       # place image to the left of the text
                      indicatoron=0,         # hide the circle indicator; button acts as a toggle
                      width=300,
                      fg="black",
                      bg='grey',
                      activebackground="black",
                      command=order)         # call order() whenever this button is clicked
button1.pack(anchor=W)                       # align button to the left

# radio button for Burger
button2 = Radiobutton(window,
                      text=food[1],
                      value=1,
                      variable=selection,
                      padx=20,
                      pady=20,
                      font="Arial, 20",
                      image=foodimages[1],
                      compound="left",
                      indicatoron=0,
                      width=300,
                      fg="black",
                      bg='grey',
                      activebackground="black",
                      command=order)
button2.pack(anchor=W)

# radio button for Hot Dog
button3 = Radiobutton(window,
                      text=food[2],
                      value=2,
                      variable=selection,
                      padx=20,
                      pady=20,
                      font="Arial, 20",
                      image=foodimages[2],
                      compound="left",
                      indicatoron=0,
                      width=300,
                      fg="black",
                      bg='grey',
                      activebackground="black",
                      command=order)
button3.pack(anchor=W)



window.mainloop()   # start the event loop — keeps the window open and responsive
