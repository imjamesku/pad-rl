import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-3]))
from ppad.pad.game import PAD
import os
import numpy as np






game = PAD()
game.reset(finger=np.array([0, 0]))
game.step(action=0)
game.step(action=0)
game.step(action=1)
print(os.environ['PPADPATH'])
print(game.board)
game.visualize(filename='test.gif')