from tkinter import *

food = ["Pizza", "Burger", "Hot Dog"]
prices = ['$10', '$15', '$20']
total = 0 



window = Tk()

window.title('FOOD MENU ORDER') #set the title of the window

pizzaimage=PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/pizza.png")
burgerimage=PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/burger.png")
hotdogimage=PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/hotdog.png")

foodimages = [pizzaimage, burgerimage, hotdogimage]
x = IntVar()

def order():
    if x.get() == 0:
        print("You ordered Pizza")
    elif x.get() == 1: 
        print("You ordered Burger")
    elif x.get() == 2:
        print("You ordered Hot Dog")
    else:
        print("Please select a food")

total = 0

def calculate_total():
  
    global total
    if x.get() == 0:
        total += 10
    elif x.get() == 1:
        total += 15
    elif x.get() == 2:
        total += 20
   
    print(f"Total: ${total}")


for index in range(len(food)):
    radio_button = Radiobutton(window, 
                               text=food[index], #add text to radio button
                               value=index, #group radio button together if they share the same varible 
                               variable=x,
                               padx=20,
                               pady=20,
                               font="Arial, 20",
                               image = foodimages[index],
                               compound= "left",
                               indicatoron=0, #eliminate the circle indicator 
                               width=300,
                               fg="black",
                               bg='grey',
                               activebackground="black")
    radio_button.config(command=order)
    radio_button.pack(anchor=W)



button = Button(window, text="Calculate Total", font="Arial, 20", command=calculate_total)
button.pack()


    
def delete():
    Entry.delete(0, END) #delete the input in the entry widget  
delete = Button(window, text="Delete", command=delete) #create a delete button
delete.pack(side = BOTTOM ) #place the delete button in the window 
button.pack(side = BOTTOM ) #place the button in the window

window.mainloop()