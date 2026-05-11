
from tkinter import * 

window = Tk() #initiate the window
#window.geometry('400x400') #set the size of the window
window.title('My First Window') #set the title of the window    

photo = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded.png") #set the icon of the window
label = Label(window, text = " This is a test for the label widget", 
              font = ('Times New Roman', 14), 
              fg='white', 
              bg='black',
              bd =10, #set the border width of the label
              padx = 20, #set the horizontal padding of the label
              pady = 20, #set the vertical padding of the label
              relief = GROOVE,
              image = photo,
              compound = 'bottom') #create a label widget

label.pack() #place the label in the window




icon = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded.png") #set the icon of the window 
window.iconphoto(True, icon) #place the icon in the window
window.config(bg='black') #set the background color of the window
window.iconphoto(True, icon) #place the icon in the window














window.mainloop() #place the window in the middle of the screen
