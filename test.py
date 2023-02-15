from vpython import *
import random

# take inputs from the user
num_balls = int(input("Enter the number of balls: "))
square_x = float(input("Enter the length of the square on the X axis: "))
square_y = float(input("Enter the length of the square on the Y axis: "))

# create the square
scene = canvas(title='Project 1 simulation', width=800, height=800)
wall_left = box(pos=vector(-square_x/2, 0, 0), size=vector(0.1, square_y, square_y), color=color.white)
wall_right = box(pos=vector(square_x/2, 0, 0), size=vector(0.1, square_y, square_y), color=color.white)
wall_top = box(pos=vector(0, square_y/2, 0), size=vector(square_x, 0.1, square_y), color=color.white)
wall_bottom = box(pos=vector(0, -square_y/2, 0), size=vector(square_x, 0.1, square_y), color=color.white)

# create the door
door = box(pos=vector(square_x/2, 0, 0), size=vector(0.1, square_y/3, square_y/3), color=color.green)

# create the balls
balls = []
for i in range(num_balls):
    ball = sphere(pos=vector(random.uniform(-square_x/2, square_x/2), random.uniform(-square_y/2, square_y/2), 0), radius=0.5, color=color.red)
    balls.append(ball)





# define the movement of the balls
def move_balls():
    t = 0
    while True:
        # update timer
        print(t)



        rate(100)
        t += 0.01
        for ball in balls:
            ball.pos += vector(square_x/num_balls, 0, 0) * (door.pos - ball.pos).norm() * 0.1
            for other_ball in balls:
                if ball != other_ball and mag(ball.pos - other_ball.pos) <= ball.radius + other_ball.radius:
                    ball.pos -= vector(square_x/num_balls, 0, 0) * (door.pos - ball.pos).norm() * 0.1
                    break
            if mag(ball.pos - door.pos) <= ball.radius:
                print("people reached the door in", t, "seconds")
                ball.visible = False

# start the movement of the balls
move_balls()