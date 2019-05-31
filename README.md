# AI-Projects
Projects done in the Artificial Intelligence Course during Masters at USC

## Placing Police Officers(Using search algorithms)
1. Description: Placing Police Officers to the Blocks having some value(most number of crime activities in that block) such that you address max points such that no 2 officers are on same row & column & diagonal(similar to n queens)
2. Rest of the description can be found under description.pdf under Placing Police Officers folder.
3. activity_score.py: Used dfs search technique with recursion similar to nqueens problem and comparing all the nqueen solutions and giving the maximum score. Pruned search space as when queens are equal to number of blocks.


## Serving homeless community(Using game-playing algorithms)
1. Description: Two communities LAHSA(Homeless community), SPLA(Parking LA community) providing bed spaces as well parking spaces for homeless people and optimizing the spaces based on constraints and giving each other alternate turns to choose the best candidate(game playing algorithm)
2. Rest of the description can be found under description.pdf under Serving Homeless community folder.
3. game_playing_algo.py: Implemented alternate turn game playing algo which optimizes the best candidate to choose so that bed spaces and parking lots are filled optimally.
