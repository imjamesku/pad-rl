from ppad.pad.utils import cancel_until_termination
from dfs import dfs, move_finger, swap
from numpy.typing import NDArray
import numpy as np
def find_best_path(board: NDArray[np.int8], finger_position: tuple[int, int], depth: int, steps: int):
    """find the best path by using des on every step

    Args:
        board (NDArray[np.int8]): _description_
        finger_position (tuple[int, int]): _description_
        depth (int): _description_
    """
    prev_action = 'none'
    cur_finger_position = finger_position
    path = []
    for i in range(steps):
        print('step', i)
        max_combo, max_path = dfs(board, cur_finger_position, prev_action, depth)
        # print(max_combo, max_path)
        action = max_path[0]
        # print(action)
        path.append(action)
        # is_valid_action is guaranteed to be True, because the action is from dfs
        next_finger_position, is_valid_action = move_finger(cur_finger_position, action)
        # print(cur_finger_position, next_finger_position)
        swap(board, cur_finger_position, next_finger_position)
        cur_finger_position = next_finger_position
        prev_action = action
        # print(board)
    combos = cancel_until_termination(board, False)
    return path, len(combos)

if __name__ == "__main__":
    test_board = np.array([[1, 0, 5, 4, 0, 1],
    [5, 3, 1, 0, 0, 1],
    [2, 5, 3, 0, 5, 2],
    [1, 1, 5, 3, 2, 4],
    [4, 0, 1, 3, 4, 2]])


    path, combos = find_best_path(board=test_board, finger_position=(0, 2), depth=8, steps=30)
    print(path)
    print('combos', combos)
