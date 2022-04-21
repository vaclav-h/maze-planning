import sys
from collections import defaultdict
import random


class VIMaze:
    def __init__(self, path):
        self.maze = self.load_maze(path)
        self.states = self.get_all_valid_states()
        self.policy = self.init_policy()
        self.state_value = defaultdict(lambda:0)
        self.next_state_probs = dict()

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

    def get_all_valid_states(self):
        states = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] != "#" and len(self.get_actions((i, j))) > 0:
                    states.append((i, j))
        return states

    def is_terminal(self, state):
        return self.maze[state[0]][state[1]] == "E"

    def is_valid_action(self, action):
        try:
            # Move within the maze
            return self.maze[action[0]][action[1]] != '#'
        except:
            # Move out of the maze
            return False

    def get_actions(self, state):
        actions = []
        i, j = state
        if self.is_valid_action((i-1, j)):
            actions.append((i-1, j))
        if self.is_valid_action((i, j-1)):
            actions.append((i, j-1))
        if self.is_valid_action((i, j+1)):
            actions.append((i, j+1))
        if self.is_valid_action((i+1, j)):
            actions.append((i+1, j))
        return actions

    def init_policy(self):
        policy = dict()
        for state in self.states:
            if self.is_terminal(state):
                policy[state] = None
                continue
            actions = self.get_actions(state)
            policy[state] = random.choice(actions)
        return policy

    def get_next_states_and_probs(self, state, action):
        """
        Returns list of next states reachable from current state when using given action 
        [(state1, probability1), (state2, probability2), ...] 
        """
        if (state, action) in self.next_state_probs:
            return self.next_state_probs[(state, action)]

        states_probs = []

        # wants to go up or down
        up_or_down = action[1] - state[1] == 0
        
        if up_or_down:
            # go east
            bad_action1 = (state[0], state[1]+1)
        else:
            # go south
            bad_action1 = (state[0]+1, state[1])

        if up_or_down:
            # go west
            bad_action2 = (state[0], state[1]-1)
        else:
            #go north
            bad_action2 = (state[0]-1, state[1])

        states_probs.append((action, 0.7))

        if self.is_valid_action(bad_action1):
            states_probs.append((bad_action1, 0.15))
        else:
            states_probs.append((state, 0.15))

        if self.is_valid_action(bad_action2):
            states_probs.append((bad_action2, 0.15))
        else:
            states_probs.append((state, 0.15))

        self.next_state_probs[(state, action)] = states_probs
        return states_probs

    def get_reward(self, state):
        if self.maze[state[0]][state[1]] in [' ', 'S']:
            return -1
        elif self.maze[state[0]][state[1]] == 'D':
            return -50
        elif self.maze[state[0]][state[1]] == 'E':
            return 200

    def value_iteration(self, discount, eps, max_iter):
        delta = float('inf')

        it = 0
        while delta > eps and it < max_iter:
            it += 1
            delta = 0
            for state in self.states:
                if not self.is_terminal(state):
                    max_value = -float('inf')
                    for action in self.get_actions(state):
                        next_states_and_probs = self.get_next_states_and_probs(state, action)
                        new_value = 0
                        for next_state, prob in next_states_and_probs:
                            new_value += prob * (self.get_reward(next_state) + discount *
                                                 self.state_value[next_state])
                        if new_value > max_value:
                            max_value = new_value
                            best_action = action
                    # Maximal change in this iteration
                    delta = max(delta, abs(self.state_value[state] - max_value))
                    self.state_value[state] = max_value
                    self.policy[state] = best_action

    def step(self, state, action):
        """
        Make single step from state with success probability 0.7 and probability
        0.15 to go sideways
        """
        chance = random.random()

        # wants to go up or down
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
        """
        Executes single traversal through the maze while following policy learned
        by value-iteration and returns the reward
        """
        state = start
        reward = 0
        while not self.is_terminal(state):
            state, r = self.step(state, self.policy[state])
            reward += r
        return reward


if __name__ == '__main__':
    maze = VIMaze(sys.argv[1])
    maze.value_iteration(0.999999, 1e-9, 500)

    TRIALS = 1000
    rewards = []
    for i in range(TRIALS):
        rewards.append(maze.traverse((0, 1)))
    print("Average reward over %d trials: %f" % (TRIALS, sum(rewards) / TRIALS))
    print("State value of initial state: %f" % (maze.state_value[(0, 1)]))
