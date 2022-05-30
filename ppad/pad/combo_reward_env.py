from ppad.pad.game import PAD
import gym
import ppad.pad.utils as pad_utils
import numpy as np

class ComboRewardEnv(gym.Env):
    def __init__(self):
        super(ComboRewardEnv, self).__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        # Example for using image as input (channel-first; channel-last also works):
        self.game = PAD()
        self.action_space = self.game.action_space
        self.observation_space = self.game.observation_space

    def step(self, action):
        obs, reward, done, info = self.game.step(action)
        reword = 0
        if self.game.action_mapping[action] != 'pass':
            if info['is_invalid_move'] == True or info['did_go_back'] == True:
                reward -= 10
        if done:
            reward += self.calculate_reward(self.game.board)
        return obs, reward, done, info
    def reset(self):
        return self.game.reset()
    def render(self, board):
        self.game.render(board)

    def visualize(self, filename, shrink=3, animate=True):
        self.game.visualize(filename)
    def calculate_reward(self, board=None, skyfall_damage=True, verbose=False):
        # Make a copy of the board.
        board = np.copy(board)

        # A list of dictionaries to store combos.
        all_combos = []
        # Repeat the combo detection until nothing more can be canceled.
        while True:
            if verbose == True:
                print('Board before combo canceling:')
                self.render(board)
                print(board)

            combos = pad_utils.cancel(board)
            if verbose == True:
                print('Board after combo canceling:')
                self.render(board)
                print(board)

            # Break out of the loop if nothing can be canceled.
            if len(combos) < 1:
                break

            # Add combo to combo list and skyfall.
            all_combos += combos
            if skyfall_damage == False:
                break

            board = self.game.drop(board=board)
            if verbose == True:
                print('Board after orb drop:')
                self.render(board)
            board = self.game.fill_board(board=board)
            if verbose == True:
                print('Board after fill board:')
                self.render(board)

        # Reward is the total damage calculated based on combos.
        reward = len(all_combos)
        if verbose == True:
            print(all_combos)
            print('The total combo is:', reward)
        return reward