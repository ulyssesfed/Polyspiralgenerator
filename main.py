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
            "rand": row[5]
        }
        configs.append(config)

    # Close the connection
    cursor.close()
    conn.close()

    return configs

def turtlefunc():
    t = Turtle()
    colormode(255)
    duration = 10
    angle = randint(48, 360)
    t.pensize(randint(1, 4))
    colour1 = randint(0, 255)
    colour2 = randint(0, 255)
    colour3 = randint(0, 255)
    rand = randint(0, 15000)
    pencolor(0,0,0)
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
                rand = config["rand"]
                duration = int(input("how long do you want it to go"))
    else:
        print("No existing configs.")

    start_time = time.time()

    t.speed(0)



    while time.time() - start_time < duration:
        # Calculate the value of i based on the current time
        i = int((time.time() - start_time) * 10) + rand


        j += 1

        t.forward(j)
        t.left(angle)
        t.pencolor(255 - i % colour1, i % colour2, i % colour3)

    record_values = input(
        "Do you want to record the values of angle, pensize, colour1, colour2, and colour3 in a database? (y/n) ")

    if record_values.lower() == "y":
        # Connect to the Access database
        conn = pyodbc.connect(
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\uly\PycharmProjects\turtle\patterns.accdb")
        cursor = conn.cursor()

        # Define the table and field names
        table_name = "patterns"
        field_names = ["angle", "pensize", "colour1", "colour2", "colour3", "rand"]

        # Create the table if it doesn't exist
        try:
            cursor.execute(f"CREATE TABLE {table_name} ({', '.join([f'{name} INTEGER' for name in field_names])})")
        except pyodbc.ProgrammingError:
            pass

        # Insert the values into the table
        values = [angle, t.pensize(), colour1, colour2, colour3, rand]
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
    t.

if __name__ == '__main__':
    while True:
        turtlefunc()
        choice = input("Do you want to run the program again? (y/n) ")
        if choice.lower() != "y":
            break
