import gym
from gym import spaces
from collections import deque
import numpy as np

from snake import *

SPEED = 25 # Pygame clock

class SnakeEnv(gym.Env):
    """Custom Environment that follows gym interface"""

    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.goal = 30
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(5)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf,
                                            shape=(self.goal+8,), dtype=np.float64)

    def step(self, action):
        self.prev_actions.append(action)
        main(SPEED) # Game

        if action == 0: # Do nothing
            pass
        if action == 1: # Left
            snake.turn(left)
        if action == 2: # Up
            snake.turn(up)
        if action == 3: # Right
            snake.turn(right)
        if action == 4: # Down
            snake.turn(down)

        self.reward = data()["reward"] * 10

        danger_left = float(data()["danger"][0])
        danger_up = float(data()["danger"][1])
        danger_right = float(data()["danger"][2])
        danger_down = float(data()["danger"][3])

        food_left = float(data()["foodpos"][0])
        food_up = float(data()["foodpos"][1])
        food_right = float(data()["foodpos"][2])
        food_down = float(data()["foodpos"][3])

        self.prev_actions = deque(maxlen=self.goal)

        for _ in range(self.goal):
            self.prev_actions.append(-1)

        self.observation = [danger_left, danger_up, danger_right, danger_down, food_left, food_up, food_right, food_down] + list(self.prev_actions)
        self.observation = np.array(self.observation)

        info = {}
        return self.observation, self.reward, self.done, info

    def reset(self):
        self.done = False

        snake.reset() # Resets game

        # danger_left, danger_up, danger_right, danger_down, food_left, food_up, food_right, food_down (8)

        danger_left = float(data()["danger"][0])
        danger_up = float(data()["danger"][1])
        danger_right = float(data()["danger"][2])
        danger_down = float(data()["danger"][3])

        food_left = float(data()["foodpos"][0])
        food_up = float(data()["foodpos"][1])
        food_right = float(data()["foodpos"][2])
        food_down = float(data()["foodpos"][3])

        self.prev_actions = deque(maxlen=self.goal)

        for _ in range(self.goal):
            self.prev_actions.append(-1)

        self.observation = [danger_left, danger_up, danger_right, danger_down, food_left, food_up, food_right, food_down] + list(self.prev_actions)
        self.observation = np.array(self.observation)

        return self.observation
