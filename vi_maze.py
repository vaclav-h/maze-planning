import random
from collections import defaultdict
from maze import Maze


class VIMaze(Maze):
    def __init__(self, path):
        super().__init__(path)
        self.states = self.get_all_valid_states()
        self.policy = self.init_policy()
        self.state_value = defaultdict(lambda:0)
        self.next_state_probs = dict()

    def get_all_valid_states(self):
        states = []
        for i in range(len(self.maze)):
            for j in range(len(self.maze[0])):
                if self.maze[i][j] != "#" and len(self.get_actions((i, j))) > 0:
                    states.append((i, j))
        return states

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

    def traverse(self, start):
        """
        Executes single traversal through the maze while following policy learned
        by value-iteration and returns the reward and path
        """
        path = []
        path.append(start)

        state = start
        reward = 0
        while not self.is_terminal(state):
            state, r = self.step(state, self.policy[state])
            reward += r
            path.append(state)
        return reward, path

