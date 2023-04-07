# Crowd Simulation
## Tips to run
I'd recommend using PyCharm to run the below since there's a couple heavy weight(ish) packages for the 3d graphics that can be a little annoying to install directly. If you have any issues or questions please open up an issue, I'm happy to help!

# File by file breakdown:
## main.py
- runs simulation, there's instructions at the bottom in the main function to run different templates (ie rooms + num humans)
- to edit any parameter, you can update it via the notation used to set the room and n, like so:
  - sim.baseVelocity = x
  - sim.secondsTakenToExitPP = y
- see list of params in below section to edit (edit these only in main function, not inside any of internal functions)

## runners/runnerN.py
- can run these different runner files to build data on evac time in parallel (speeds up data building by 5x)
- each will write to their own csv in assets/raw_csvs 
- run create_visuals.update_master_csv() to merge all the raw csvs

## create_visuals.py
- update_master_csv()
  - reads from all the raw csvs of data in assets/raw_csvs, and updates assets/master/master.csv by joining them

- built_n_time_linechart()
  - creates a new linechart that shows each rooms number of humans vs line 
  - writes to assets/visuals/n_vs_time.png



## Assets folder
- assets/master.csv
  - all data on evac time vs numHumans
  - make sure to run updateMasterCsv() in create_visuals.py before using to make sure it's updates with latest raw data from runners
- assets/raw_csvs
  - csvs for each of the runner files + the main file
- visuals
  - contains n_vs_time line chart
  - please build all plots into this folder
  

# Parameters

Access all of the below like: sim.paramName = x
| parameter                  | default        | description                                                                                                                                                |
| -------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| roomName                   | room.classroom | the selected room. can choose between: room.classroom, room.jonesRoom, room.meetingRoom, room.basic                                                        |
| numHumans                  | 70             | number of humans in the simulation                                                                                                                         |
| humanRadius                | 0.5            | radius of every human. should not increase beyond around .8 feet                                                                                           |
| baseVelocity               | 4              | maximum speed (feet / second) of the faster person, when unhindered                                                                                        |
| minSpeed                   | 0.001          | min speed at any given time. can set to 0 without breaking sim, but can be helpful if dealing with issues of stuck people                                  |
| minInitialSpeedCoefficient | 0.6            | the lower threshold of speed coefficient for velocity of given person, means slowest person will be baseVelocity * this                                    |
| coneWidth                  | 90             | the degrees of the cone an individual uses to considering other humans compared to their goal                                                              |
| coneRadius                 | 1              | any other individual not inside this radius will not effect this persons speed.                                                                            |
| showLabels                 | False          | useful for debugging objects to show their names in code, will show floating labels for each object                                                        |
| likelihoodOfWaiting        | 0.4            | for instances where 2 people could both logically go, we give a person a 40% chance to let the other person go first. this can be increased to show frenzy |
 


# Methodology
 1. build(selectRoom)
    1. takes in:
        1. a set of 3d rooms with dimension
        2. a set of obstacles for the humans to avoid
        3. a determined exit
            1. we are only modeling one door for now, but our code supports multiple with minor tweaks
    2. outputs
        1. a graph of the environment and obstacles

 2. human generation
     1. we randomly generate the humans locations
         1. we can choose to populate them in a specific area, like we do for the classroom, where we want people to be in their seats
     2. we assign them a speed coefficient (ranges from 0-1)
         1. personSpeed = baseSpeed * speedCoefficient
 3. path planning
     1. For each person:
         1. pick closest goal from goals (for now only working with one)
         2. calculate the shortest path to goal free of obstacles via visibility graphs
             1. This will store a series of vectors from the origin, representing the path as a series of interim goals
             2. show image
         3. store path in person
 4. movement
     1. Run a timestep
     2. For each individual:
         1. check if at interim goal
             1. if so, pop and move onto next iterim goal
             2. if nothing left in stack, person has arrived at exit
             3. return
         2. calculate direction vector
             1. tip to tip vector subtraction to get direction
                 1. we subtract interim goal from person.posVector
                 2. this will give us a vector to our goal
             2. normalize this vector to length 1
                 1. path = path / mag(path)
         3. loop through all other people for a few reasons
             1. find closest person in direction of goal
                 1. we calculate a “cone” in front of them to detect if there’s anyone in the way
                     1. this is parameterized, but for our final answer we used a 90 degree angle and a radius of 1
                 2. a person is inside the cone if they meet two criteria:
                     1. they’re within the cone radius
                         1. calculated by: mag ( otherPer.Vector - per.Vector) 
                     2. they’re within the cone angle
                         1. we calculate the angle between our goal path and the other person as: 
                             1. vectorToOther = otherPerson.posVec - person.posVec
                             2. arcos * (dot(path, vectorToOther) / mag(path) * mag(vectorToOther)
                 3. if this is the closest person we’ve found, we store that
             2. check if our path will hit anyone else
                 1. if our path will come close to hitting someone in front of us or coming close to colliding from the side with someone else, we have 60% chance of moving, and 40% of waiting
                     1. we parameterized this, because it can show levels of frenzy or calm
             3. set our velocity
                 1. velocity = max(sim.minSpeed, sqrt(closestPersonDistance))
                 2. the min speed is very very low, just to simulate a slightly forward motion (~1% max speed)
             4. multiply path * velocity 
                 1. this gives us a vector of magnitude velocity, in the direction we want to head
             5. multipy*path*dt
                 1. this moves us forward exactly enough for the 100th of second the timestep animation has passed
     3. exiting
         1. we set the rate of exiting through the door as follows
             1. secondsTakenToExitPP = (doorWidth / (baseVelocity * .5)) / (doorWidth / (humanRadius * 2))
                 1. we wanted to exiting to be faster when doors are wider and base velocity is higher, we also wanted it to be connected to width of a human
         2. our simulation controls how many people can exit to this exact above rate

 5. Conclusion
    1. To make a conclusion on a bigger room, find the legal required time to exit, and then use the table and data to triangulate how many people should be  in the room
    2. This can be further extending to much bigger and more complicated spaces to run into more spatial bottlenecks
    3. Can extend this by adding rooms in the build() function and to the room enum, that way you can add your own 3d rooms and can test on them
