import numpy as np
from mcts import find_best_path_mcts2
from ppad.pad.game import PAD
board = np.array([[0, 4, 1, 4, 5, 5],[3, 5, 2, 2, 3, 4], [
                 5, 3, 5, 4, 2, 0], [1, 1, 5, 3, 4, 2], [3, 0, 0, 1, 4, 3]])

finger = np.array([1, 4])
MIN_LEN = 20
SIMS = 1000
C = 1

env = PAD(board=board, finger=finger)

path, child_not_explored = find_best_path_mcts2(env.board, env.finger, min_path_len=MIN_LEN, total_simulations=SIMS, C=C)
print(path)
print('child not explored: ', child_not_explored)
for action in path:
    env.step(env.action_to_num[action])
print('Rendering gif...')
env.visualize(f"mcts/sim_without_min_len_{MIN_LEN}_{SIMS}.gif")