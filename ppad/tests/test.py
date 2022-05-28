import sys,os; sys.path.append('/'.join(os.path.realpath(__file__).split('/')[:-3]))
from ppad.pad.game import PAD
import os






game = PAD()
game.reset()
game.step(action="right")
print(os.environ['PPADPATH'])
print(game.board)
game.visualize(filename='test')