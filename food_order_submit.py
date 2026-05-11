from tkinter import *

food = ["Pizza", "Burger", "Hot Dog"]
prices = [10, 15, 20]

window = Tk()
window.title('FOOD MENU ORDER')

pizzaimage = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/pizza.png")
burgerimage = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/burger.png")
hotdogimage = PhotoImage(file="/Users/thienton/Documents/Python/TKINTER/hotdog.png")

foodimages = [pizzaimage, burgerimage, hotdogimage]

x = IntVar()
y = IntVar()
z = IntVar()

selections = [x, y, z]

button1 = Checkbutton(window,
                      text=food[0],
                      variable=x,
                      padx=20,
                      pady=20,
                      font="Arial, 20",
                      image=foodimages[0],
                      compound="left",
                      indicatoron=0,
                      width=300,
                      fg="black",
                      bg='grey',
                      activebackground="black",
                      selectcolor="blue")
button1.pack(anchor=W)

button2 = Checkbutton(window,
                      text=food[1],
                      variable=y,
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
                      selectcolor="blue")
button2.pack(anchor=W)

button3 = Checkbutton(window,
                      text=food[2],
                      variable=z,
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
                      selectcolor="blue")
button3.pack(anchor=W)

result_label = Label(window, text="", font="Arial 16", pady=10)
result_label.pack()

def submit():
    total_items = sum(var.get() for var in selections)
    total_price = sum(prices[i] for i, var in enumerate(selections) if var.get())

    if total_items == 0:
        result_label.config(text="Please select at least one item.")
    else:
        selected = [food[i] for i, var in enumerate(selections) if var.get()]
        result_label.config(
            text=f"Items: {', '.join(selected)}\nTotal items: {total_items}  |  Total price: ${total_price}"
        )

submit_btn = Button(window,
                    text="Submit",
                    font="Arial 16 bold",
                    bg="green",
                    fg="white",
                    padx=20,
                    pady=10,
                    command=submit)
submit_btn.pack(pady=10)

window.mainloop()
