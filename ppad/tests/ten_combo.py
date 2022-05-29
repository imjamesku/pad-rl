import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-3]))
from ppad.pad.game import PAD
import os
import numpy as np


# int2english = {0: 'red',
#                1: 'blue',
#                2: 'green',
#                3: 'light',
#                4: 'dark',
#                5: 'heal',
#                6: 'jammer',
#                7: 'poison',
#                8: 'mortal poison',
#                9: 'bomb'}



game = PAD()
game.reset(board=np.array([
    [1, 4, 4, 1, 1, 3],
    [5, 1, 4, 0, 3, 2],
    [1, 5, 1, 3, 2, 5],
    [4, 1, 5, 2, 5, 0],
    [4, 4, 1, 5, 0, 0]
], ), finger=np.array([0, 3]))
obs, reward, done, info = game.step(action=2)
print(obs[:, :, 0])
print(obs[:, :, 1])
obs, reward, done, info = game.step(action=1)
print(obs[:, :, 0])
print(obs[:, :, 1])
obs, reward, done, info = game.step(action=1)
print(obs[:, :, 0])
print(obs[:, :, 1])

obs, reward, done, info = game.step(action=1)
print(obs[:, :, 0])
print(obs[:, :, 1])
obs, reward, done, info = game.step(action=1)
print(obs[:, :, 0])
print(obs[:, :, 1])
game.step(action=2)
game.step(action=2)
game.step(action=0)
game.step(action=0)
game.step(action=0)
game.step(action=0)
game.step(action=3)
game.step(action=3)
game.step(action=3)
game.step(action=1)
game.step(action=1)
game.step(action=1)
game.step(action=1)
game.step(action=3)
game.step(action=3)
game.step(action=0)
game.step(action=0)
game.step(action=0)
game.step(action=0)
game.step(action=2)
obs, reward, done, info = game.step(action=2)
print(obs[:, :, 0])
print(obs[:, :, 1])
# game.step(action=0)
# game.step(action=4)
# game.step(action=2)
# game.step(action=3)
print(os.environ['PPADPATH'])
# print(game.board)
# game.visualize(filename='ten_combo.gif')