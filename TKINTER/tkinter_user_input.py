from tkinter import * 

window = Tk() #initiate the window

# set suubmit function
def submit():
    username = entry.get()
    print(username)
submit = Button(window, text="Submit", command=submit) #create a submit button
submit.pack(side = BOTTOM ) #place the submit button in the window

#set delete function
def delete():
    entry.delete(0, END) #delete the input in the entry widget  

delete = Button(window, text="Delete", command=delete) #create a delete button
delete.pack(side = BOTTOM ) #place the delete button in the window 

#set backspace function
def backspace():
    entry.delete((len(entry.get()) - 1), END) #delete the input in the entry widget  

backspace = Button(window, text="Backspace", command=backspace) #create a backspace button
backspace.pack(side = BOTTOM ) #place the backspace button in the window

entry = Entry()
entry.config(font=('Arial', 15, 'bold'), 
             bg="black",
             fg="white",
             width=20) #set the font of the entry widget

entry.config(show="*") #set the show property of the entry widget to hide the input

entry.pack()






























window.mainloop() #place the window in the middle of the screen