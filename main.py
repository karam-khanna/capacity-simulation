# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

from vpython import *
from numpy import random

import pyvisgraph as vg



# create class called capacity_simulation
class sim:

    class room:
        basic = 0
        classroom = 1
        meetingRoom = 2
        jonesRoom = 3


    numHumans = 60
    humanRadius = .6
    baseVelocity = 3
    minSpeedCoefficient = 0.4
    coneWidth = 170
    coneRadius = 1
    showLabels = False


    roomName = room.classroom







    def plot_path(person, pos, obstacles, goalLocation, graph: vg.VisGraph):
        # create curPos in vg
        curPos = vg.Point(person.pos.x, person.pos.y)

        # create goalLocation in vg
        goalLocation = vg.Point(goalLocation.x, goalLocation.y, goalLocation.z)

        # graph path for current obstacle
        path = graph.shortest_path(curPos, goalLocation)

        # turn path into array of points with -8 z coordinate
        targetPoints = []
        for point in path:
            targetPoints.append(vector(point.x, point.y, sim.humanRadius))

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
            successRadius = successRadius*4


        # check to see if at current point
        if mag(curPos - nextPoint) < successRadius:

            # remove current goal from interimGoals
            person.interimGoals.pop(0)

            # check to see if there are any more goals
            if len(person.interimGoals) == 0:
                person.visible = False

                # remove from people
                people.remove(person)
                return 0, 0

        # get next goal in interimGoals
        nextPoint = person.interimGoals[0]



        # get vector to next point
        path = nextPoint - vector(curPos)



        # normalize vector
        path = path / mag(path)


        # detect closest person in front of them
        closestPerson = None
        closestPersonDistance = 10000
        for otherPerson in people:
            if otherPerson != person:
                # get vector to other person
                otherPersonVector = otherPerson.pos - person.pos

                # check to see if person is within cone radius of the path direction
                # get angle between path and otherPersonVector

                try:
                    angle = degrees(acos(dot(path, otherPersonVector) / (max(mag(path), .1) * max(mag(otherPersonVector), .1) ) ) )

                    # checking if in collision cone
                    if angle < sim.coneWidth / 2:
                        # set closest person if person is within the cone radius and angle and closer than the current closest person
                        if mag(otherPersonVector) < sim.coneRadius and mag(otherPersonVector) < closestPersonDistance:
                            closestPerson = otherPerson
                            closestPersonDistance = mag(otherPersonVector)

                        # if moving with cause collision then set path to 0
                        if mag(otherPersonVector)  < sim.humanRadius * 2 and mag(nextPoint-curPos) > successRadius*4:
                            if person.waitCount < sim.waitCount
                                print("got here 1")
                                person.waitCount += 1
                                # person will not move this iteration
                                path = vector(0, 0, 0)
                                continue
                            else:
                                person.waitCount = -sim.waitCount
                                continue



                    # if person is roughly orthogonal to path also don't go
                    if angle < 85 and angle > 95:
                        # check if other person is closer to goal
                        if mag(nextPoint - otherPerson.pos) < mag(nextPoint - person.pos):
                            if person.waitCount < sim.waitCount:
                                print("got here 2")
                                person.waitCount += 1
                                path = vector(0, 0, 0)
                                continue
                            else:
                                person.waitCount = -sim.waitCount


                            # person will not move this iteration
                except:
                    print("Math domain error")
                    continue


        # if closest person is none then velocity = base velocity
        if closestPerson is None:
            velocity = person.baseVelocity
        else:
            scaledDistance = max(sim.minSpeedCoefficient, 0.5 - closestPersonDistance / sim.coneRadius)
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


    def build(self):
        # make window larger
        scene.width = 1200
        scene.height = 800

        # make window grabbable
        scene.userzoom = True
        scene.userspin = True


        if sim.roomName == sim.room.basic:


            # create a floor
            floor = box(pos=vector(0, 0, -1), size=vector(16, 16, 2), texture=textures.rug
)

            # rectangles
            rectangles = []

            # create four walls of the room with length 8 and width 8
            wallR = box(pos=vector(8, 0, 1), size=vector(0.2, 16, 2), texture=textures.wood)
            wallL = box(pos=vector(-8, 0, 1), size=vector(0.2, 16, 2), texture=textures.wood)
            wallB = box(pos=vector(0, -8, 1), size=vector(16, 0.2, 2), texture=textures.wood)
            wallT = box(pos=vector(0, 8, 1), size=vector(16, 0.2, 2), texture=textures.wood)

            roomCoordinates= {"xmax":8, "xmin":-8, "ymax":8, "ymin":-8}



            barrierDifferencePercentage = 0.65
            barrierOpacity = 0

            obstacle1_barrier = box(pos=vector(1, 2, 1), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
            obstacle1_visible = box(pos=obstacle1_barrier.pos, size=obstacle1_barrier.size * barrierDifferencePercentage,
                                     texture=textures.granite)

            # add fire texture to obstacle1_barrier


            label(pos=obstacle1_barrier.pos, text="Obstacle 1", xoffset=20, yoffset=20, space=20, height=10, border=4,
                  font='sans', visible=sim.showLabels)

            obstacle2_barrier = box(pos=vector(4, 5, 1), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
            obstacle2_visible = box(pos=obstacle2_barrier.pos, size=obstacle2_barrier.size * barrierDifferencePercentage,
                                    texture=textures.granite)
            label(pos=obstacle2_barrier.pos, text="Obstacle 2", xoffset=20, yoffset=20, space=20, height=10, border=4,
                  font='sans', visible=sim.showLabels)

            obstacle3_barier = box(pos=vector(5, 0, 1), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
            obstacle3_visible = box(pos=obstacle3_barier.pos, size=obstacle3_barier.size * barrierDifferencePercentage,
                                    texture=textures.granite)
            label(pos=obstacle3_barier.pos, text="Obstacle 3", xoffset=20, yoffset=20, space=20, height=10, border=4,
                  font='sans', visible=sim.showLabels)

            obstacle4_barrier = box(pos=vector(0, 5.1, 1), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
            obstacle4_visible = box(pos=obstacle4_barrier.pos, size=obstacle4_barrier.size * barrierDifferencePercentage,
                                    texture=textures.granite)
            label(pos=obstacle4_barrier.pos, text="Obstacle 4", xoffset=20, yoffset=20, space=20, height=10, border=4,
                  font='sans', visible=sim.showLabels)

            obstacle5_barrier = box(pos=vector(-5, 0, 1), size=vector(2, 2, 2), color=color.red, opacity=barrierOpacity)
            obstacle5_visible = box(pos=obstacle5_barrier.pos, size=obstacle5_barrier.size * barrierDifferencePercentage,
                                    texture=textures.granite)
            label(pos=obstacle5_barrier.pos, text="Obstacle 5", xoffset=20, yoffset=20, space=20, height=10, border=4,
                  font='sans', visible=sim.showLabels)

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

            goalLocation = vector(7, 7, sim.humanRadius)
            goal = box(pos=goalLocation, size=vector(1.5, 1.5, 2), color=color.green)



        if sim.roomName == sim.room.meetingRoom:
            floor = box(pos=vector(0, 0, -1), size=vector(15, 8.5, 2), texture=textures.rug)


            rectangles = []
            # create four walls of the room with length 8 and width 8
            wallR = box(pos=vector(7.5, 0, 0.5), size=vector(0.2, 8.25, 1), texture=textures.stucco)
            wallL = box(pos=vector(-7.5, 0, 0.5), size=vector(0.2, 8.25, 1), texture=textures.stucco)
            wallB = box(pos=vector(0, -4.25, 0.5), size=vector(15, 0.2, 1), texture=textures.stucco)
            wallT = box(pos=vector(0, 4.25, 0.5), size=vector(15, 0.2, 1), texture=textures.stucco)

            roomCoordinates= {"xmax":7.5, "xmin":-7.5, "ymax":4.25, "ymin":-4.25}



            table = box(pos=vector(0, 0, 0.5), size=vector(8, 3, 1), texture=textures.metal)
            table_barrier = box(pos=table.pos, size=vector(table.size.x + sim.humanRadius*4, table.size.y + sim.humanRadius*4, table.size.z), color=color.purple, opacity=0)
            label(pos=table.pos, text="Table", xoffset=5, yoffset=5, space=10, height=5, border=4, font='sans', visible=sim.showLabels)

            # append table barrier ot rectangles
            rectangles.append(table_barrier)



            # create green goal area of size 1.5 x 1.5 x 0.2 in the corner of the room
            goalLocation = vector(-5.5, 3.5, 0)
            goal = box(pos=goalLocation, size=vector(3, 0.5, 0.2), color=color.green)
            # create door on top of goal location
            # add image that looks like door on door
            doorImage = box(pos=vector(-5.5, 3.5, 1), size=vector(3, 0.5, 3), color=color.white, opacity=1)
            doorImage.texture = textures.wood_old


        if sim.roomName == sim.room.classroom:
            # create four walls of the room with length 8 and width 8
            wallR = box(pos=vector(16.25, 0, 1), size=vector(0.2, 28, 2), texture=textures.rough)
            wallL = box(pos=vector(-16.25, 0, 1), size=vector(0.2, 28, 2), texture=textures.rough)
            wallB = box(pos=vector(0, -14, 1), size=vector(32.5, 0.2, 2), texture=textures.rough)
            wallT = box(pos=vector(0, 14, 1), size=vector(32.5, 0.2, 2), texture=textures.rough)

            roomCoordinates= {"xmax":16.5, "xmin":-16.5, "ymax":7, "ymin":-10}

            # create floor
            floor = box(pos=vector(0, 0, -1), size=vector(32.5, 28, 2), texture=textures.metal)

            goalLocation = vector(15.5, 9.5, 0)
            goal = box(pos=vector(goalLocation.x-.5, goalLocation.y, goalLocation.z), size=vector(2, 2, 0.2), color=color.green, opacity=.5)

            # add door
            door = box(pos=vector(goalLocation.x+0.5, goalLocation.y, goalLocation.z), size=vector(0.5, 3, 5), texture=textures.wood)


            # create tables

            human_radius = 2
            barrierOpacity = 0
            tableTexture = textures.wood_old

            # Desk 1
            desk1 = box(pos=vector(0, -10, 0), size=vector(28, 1.5, 4), texture=tableTexture)
            desk1_barrier = box(pos=vector(0, -10, 0), size=vector(28 + sim.humanRadius*2 , 1.5 + sim.humanRadius*2, 4),
                                color=color.purple, opacity=barrierOpacity)
            label(pos=desk1.pos, text="Desk 1", xoffset=5, yoffset=5, space=10, height=10, border=4, font='sans', visible=sim.showLabels)
            # Desk 2
            desk2 = box(pos=vector(0, -5.5, 0), size=vector(28, 1.5, 4), texture=tableTexture)
            desk2_barrier = box(pos=vector(0, -5.5, 0), size=vector(28 + sim.humanRadius*2, 1.5 + sim.humanRadius*2, 4),
                                color=color.purple, opacity=barrierOpacity)
            label(pos=desk2.pos, text="Desk 2", xoffset=5, yoffset=5, space=10, height=10, border=4, font='sans', visible=sim.showLabels)
            # Desk 3
            desk3 = box(pos=vector(0, -1, 0), size=vector(28, 1.5, 4), texture=tableTexture)
            desk3_barrier = box(pos=vector(0, -1, 0), size=vector(28 + sim.humanRadius*2, 1.5 + sim.humanRadius*2, 4),
                                color=color.purple, opacity=barrierOpacity)
            label(pos=desk3.pos, text="Desk 3", xoffset=5, yoffset=5, space=10, height=10, border=4, font='sans', visible=sim.showLabels)
            # Desk 4
            desk4 = box(pos=vector(0, 3.5, 0), size=vector(28, 1.5, 4), texture=tableTexture)
            desk4_barrier = box(pos=vector(0, 3.5, 0), size=vector(28 + sim.humanRadius*2, 1.5 + sim.humanRadius*2, 4),
                                color=color.purple, opacity=barrierOpacity)
            label(pos=desk4.pos, text="Desk 4", xoffset=5, yoffset=5, space=10, height=10, border=4, font='sans', visible=sim.showLabels)
            # Teachers Desk
            teachers = box(pos=vector(-11, 7, 0), size=vector(7, 2.5, 4), texture=tableTexture)
            teachers_barrier = box(pos=vector(-11, 7, 0), size=vector(7 + sim.humanRadius*2, 2.5+sim.humanRadius*2, 4),
                                   color=color.purple, opacity=barrierOpacity)
            label(pos=teachers.pos, text="Teacher's Desk", xoffset=5, yoffset=5, space=10, height=10, border=4,
                  font='sans', visible=sim.showLabels)


            rectangles = [desk1_barrier, desk2_barrier, desk3_barrier, desk4_barrier, teachers_barrier]


        if sim.roomName == sim.room.jonesRoom:
            floor = box(pos=vector(0, 0, -1), size=vector(26, 28, 2), color=color.blue)

            wallR = box(pos=vector(13, 0, 1), size=vector(0.2, 28, 2), texture=textures.wood)
            wallL = box(pos=vector(-13, 0, 1), size=vector(0.2, 28, 2), texture=textures.wood)
            wallB = box(pos=vector(0, -14, 1), size=vector(26, 0.2, 2), texture=textures.wood)
            wallT = box(pos=vector(0, 14, 1), size=vector(26, 0.2, 2), texture=textures.wood)

            roomCoordinates= {"xmax":13, "xmin":-13, "ymax":14, "ymin":-14}



            goalLocation = vector(-11, -13.5, 0)
            goal = box(pos=goalLocation, size=vector(2, 1, 0.2), color=color.green)

            rectangles = []






















        # -------------------------- create vg polygons --------------------------#
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

        return graph, goalLocation, rectangles, roomCoordinates


    def run(graph, goalLocation, rectangles, roomCoordinates):


        people = []
        for i in range(sim.numHumans):
            while (True):


                # person = sphere(pos=vector(random.uniform(-7, 7), random.uniform(-7, 7), sim.humanRadius), radius=sim.humanRadius, color=color.red)
                person = sphere(pos=vector(random.uniform(roomCoordinates["xmin"] + 2*sim.humanRadius, roomCoordinates["xmax"] - 2*sim.humanRadius), random.uniform(roomCoordinates["ymin"] + 2*sim.humanRadius, roomCoordinates["ymax"] - 2*sim.humanRadius), sim.humanRadius), radius=sim.humanRadius, color=color.red)
                person.waitCount = 0



                if not sim.checkForCollision(person, rectangles, people):
                    people.append(person)
                    sim.plot_path(person, person.pos, rectangles, goalLocation, graph)

                    # create random value between 0.3 and 1
                    person.baseVelocity = sim.baseVelocity * random.uniform(0.3, 1)
                    break
                else:
                    person.visible = False




        # create timestep and loop over 10 seconds
        dt = 0.01
        totalTime = 100



        for t in arange(0, totalTime, dt):
            rate(100)
            # loop over all people
            for person in people:
                # move person
                moveX, moveY = sim.make_move(person, people)

                person.pos.x += moveX*dt
                person.pos.y += moveY*dt




if __name__ == '__main__':
    # run build
    graph, goalLocation, rectangles, roomCoordinates = sim.build(sim)
    sim.run(graph, goalLocation, rectangles, roomCoordinates)









