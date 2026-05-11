from turtle import *
space = Screen()
mario = Turtle()

# Background
mario.color("sky blue")
mario.pensize(800)
mario.forward(0)                # Draw a blue dot that covers the screen

# Base - a 200px circle centered at 0, -160
mario.color("white")
mario.penup()                   # Pick up the pen so we don't draw when we goto
mario.goto(0, -160)             # Jump directly to x = 0, y = -160
mario.pendown()
mario.pensize(200)
mario.forward(0)                # Draw a dot at the current pensize

# Body - a 150px circle centered at 0, 0
mario.penup()
mario.goto(0, 0)
mario.pendown()
mario.pensize(150)
mario.forward(0)

# Head - a 100px circle centered at 0, 120
mario.penup()
mario.goto(0, 120)
mario.pendown()
mario.pensize(100)
mario.forward(0)
