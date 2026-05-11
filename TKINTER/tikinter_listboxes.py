   # ___________Functions____________________

# Prints the currently selected menu item when the submit button is clicked
from ast import For


def submit():
    food = []

    for index in listbox.curselection():  # loop through the selected indices in the listbox
         food.insert(index, listbox.get(index))  # get the item at the selected index and add it to the food list

         print("you have ordered: ")
         for index in food:
             print(index)  # print each selected food item  
 
# add function
def add():
    new_item = entry.get()  # get the text from the entry widget
    if new_item:  # check if the entry is not empty
        listbox.insert(END, new_item)  # add the new item to the end of the listbox
        entry.delete(0, END)  # clear the entry widget after adding

# delete function
def delete():
    for index in reversed(listbox.curselection()):
        listbox.delete(index)

# ___________END OF FUNCTIONS____________________

from tkinter import *

# ___________CREATE THE MAIN WINDOW____________________

# Create the main application window
window = Tk()

# Create a listbox to display menu items
listbox = Listbox(window, font=("Aerial", 20),
                  bg= "grey",
                  fg="white", 
                  width=20,
                  selectmode=MULTIPLE)  # allow multiple selection

# menu items to be added to the listbox
listbox.insert(1, "Noodle soup")
listbox.insert(2, "Bun cha")
listbox.insert(3, "Banh mi")
listbox.insert(4, "Spring rolls")
listbox.insert(5, "Vietnamese salad")

# Auto-size the listbox height to fit all items
listbox.config(height=listbox.size())

listbox.pack()

# entry widget for adding new items to the listbox
entry = Entry(window, font=("Aerial", 20), bg="white", fg="black", text="Add new item")
entry.pack()

# ____________BUTONS____________________

# Button that triggers the submit function on click
submit_button = Button(window, text="Submit", command=submit)
submit_button.pack()

# add button
add_button = Button(window, text="Add Item", command=add)
add_button.pack()

#delete button
delete_button = Button(window, text="Delete Item", command=delete)
delete_button.pack()

# ___________END OF BUTTONS____________________

# Start the event loop to keep the window open
 
window.mainloop()


