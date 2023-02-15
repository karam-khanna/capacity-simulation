# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from vpython import *
from numpy import random

import pyvisgraph as vg


def plot_path(person, pos, obstacles, goalLocation, graph: vg.VisGraph):
    # create curPos in vg
    curPos = vg.Point(pos.x, pos.y)

    # create goalLocation in vg
    goalLocation = vg.Point(goalLocation.x, goalLocation.y, goalLocation.z)

    # graph path for current obstacle
    path = graph.shortest_path(curPos, goalLocation)

    # turn path into array of points with -8 z coordinate
    targetPoints = []
    for point in path:
        targetPoints.append(vector(point.x, point.y, -8))

    # set interimGoals
    person.interimGoals = targetPoints
    return


def make_move(person, people):

    curPos = person.pos

    # get next target in interimGoals
    nextPoint = person.interimGoals[0]

    successRadius = 0.1

    # special case where interim goal is the last one
    if len(person.interimGoals) == 1:
        successRadius = 1


    # check to see if at current point
    if mag(curPos - nextPoint) < successRadius:

        # remove current goal from interimGoals
        person.interimGoals.pop(0)

        # check to see if there are any more goals
        if len(person.interimGoals) == 0:
            person.visible = False

            # remove from people
            people.remove(person)
            return 0,0

    # get next goal in interimGoals
    nextPoint = person.interimGoals[0]

    # get vector to next point
    path = nextPoint - vector(curPos)

    # normalize vector
    path = path / mag(path)

    # multiply by velocity
    path = path

    # detect closest person in front of them
    closestPerson = None
    closestPersonDistance = 10000
    for otherPerson in people:
        if otherPerson != person:
            # get vector to other person
            otherPersonVector = otherPerson.pos - person.pos

            # check to see if person is within cone radius of the path direction
            # get angle between path and otherPersonVector
            angle = degrees(acos(dot(path, otherPersonVector) / (mag(path) * mag(otherPersonVector))))




            # check to see if angle is less than 45 degrees
            if angle < person.coneWidth / 2:
                # set closest person if person is within the cone radius and angle and closer than the current closest person
                if mag(otherPersonVector) < person.coneRadius and mag(otherPersonVector) < closestPersonDistance:
                    closestPerson = otherPerson
                    closestPersonDistance = mag(otherPersonVector)



    # if closest person is none then velocity = base velocity
    if closestPerson is None:
        velocity = person.baseVelocity
    else:
        scaledDistance = closestPersonDistance / person.coneRadius
        velocity = person.baseVelocity * scaledDistance



    # multiply by velocity
    path = path * velocity

    # return x and y from path
    return path.x, path.y



def checkForCollision(person, obstacles, people):
    # check if person collides with any obstacle
    for obstacle in obstacles:
        if person.pos.x + person.size.x / 2 >= obstacle.pos.x - obstacle.size.x / 2 and person.pos.x - person.size.x / 2 <= obstacle.pos.x + obstacle.size.x / 2:
            if person.pos.y + person.size.y / 2 >= obstacle.pos.y - obstacle.size.y / 2 and person.pos.y - person.size.y / 2 <= obstacle.pos.y + obstacle.size.y / 2:
                return True

    # check if person collides with any other person
    for otherPerson in people:
        if person.pos.x + person.size.x / 2 >= otherPerson.pos.x - otherPerson.size.x / 2 and person.pos.x - person.size.x / 2 <= otherPerson.pos.x + otherPerson.size.x / 2:
            if person.pos.y + person.size.y / 2 >= otherPerson.pos.y - otherPerson.size.y / 2 and person.pos.y - person.size.y / 2 <= otherPerson.pos.y + otherPerson.size.y / 2:
                return True

    return False


def run():
    # make 10 people with a sphere in put them in an array and spread them randomly in the room and on the floor
    numHumans = 100
    humanRadius = 0.25
    baseVelocity = 2
    coneWidth = 45
    coneRadius = 1

    # make window larger
    scene.width = 1200
    scene.height = 800

    # make window grabbable
    scene.userzoom = True
    scene.userspin = True

    # create a floor
    floor = box(pos=vector(0, 0, -8.2), size=vector(16, 16, 0.2), color=color.blue)


    # rectangles
    rectangles = []


    # create four walls of the room with length 8 and width 8
    wallR = box(pos=vector(8, 0, 0), size=vector(0.2, 16, 16), color=color.blue)
    wallL = box(pos=vector(-8, 0, 0), size=vector(0.2, 16, 16), color=color.blue)
    wallB = box(pos=vector(0, -8, 0), size=vector(16, 0.2, 16), color=color.blue)
    wallT = box(pos=vector(0, 8, 0), size=vector(16, 0.2, 16), color=color.blue)


    # TODO: standardize size of boxes and make them smaller proportionally to the size of the humans

    barrierDifferencePercentage = 0.65
    barrierOpacity = 0

    obstacle1_barrier = box(pos=vector(1, 2, -8), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
    obstacle1_visible = box(pos=obstacle1_barrier.pos, size=obstacle1_barrier.size * barrierDifferencePercentage, color=color.yellow)
    label(pos=obstacle1_barrier.pos, text="Obstacle 1", xoffset=20, yoffset=20, space=20, height=10, border=4, font='sans')

    obstacle2_barrier = box(pos=vector(4, 5, -8), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
    obstacle2_visible = box(pos=obstacle2_barrier.pos, size=obstacle2_barrier.size * barrierDifferencePercentage, color=color.yellow)
    label(pos=obstacle2_barrier.pos, text="Obstacle 2", xoffset=20, yoffset=20, space=20, height=10, border=4, font='sans')

    obstacle3_barier = box(pos=vector(5, 0, -8), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
    obstacle3_visible = box(pos=obstacle3_barier.pos, size=obstacle3_barier.size * barrierDifferencePercentage, color=color.yellow)
    label(pos=obstacle3_barier.pos, text="Obstacle 3", xoffset=20, yoffset=20, space=20, height=10, border=4, font='sans')

    obstacle4_barrier = box(pos=vector(0, 5.1, -8), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
    obstacle4_visible = box(pos=obstacle4_barrier.pos, size=obstacle4_barrier.size * barrierDifferencePercentage, color=color.yellow)
    label(pos=obstacle4_barrier.pos, text="Obstacle 4", xoffset=20, yoffset=20, space=20, height=10, border=4, font='sans')

    obstacle5_barrier = box(pos=vector(-5, 0, -8), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
    obstacle5_visible = box(pos=obstacle5_barrier.pos, size=obstacle5_barrier.size * barrierDifferencePercentage, color=color.yellow)
    label(pos=obstacle5_barrier.pos, text="Obstacle 5", xoffset=20, yoffset=20, space=20, height=10, border=4, font='sans')


    # add all to rectangles
    rectangles.append(wallR)
    rectangles.append(wallL)
    rectangles.append(wallB)
    rectangles.append(wallT)
    rectangles.append(obstacle1_barrier)
    rectangles.append(obstacle2_barrier)
    rectangles.append(obstacle3_barier)
    rectangles.append(obstacle4_barrier)
    rectangles.append(obstacle5_barrier)

    polys = []
    for obstacle in rectangles:
        # create vg polygons
        obstaclePolygon = [
            # add vertices of rectangle + humanRadius to make sure people don't collide with the walls
            vg.Point(obstacle.pos.x - obstacle.size.x / 2, obstacle.pos.y - obstacle.size.y / 2),
            vg.Point(obstacle.pos.x + obstacle.size.x / 2, obstacle.pos.y - obstacle.size.y / 2),
            vg.Point(obstacle.pos.x + obstacle.size.x / 2, obstacle.pos.y + obstacle.size.y / 2),
            vg.Point(obstacle.pos.x - obstacle.size.x / 2, obstacle.pos.y + obstacle.size.y / 2)

        ]
        polys.append(obstaclePolygon)

    # create graph
    graph = vg.VisGraph()
    graph.build(polys)



    # create green goal area of size 1.5 x 1.5 x 0.2 in the corner of the room
    goalLocation = vector(7, 7, -8)
    goal = box(pos=goalLocation, size=vector(1.5, 1.5, 0.2), color=color.green)

    people = []
    for i in range(numHumans):
        while (True):
            person = sphere(pos=vector(random.uniform(-7, 7), random.uniform(-7, 7), -8), radius=humanRadius, color=color.red)


            if not checkForCollision(person, rectangles, people):
                people.append(person)
                plot_path(person, person.pos, rectangles, goalLocation, graph)
                person.baseVelocity = baseVelocity
                person.velocity = baseVelocity

                # person will set their velocity based on people around them in the shape of a semi-circle in front of them
                # set the cone radius and angle
                person.coneRadius = coneRadius
                person.coneWidth = coneWidth




                break
            else:
                person.visible = False




    # create timestep and loop over 10 seconds
    dt = 0.01
    totalTime = 100
    velocity = .03


    for t in arange(0, totalTime, dt):
        rate(100)
        # loop over all people
        for person in people:
            # move person
            moveX, moveY = make_move(person, people)

            person.pos.x += moveX*dt
            person.pos.y += moveY*dt




if __name__ == '__main__':
    run()









