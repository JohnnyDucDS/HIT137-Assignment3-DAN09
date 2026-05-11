
from tkinter import *

window = Tk()

window.config(width=1650,
              height=1450)

def display():
    if x.get() == 1 and y.get() == 1:
        print("Both checked")
    elif x.get() == 1 or y.get() == 1:
        print("Checked")
    else:
        print("Unchecked")

x = IntVar()
y = IntVar()
checkbox = Checkbutton(window, text="Hehe", variable=x, onvalue=1, offvalue=0, command=display)
checkbox.config(font=("Arial", 20, "bold"),
                fg="white",
                bg="black",
                padx=10,
                pady=10,
                cursor="hand2",  
                anchor="w"
            )

photo=PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded_resize.png")
checkbox.config(image=photo, compound="left",
                padx=20, pady=20,
               )

#check box 2

checkbox2 = Checkbutton(window, text="Hihi", variable=y, onvalue=1, offvalue=0, command=display)
checkbox2.config(font=("Arial", 20, "bold"),
                fg="white",
                bg="black",
                padx=10,
                pady=10,
                cursor="hand2",
                anchor="w")

photo2=PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/camera_lens_logo_rounded_resize.png")
checkbox2.config(image=photo2, compound="left",
                padx=20, pady=20,
               )
               
checkbox.pack(anchor=W)
checkbox2.pack(anchor=W)




























window.mainloop()
