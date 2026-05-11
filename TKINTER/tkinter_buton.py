
from tkinter import * 

window = Tk() #initiate the window
#window.geometry('400x400') #set the size of the window
window.title('My First Window') #set the title of the window    

button = Button(window, text = "Click Me") 
                # config button properties
button.config(bg='#34ebba') #set the background color of the button
button.config(fg='#eb3477') #set the foreground color of the button
button.config(font=('Arial', 20, 'bold')) #set the font of the button
button.config(activebackground='#eb3477') #set the background color of the button when it is clicked
button.config(activebackground='#34ebba') #set the background color of the button when it is clicked
image = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded.png") #set the image for the button
button.config(image=image) #place the image in the button
button.config(compound='bottom') #set the position of the image in the button



def button_click():
    print("Button Clicked!")

button.config(command=button_click) #set the command for the button

button.pack() #place the button in the window

window.mainloop() #place the window in the middle of the screen
