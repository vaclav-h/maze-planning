# maze-planning

Simple scripts for finding plan in stochastic maze (grid-world).

Sample mazes can be found in `data` folder. The format of the data files is as follows:

* Each file starts with two numbers specifying the number of rows and columns
* '#' is a wall
* 'S' is starting position
* 'D' is delay position
* 'E' is the goal
* ' '  (space character) is free space

The goal is to navigate from start to goal using up/down/left/right actions.

#### Probabilistic setting:

* Whenever the agent decides to go in one direction, he will do so with probability **0.7** and he will go sideways with probability **0.15**
* If he hits the wall he stays put (but it still counts as a transition)

#### Rewards:

* For reaching the goal the agent receives reward of **200**
* For stepping on delay he receives reward of  **-50**
* For every other transition he receives **-1**

### Implemented algorithms
* #### FF-Replan
    * `ff_maze.py` contains implementation of FF-Replan algorithm for described maze environments.
    * Demo usage  ``python3 ff_maze.py path_to_maze_file.txt``
* #### Value-iteration
    * `vi_maze.py` contains implementation of Value-Iteration for described maze environments
    * Demo usage ``python3 vi_maze.py path_to_maze_file.txt``

