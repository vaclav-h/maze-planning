import sys
import random
from priority_queue import PriorityQueue
from collections import defaultdict


class FFMaze:
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

    def get_state_dist(self, state):
        """
        Distances for Dijkstra to find shortest path to goal while avoiding delays
        """
        if self.maze[state[0]][state[1]] in [' ', 'S']:
            return 1
        elif self.maze[state[0]][state[1]] == 'D':
            return 50
        elif self.maze[state[0]][state[1]] == 'E':
            return 0

    def get_state_reward(self, state):
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

    def expand_state(self, state):
        """
        Returns list of valid transitions and their coresponding costs like so
        [(state1, cost1), (state2, cost2), ...]
        """
        next_state_cost = []
        i, j = state
        if self.is_valid_action((i-1, j)):
            next_state_cost.append(((i-1, j), self.get_state_dist((i-1, j))))
        if self.is_valid_action((i, j-1)):
            next_state_cost.append(((i, j-1), self.get_state_dist((i, j-1))))
        if self.is_valid_action((i, j+1)):
            next_state_cost.append(((i, j+1), self.get_state_dist((i, j+1))))
        if self.is_valid_action((i+1, j)):
            next_state_cost.append(((i+1, j), self.get_state_dist((i+1, j))))
        return next_state_cost

    def find_plan(self, start):
        """
        Finds plan using Dijkstra algorithm
        """
        pq = PriorityQueue() 
        parent = {}
        dist = defaultdict(lambda:float('inf'))
        dist[start] = 0
       
        pq.push(start, 0)
        while not pq.empty():
            u = pq.pop()
            if self.is_terminal(u):
                return self.reconstruct_plan(parent, start, u)
            for (v, cost) in self.expand_state(u):
                new_dist = dist[u] + cost
                if new_dist < dist[v]:
                    parent[v] = u
                    dist[v] = new_dist
                    pq.push(v, new_dist)
        return None

    def reconstruct_plan(self, parent, start, goal):
        """
        Reconstructs plan from goal to start
        """
        plan = []
        state = goal
        while state != start:
            plan.insert(0, state)
            state = parent[state]
        return plan

    def step(self, state, action):
        """
        Make single step from state with success probability 0.7 and probability
        0.15 to go sideways
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
            return next_state, self.get_state_reward(next_state)
        else:
            return state, self.get_state_reward(state)

    def traverse(self, start):
        """
        Executes single traversal through the maze using FF-Replan and returns
        the reward
        """
        reward = 0
        plan = self.find_plan(start)
        state = start
        while not self.is_terminal(state):
            action = plan.pop(0)
            state, r = self.step(state, action)
            reward += r
            # If action was not successful => replan
            if state != action:
                plan = self.find_plan(state)
        return reward

if __name__ == '__main__':
    maze = FFMaze(sys.argv[1])

    TRIALS = 100
    rewards = []
    for i in range(TRIALS):
        rewards.append(maze.traverse((0, 1)))
    print("Average reward over %d trials: %f" % (TRIALS, sum(rewards) / TRIALS))
