from tkinter import * 

count = 0 

def click_count():
    global count 
    count += 1 
    label.config(text=f"Count: {count}")


window = Tk() #initiate the window
#window.geometry('400x400') #set the size of the window
window.title('My First Window') #set the title of the window    

button = Button(window, text = "Click Me") 
                # config button properties
image = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/emergency_button_logo.png") #set the image for the button
button.config(bg='#34ebba',
              fg='#eb3477',
              font=('Arial', 20, 'bold'),
              activebackground="black",
              activeforeground='#34ebba',
              image=image,
              compound='bottom')


label = Label(window, text=count, font=('Arial', 20, 'bold')) #create a label widget to display the count
label.pack() #place the label in the window

button.config(command=click_count) #set the command for the button

button.pack() #place the button in the window

# set desktop icon when run the program
icon = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/emergency_button_logo.png") #set the icon of the window 
window.iconphoto(True, icon) #place the icon in the window
window.config(bg='black') #set the background color of the window
window.iconphoto(True, icon) #place the icon in the window

window.mainloop() #place the window in the middle of the screen
