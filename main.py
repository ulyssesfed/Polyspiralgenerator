import colorsys
import turtle

import pyodbc
from turtle import *
from random import randint
import time


def get_configs():
    # Connect to the Access database
    conn = pyodbc.connect(
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\uly\PycharmProjects\turtle\patterns.accdb")
    cursor = conn.cursor()

    # Define the table name
    table_name = "patterns"

    # Retrieve the configs from the database
    configs = []
    for row in cursor.execute(f"SELECT * FROM {table_name}"):
        config = {
            "angle": row[0],
            "pensize": row[1],
            "colour1": row[2],
            "colour2": row[3],
            "colour3": row[4],
            "colour12": row[6],
            "colour22": row[7],
            "colour32": row[8],
            "rand": row[5],
            "descriptions": row[9]
        }
        configs.append(config)

    # Close the connection
    cursor.close()
    conn.close()

    return configs


def turtlefunc():
    t = Turtle()
    t.clear()
    t.penup()
    t.goto(0, 0)
    t.pendown()
    colormode(255)
    duration = 10
    angle = randint(48, 360)
    t.pensize(randint(2, 4))
    colour1 = randint(0, 255)
    colour2 = randint(0, 255)
    colour3 = randint(0, 255)
    colour12 = randint(0, 255)
    colour22 = randint(0, 255)
    colour32 = randint(0, 255)
    rand = 1300
    pencolor(0, 0, 0)
    j = 0

    configs = get_configs()

    if configs:
        print("Existing configs:")
        for i, config in enumerate(configs):
            print(f"{i + 1}. {config}")
        choice = input("Enter the number of the config to load, or press enter to create a new one: ")
        if choice:
            choice = int(choice) - 1
            if 0 <= choice < len(configs):
                config = configs[choice]
                angle = config["angle"]
                t.pensize(config["pensize"])
                colour1 = config["colour1"]
                colour2 = config["colour2"]
                colour3 = config["colour3"]
                colour12 = config["colour12"]
                colour22 = config["colour22"]
                colour32 = config["colour32"]
                rand = config["rand"]
                duration = int(input("how long do you want it to go"))
    else:
        print("No existing configs.")

    start_time = time.time()

    t.speed(0)

    start_color = (colour1, colour2, colour3)
    end_color = (colour12, colour22, colour32)

    rainbowMode = input("Do you want to use rainbow mode? (y/n) ")

    if rainbowMode.lower() == "n":

        gradient_cycles = int(duration / 10)  # number of times to repeat the gradient
        cycle_duration = duration / gradient_cycles  # duration for each cycle
        start_time = time.time()  # reset the start time for each cycle

        for cycle in range(gradient_cycles):
            cycle_start_time = time.time()  # start time for this cycle

            while time.time() - cycle_start_time < cycle_duration:
                # Calculate the value of i based on the current time and the cycle duration
                i = (time.time() - cycle_start_time) / cycle_duration

                j += 1

                # Interpolate between the start and end colors based on i
                r = int(start_color[0] * (1 - i) + end_color[0] * i)
                g = int(start_color[1] * (1 - i) + end_color[1] * i)
                b = int(start_color[2] * (1 - i) + end_color[2] * i)

                t.forward(j)
                t.left(angle)
                t.pencolor(r, g, b)

            # Update the start time for the next cycle
            start_time += cycle_duration
        t.hideturtle()


    else:
        print("Rainbow mode activated.")
        while time.time() - start_time < duration:
            # Calculate the value of i based on the current time
            i = (time.time() - start_time) / duration

            j += 1

            # Generate a smooth gradient between the start and end colors
            r, g, b = [int(x * 255) for x in colorsys.hsv_to_rgb(i, 1, 1)]

            t.forward(j)
            t.left(angle)
            t.pencolor(r, g, b)
        t.hideturtle()


    record_values = input(
        "Do you want to record the values of angle, pensize, colour1, colour2, and colour3 in a database? (y/n) ")

    if record_values.lower() == "y":

        descriptions = input("Enter a description for the config: ")
        # Connect to the Access database
        conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\uly\PycharmProjects\turtle\patterns.accdb")
        cursor = conn.cursor()

        # Define the table and field names
        table_name = "patterns"
        field_names = ["angle", "pensize", "colour1", "colour2", "colour3", "colour12", "colour22", "colour32", "rand", "descriptions"]

        # Create the table if it doesn't exist
        try:
            cursor.execute(f"CREATE TABLE {table_name} ({', '.join([f'{name} INTEGER' for name in field_names])})")
        except pyodbc.ProgrammingError:
            pass

        # Insert the values into the table
        values = [angle, t.pensize(), colour1, colour2, colour3, colour12, colour22, colour32, rand, descriptions]
        cursor.execute(
            f"INSERT INTO {table_name} ({', '.join(field_names)}) VALUES ({', '.join(['?' for i in range(len(values))])})",
            values)
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        print("Values recorded in database.")


    else:
        print("Values not recorded.")


    screen = Screen()
    screen.bye()

if __name__ == '__main__':
    turtlefunc()