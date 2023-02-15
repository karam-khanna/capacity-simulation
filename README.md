# capacity-simulation

# file mapping
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



## assets folder
- assets/master.csv
  - all data on evac time vs numHumans
  - make sure to run updateMasterCsv() in create_visuals.py before using to make sure it's updates with latest raw data from runners
- assets/raw_csvs
  - csvs for each of the runner files + the main file
- visuals
  - contains n_vs_time line chart
  - please build all plots into this folder
  

# parameters

Access all of the below like: sim.paramName = x
| parameter                  | default        | description                                                                                                                                                |
| -------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| roomName                   | room.classroom | the selected room. can choose between: room.classroom, room.jonesRoom, room.meetingRoom, room.basic                                                        |
| numHumans                  | 80             | number of humans in the simulation                                                                                                                         |
| humanRadius                | 0.5            | radius of every human. should not increase beyond around .8 feet                                                                                           |
| baseVelocity               | 4              | maximum speed (feet / second) of the faster person, when unhindered                                                                                        |
| minSpeed                   | 0.001          | min speed at any given time. can set to 0 without breaking sim, but can be helpful if dealing with issues of stuck people                                  |
| minInitialSpeedCoefficient | 0.6            | the lower threshold of speed coefficient for velocity of given person, means slowest person will be baseVelocity * this                                    |
| coneWidth                  | 90             | the degrees of the cone an individual uses to considering other humans compared to their goal                                                              |
| coneRadius                 | 1              | any other individual not inside this radius will not effect this persons speed.                                                                            |
| showLabels                 | False          | useful for debugging objects to show their names in code, will show floating labels for each object                                                        |
| likelihoodOfWaiting        | 0.4            | for instances where 2 people could both logically go, we give a person a 40% chance to let the other person go first. this can be increased to show frenzy |
 
