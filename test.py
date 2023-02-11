# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from vpython import *
from numpy import random

if __name__ == '__main__':
    # make window larger
    scene.width = 1200
    scene.height = 800

    # make window grabbable
    scene.userzoom = True
    scene.userspin = True


    # create four walls of the room with length 8 and width 8
    wallR = box(pos=vector(8, 0, 0), size=vector(0.2, 16, 16), color=color.blue)
    wallL = box(pos=vector(-8, 0, 0), size=vector(0.2, 16, 16), color=color.blue)
    wallB = box(pos=vector(0, -8, 0), size=vector(16, 0.2, 16), color=color.blue)
    wallT = box(pos=vector(0, 8, 0), size=vector(16, 0.2, 16), color=color.blue)

    # create a floor
    floor = box(pos=vector(0, 0, -8), size=vector(16, 16, 0.2), color=color.blue)


    # create green goal area of size 1.5 x 1.5 x 0.2 in the corner of the room
    goalLocation = vector(7, 7, -8)

    goal = box(pos=goalLocation, size=vector(1.5, 1.5, 0.2), color=color.green)

    # make 10 people with a sphere in put them in an array and spread them randomly in the room and on the floor
    numHumans = 30
    people = []
    for i in range(numHumans):
        people.append(sphere(pos=vector(random.uniform(-7, 7), random.uniform(-7, 7), -8), radius=0.5, color=color.red))
        print(people[i].pos)


    # create timestep and loop over 10 seconds
    dt = 0.01
    totalTime = 10
    velocity = .03


    for t in arange(0, totalTime, dt):
        rate(100)
        # loop over all people
        for i in range(numHumans):
            # implement simple path planning with visibility graph










