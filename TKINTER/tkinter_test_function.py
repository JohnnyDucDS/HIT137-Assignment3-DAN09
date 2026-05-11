from tkinter import * 

count = 0 

def click_count():
    global count 
    count += 1 
    label.config(text=count)


window = Tk() #initiate the window
#window.geometry('400x400') #set the size of the window
window.title('My First Window') #set the title of the window    

button = Button(window, text = "Click Me") 
                # config button properties
button.config(bg='#34ebba') #set the background color of the button
button.config(fg='#eb3477') #set the foreground color of the button
button.config(font=('Arial', 20, 'bold')) #set the font of the button
button.config(activebackground="#1119bc") #set the background color of the button when it is clicked
button.config(activebackground='#34ebba') #set the background color of the button when it is clicked
image = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded.png") #set the image for the button
button.config(image=image) #place the image in the button
button.config(compound='bottom') #set the position of the image in the button


label = Label(window, text = " This is a test for the label widget", 
              font = ('Times New Roman', 14), 
              fg='white', 
              bg='black',
              bd =10, #set the border width of the label
              padx = 20, #set the horizontal padding of the label
              pady = 20, #set the vertical padding of the label
              relief = GROOVE,
              image = image,
              compound = 'bottom') #create a label widget

label.pack() #place the label in the window

# set desktop icon when run the program
icon = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded.png") #set the icon of the window 
window.iconphoto(True, icon) #place the icon in the window
window.config(bg='black') #set the background color of the window
window.iconphoto(True, icon) #place the icon in the window

window.mainloop() #place the window in the middle of the screen