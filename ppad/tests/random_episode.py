import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-3]))
from ppad.pad.game import PAD
from ppad.pad.combo_reward_env import ComboRewardEnv
import os
import numpy as np

game = ComboRewardEnv()
game.reset()
done = False
while not done:
    action = game.action_space.sample()
    obs, reward, done, info = game.step(action)
    print(f"combo: {reward}")
    # game.render()

print("done")
print(os.environ['PPADPATH'])
game.visualize(filename='random_episode.gif')