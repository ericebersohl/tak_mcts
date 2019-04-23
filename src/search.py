import random
from typing import Tuple
import pprint
import copy
import pdb

from .node import Node
from .types import State, Action
from .game import simulate, validate_action, get_next_state, check_victory, get_actions
from .utils import print_state, get_action_string

def mcts(root: State, iterations: int) -> Action:
    root_node: Node = Node(action = None, state = root, parent = None)

    for i in range(iterations):
        # pdb.set_trace()
        current_node: Node = root_node
        state = root_node.state._replace()
        print(i)

        # Select
        while not current_node.unexplored and current_node.children:  # fully expanded, non-terminal
            current_node = current_node.select_child()
            state = get_next_state(state, current_node.action)

        # Expand
        if current_node.unexplored:
            action = current_node.get_random_action()
            state = get_next_state(state, action)
            current_node = current_node.add_child(action, state)

        # Simulate
        while check_victory(state) is None:
            state = get_next_state(state, random.choice(get_actions(state)))
        
        # typing workaround, currently no good way to unwrap an optional type
        if check_victory(state) == (1.0, 0.0):
            result = (1.0, 0.0)
        elif check_victory(state) == (0.0, 1.0):
            result = (0.0, 1.0)
        else:
            result = (0.5, 0.5)

        # Backpropagate
        while current_node is not None:
            current_node.update_node(result)
            current_node = current_node.parent

    return sorted(root_node.children, key = lambda x: x.visits)[-1].action
