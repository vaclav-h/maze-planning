from utils import PriorityQueue
from collections import defaultdict
from maze import Maze


class FFMaze(Maze):

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

    def traverse(self, start):
        """
        Executes single traversal through the maze using FF-Replan and returns
        the reward and path
        """

        path = []
        path.append(start)

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
            path.append(state)
        return reward, path
