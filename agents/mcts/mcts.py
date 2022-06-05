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
        self.steps_taken = 0


# def search(root: TreeNode, board, rounds: int):
    # https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    # for i in range(rounds):
        # update_tree(root, board, prev_action, finger_position)


def update_tree(root: TreeNode, board: NDArray[np.int8], prev_action: Literal['left', 'right', 'up', 'down', 'pass'], finger_position: tuple[int, int], min_steps: int, C: int):
    # not visited yet
    if root.hits == 0:
        value, _ = run_simulation(board, finger_position, prev_action, min_steps=0)
        root.total_value = value
        root.hits = 1
        can_pass = root.steps_taken >= min_steps
        expand(root, prev_action, finger_position, can_pass=can_pass)
        return value
    # visited, so update children and back propagate
    else:
        # pick children based on UCT
        max_action = select_action(root, C)

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
        value = update_tree(root.children[max_action], board, max_action, next_finger_position, min_steps, C=C)
        # move finger back
        swap(board, finger_position, next_finger_position)
        # update hits & value
        root.hits += 1
        root.total_value += value
        return value

def run_simulation(board: NDArray[np.int8], finger_position: tuple[int, int], prev_action: Literal['up', 'down', 'left', 'right'], min_steps: int):
    board_copy = np.copy(board)
    cur_action = None
    cur_finger_position = finger_position
    prev_action = prev_action
    path = []
    rows, cols = board.shape[0], board.shape[1]
    while True:
        can_pass = len(path) >= min_steps
        cur_action = random.choice(get_valid_actions(cur_finger_position, prev_action, rows, cols, include_pass=can_pass))
        path.append(cur_action)
        if cur_action == 'pass':
            break
        next_finger_position, is_valid_action = move_finger(cur_finger_position, cur_action)
        
        swap(board_copy, cur_finger_position, next_finger_position)
        prev_action = cur_action
        cur_finger_position = next_finger_position

        
    combos = cancel_until_termination(board_copy, False)
    return len(combos), path

def get_valid_actions(finger_position: tuple[int, int], prev_action: Literal['up', 'down', 'left', 'right'], rows: int, cols: int, include_pass: bool = True):
    valid_actions = list(action_list)
    if not include_pass:
        valid_actions.remove('pass')
        
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


def select_action(root: TreeNode, C: int):
    """selection action based on UCB

    Args:
        root (TreeNode): parent of children
        C (int): UCB constant

    Returns:
        string: action that has max UCB
    """
    assert len(root.children) > 0, "Did not expand properly"
    max_uct = 0
    max_action = None
    for action in root.children:
        child: TreeNode = root.children[action]
        uct = calc_uct(child.total_value, child.hits, root.hits, C=C)
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


def expand(node: TreeNode, prev_action: Literal['left', 'right', 'up', 'down'], finger_position: tuple[int, int], can_pass: bool):
    for action in get_valid_actions(finger_position, prev_action, 5, 6, include_pass=can_pass):
        # next_finger_position, is_valid_action = move_finger(finger_position, action)
        # if is_valid_action and OPPOSITE_ACTION[prev_action] != action:
        child = TreeNode()
        child.steps_taken = node.steps_taken + 1
        node.children[action] = child


def calc_uct(total_value: int, n: int, N: int, C: float = 2**0.5):
    if n == 0:
        return float('inf')
    return total_value / n + C * math.sqrt(math.log(N)/n)

def pick_best_action(root: TreeNode):
    max_mean_value = 0
    max_action = None
    for action in root.children:
        child: TreeNode = root.children[action]
        mean_value = child.total_value / child.hits if child.hits > 0 else 0
        if mean_value > max_mean_value:
            max_mean_value = mean_value
            max_action = action
    return max_action

def find_best_path_mcts(board: NDArray[np.int8], finger_position: tuple[int, int], path_len: int, simulations_per_step: int):
    board_copy = np.copy(board)
    root = TreeNode()
    prev_action = None
    path = []
    for i in range(path_len):
        for j in range(simulations_per_step):
            update_tree(root, board_copy, prev_action, finger_position)
        action = pick_best_action(root)
        path.append(action)
        if (action == 'pass'):
            break
        next_finger_position, is_valid_action = move_finger(finger_position, action) 
        print(f'finger: {finger_position}, move: {action}')
        swap(board_copy, finger_position, next_finger_position)
        finger_position = next_finger_position
        root = root.children[action]
    return path

def find_best_path_mcts2(board: NDArray[np.int8], finger_position: tuple[int, int], min_path_len: int, total_simulations: int, C: int):
    """ Find the best path using MCTS. Does not move the root. Just run the simulations

    Args:
        board (NDArray[np.int8]): _description_
        finger_position (tuple[int, int]): _description_
        path_len (int): _description_
        total_simulations (int): _description_

    Returns:
        _type_: _description_
    """
    board_copy = np.copy(board)
    root = TreeNode()
    prev_action = None
    path = []
    for j in range(total_simulations):
        update_tree(root, board_copy, prev_action, finger_position, min_steps=min_path_len, C=C)
    while True:
        action = pick_best_action(root)
        path.append(action)
        if (action == 'pass'):
            break
        root = root.children[action]
    return path




if __name__ == '__main__':
    env = PAD()
    print(env.board.tolist())
    path = find_best_path_mcts2(env.board, env.finger, min_path_len=50, total_simulations=20000)
    # TODO: Add max combo termination
    # TODO: Unit tests
    # TODO: tune steps, rounds, C
    print(path)
    for action in path:
        env.step(env.action_to_num[action])
    print('Rendering gif...')
    env.visualize(f"mcts/no-pass.gif")
    # root = TreeNode()
    # for i in range(10000):
        # update_tree(root, env.board, None, (0, 2))
    # action = pick_best_action(root)
    # print('max action: ', action)