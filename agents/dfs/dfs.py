from ppad.pad.game import PAD
from numpy.typing import NDArray
from ppad.pad.utils import cancel_until_termination
import numpy as np
from typing import Literal, List
import time
from collections import deque

env = PAD()
OPPOSITE_ACTION = {
    'up': 'down',
    'down': 'up',
    'left': 'right',
    'right': 'left'
}

ACTION_OFFSET = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1)
}

NUM_ROW = 5
NUM_COL = 6


def find_best_path(board: NDArray[np.int8], finger_position: tuple[int, int], depth: int):
    result = dfs(board, finger_position, 'none', depth)
    return result


def move_finger(finger_position: tuple[int, int], step: Literal['up, down', 'left', 'right']):
    """try to move the finger

    Args:
        finger (tuple[int, int]): position of dinger
        step (Literal[&#39;up, down&#39;, &#39;left&#39;, &#39;right&#39;]): direction of movement

    Returns:
        tuple[tuple[int, int], int]: (next_finger_position, is_valid_action)
    """
    offset_row, offset_col = ACTION_OFFSET[step]
    next_finger_position = (finger_position[0] + offset_row, finger_position[1] + offset_col)
    if next_finger_position[0] < 0 or next_finger_position[0] >= NUM_ROW or next_finger_position[1] < 0 or next_finger_position[1] >= NUM_COL:
        return finger_position, False
    return next_finger_position, True

def dfs(board: NDArray[np.int8], finger_position: tuple[int, int], prev_action: Literal['up','down', 'left', 'right', 'none'], remaining_steps: int)->tuple[int, List[str]]:
    assert len(finger_position) == 2
    assert board.shape == (NUM_ROW, NUM_COL)
    board_copy = np.copy(board)
    if remaining_steps == 0:
        combos = cancel_until_termination(board_copy, False)
        # print(board)
        return len(combos), deque()
    max_combo = 0
    max_path = deque()
    for direction in ['up', 'down', 'left', 'right']:
        if OPPOSITE_ACTION[direction] == prev_action:
            # dont go back
            continue
        # moving out of bound
        next_finger_position, is_valid_action = move_finger(finger_position, direction)
        if not is_valid_action:
            continue
        # swap orbs
        swap(board, finger_position, next_finger_position)
        combo_count, path = dfs(board, next_finger_position, direction, remaining_steps - 1)
        if combo_count > max_combo:
            max_combo = combo_count
            max_path = path
            max_path.appendleft(direction)
        # swap back
        swap(board, finger_position, next_finger_position)
    return max_combo, max_path

def swap(board: NDArray[np.int8], finger: tuple[int, int], next_finger: tuple[int, int]):
    board[finger[0], finger[1]], board[next_finger[0], next_finger[1]] = board[next_finger[0], next_finger[1]], board[finger[0], finger[1]]

if __name__ == "__main__":
    env.render()
    test_board = np.array([[1, 0, 5, 4, 0, 1],
    [5, 3, 1, 0, 0, 1],
    [2, 5, 3, 0, 5, 2],
    [1, 1, 5, 3, 2, 4],
    [4, 0, 1, 3, 4, 2]])
    print(env.board)
    start = time.time()

    combos, path = find_best_path(test_board, (0, 2), 6)
    print('combos: ', combos)
    print('execution time: ', time.time() - start)