from turtle import *
from random import randint
def userInput():
    print("do you want to see a spiral or draw?")
    string = input()
    return string

def turtle():
    t = Turtle()
    colormode(255)
    colour1 = randint(0, 255)
    colour2 = randint(0, 255)
    colour3 = randint(0, 255)
    angle = randint(0, 360)

    t.speed(0)
    t.pensize(2)
    for i in range(10000):
        t.forward(i)
        t.left(angle)
        t.pencolor(255 - i % colour1, i % colour2, i % colour3)
    screen = Screen()
    screen.exitonclick()


if __name__ == '__main__':
        turtle()


