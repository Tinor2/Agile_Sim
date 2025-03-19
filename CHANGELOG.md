* Created MVP, took feedback from client, and brought in a example (c9ac83e)

* Began working on creating the grid and creating the rooms iteratively, without hardcoding values. The method I am using to do this, is by identifing each room by a grid coordinate, with the top left room being 0,0. The doors are identified by whichever room is to the left, or above the door. For example, the door connecting cells (0,0) and (0,1) would just be identified by (0,0,y) #(probably, not too sure how to indicate whether the door is going up or down yet.) (1b3c64f)

* Started creating next MVP (e52d624)

* Revamped grids and rooms Firstly, I used AI to provide a solid basis on creating different rooms and linking them with a grid. I also created a json database, which will be used to keep track of icons and symbols used to represent different items Created the rooms themselves, added a 2D grid to organise, representing each cell, and created a system to render said rooms with doors. (cb780b9)

* Added player movement, and player moving around rooms Currently, need to fix a bug to make the rendering perfect (34fad39)

* FIXED PLAYER MOVEMENT player can move through rooms, pass through doors, without any errors. Small bug where player's character does not get erased when the room changes (2a1eaaa)

* Added randomly generated puzzles These puzzles spawn randomly across the grid. TODO: Add a list of room id's that are blacklisted from certain puzzles       Generalize the puzzle addition feature to be able to add any special cell (f92920e)

* added puzzle geneation, can now generate puzzles randomly in rooms, with a limit of the amount of puzzles that can generate per room. Also fixed prior bug where the player symbol didn't get erased. (3206e3c)