import random


class Maze:
    def __init__(self, path):
        self.maze = self.load_maze(path)

    def load_maze(self, path):
        with open(path) as f:
            line = f.readline().split()
            n = int(line[0])
            m = int(line[1])
            maze = [['x' for j in range(m)] for i in range(n)]
            for i in range(n):
                line = f.readline().strip()
                for (j, c) in enumerate(line):
                    maze[i][j] = c
        return maze

    def get_reward(self, state):
        if self.maze[state[0]][state[1]] in [' ', 'S']:
            return -1
        elif self.maze[state[0]][state[1]] == 'D':
            return -50
        elif self.maze[state[0]][state[1]] == 'E':
            return 200

    def is_terminal(self, state):
        return self.maze[state[0]][state[1]] == "E"

    def is_valid_action(self, action):
        try:
            # Move within the maze
            return self.maze[action[0]][action[1]] != '#'
        except:
            # Move out of the maze
            return False

    def step(self, state, action):
        """
        Make single step from state with 0.7 success probability and 0.15 probability
        to go sideways
        """
        chance = random.random()

        # check if he wants to go up or down
        up_or_down = action[1] - state[1] == 0
        
        if chance < 0.15:
            if up_or_down:
                # go east
                next_state = (state[0], state[1]+1)
            else:
                # go south
                next_state = (state[0]+1, state[1])
        elif chance < 0.3:
            if up_or_down:
                # go west
                next_state = (state[0], state[1]-1)
            else:
                #go north
                next_state = (state[0]-1, state[1])
        else:
            next_state = action

        if self.is_valid_action(next_state):
            return next_state, self.get_reward(next_state)
        else:
            return state, self.get_reward(state)

    def traverse(self, start):
        pass