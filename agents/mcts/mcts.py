from ppad.pad.game import PAD
import math
from numpy.typing import NDArray
from agents.dfs.dfs import move_finger, swap, OPPOSITE_ACTION
import numpy as np
from typing import Literal
from ppad.pad.utils import cancel_until_termination
import random

action_list = ['left', 'right', 'up', 'down', 'pass']
# TODO don't go back

# left, right, up, down, pass


class TreeNode:
    def __init__(self):
        self.total_value = 0
        self.hits = 0
        self.children = {}
        self.terminal_value = None # number of combos at this state


# def search(root: TreeNode, board, rounds: int):
    # https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    # for i in range(rounds):
        # update_tree(root, board, prev_action, finger_position)


def update_tree(root: TreeNode, board: NDArray[np.int8], prev_action: Literal['left', 'right', 'up', 'down', 'pass'], finger_position: tuple[int, int]):
    # not visited yet
    if root.hits == 0:
        value = run_simulation(board, finger_position, prev_action)
        root.total_value = value
        root.hits = 1
        expand(root, prev_action, finger_position)
        return value
    # visited, so update children and back propagate
    else:
        # pick children based on UCT
        max_action = select_action(root)

        if max_action == 'pass':
            # calculate combo
            child: TreeNode = root.children['pass']
            if child.terminal_value is None:
                board_copy = np.copy(board)
                combos = cancel_until_termination(board_copy, False)
                child.terminal_value = len(combos)

            child.total_value += child.terminal_value
            root.total_value += child.terminal_value
            child.hits += 1
            root.hits += 1
            return child.terminal_value
        
        # move finger
        next_finger_position, is_valid_action = move_finger(finger_position, max_action)
        assert is_valid_action, "Should always be valid"
        # swap orbs
        swap(board, finger_position, next_finger_position)
        # update children
        value = update_tree(root.children[max_action], board, max_action, next_finger_position)
        # move finger back
        swap(board, finger_position, next_finger_position)
        # update hits & value
        root.hits += 1
        root.total_value += value
        return value

def run_simulation(board: NDArray[np.int8], finger_position: tuple[int, int], prev_action: Literal['up', 'down', 'left', 'right']):
    board_copy = np.copy(board)
    action = None
    while True:
        action = random.choice(get_valid_actions(finger_position, prev_action, 5, 6))
        if action == 'pass':
            break
        next_finger_position, is_valid_action = move_finger(finger_position, action)
        swap(board_copy, finger_position, next_finger_position)

    combos = cancel_until_termination(board_copy, False)
    return len(combos)

def get_valid_actions(finger_position: tuple[int, int], prev_action: Literal['up', 'down', 'left', 'right'], rows: int, cols: int):
    valid_actions = list(action_list)
    if finger_position[0] == 0:
        valid_actions.remove('up')
    elif finger_position[0] == rows - 1:
        valid_actions.remove('down')
    if finger_position[1] == 0:
        valid_actions.remove('left')
    elif finger_position[1] == cols - 1:
        valid_actions.remove('right')
    
    if prev_action is None:
        return valid_actions

    back_action = OPPOSITE_ACTION[prev_action]
    if back_action in valid_actions:
        valid_actions.remove(back_action)
    return valid_actions


def select_action(root: TreeNode):
    assert len(root.children) > 0, "Did not expand properly"
    max_uct = 0
    max_action = None
    for action in root.children:
        child: TreeNode = root.children[action]
        uct = calc_uct(child.total_value, child.hits, root.hits)
        if uct > max_uct:
            max_uct = uct
            max_action = action
    return max_action

# def select_leaf_node(root: TreeNode):
#     if root.hits == 0:
#         return root
#     # return child with highest UCT
#     max_action = select_children(root)
#     # max_uct = 0
#     # max_action = None
#     # for action in action_list:
#     #     child: TreeNode = root.children[action]
#     #     uct = calc_uct(child.total_value, child.hits, root.hits)
#     #     if uct > max_uct:
#     #         max_uct = uct
#     #         max_action = action
#     return select_leaf_node(root.children[max_action])


def expand(node: TreeNode, prev_action: Literal['left', 'right', 'up', 'down'], finger_position: tuple[int, int]):
    for action in get_valid_actions(finger_position, prev_action, 5, 6):
        # next_finger_position, is_valid_action = move_finger(finger_position, action)
        # if is_valid_action and OPPOSITE_ACTION[prev_action] != action:
        node.children[action] = TreeNode()


def calc_uct(total_value: int, n: int, N: int, C: float = 2**0.5):
    if n == 0:
        return float('inf')
    return total_value / n + C * math.sqrt(math.log(N)/n)

def pick_best_action(root: TreeNode):
    max_mean_value = 0
    max_action = None
    for action in root.children:
        child: TreeNode = root.children[action]
        mean_value = child.total_value / child.hits
        if mean_value > max_mean_value:
            max_mean_value = mean_value
            max_action = action
    return max_action



if __name__ == '__main__':
    env = PAD()
    root = TreeNode()
    for i in range(1000):
        update_tree(root, env.board, None, (0, 2))
    action = pick_best_action(root)
    print('max action: ', action)