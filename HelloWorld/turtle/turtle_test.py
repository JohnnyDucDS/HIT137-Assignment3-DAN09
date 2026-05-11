import turtle
t = turtle.Turtle()

#color setting
t.color("blue")



# code run
'''
t.forward(100)

t.left(90)
t.forward(100)

t.left(90)
t.forward(100)

t.left(90)
t.forward(100)

'''

t.begin_fill() #start command for fill color
t.fillcolor("cyan") #color setting for fill color


t.forward(100)
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(90)
t.left(45)
t.forward(141.42 * 2)
t.right(90 + 45)
t.forward(200)
t.right(90 + 45)
t.forward(141.42 * 2)

t.end_fill() #end command for fill color

t.penup() #lift the pen up to move without drawing
# t.goto(0, 0) #move the turtle to the center of the screen
t.color("red") #change the pen color to red
t.left(45)
t.forward(200)


t.pendown() #lower the pen to start drawing

t.color('red', 'yellow') #change the pen color to red, fill color to yellow

t.begin_fill()

t.forward(100)
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(90)
t.forward(200)
t.left(90)
t.left(45)
t.forward(141.42 * 2)
t.right(90 + 45)
t.forward(200)
t.right(90 + 45)
t.forward(141.42 * 2)

t.end_fill()





turtle.done()