"""Functions for Monte-Carlo Tree Searches.

TODO: add more info about what an mcts is.

There is currently only one version of MCTS which is the default.
"""
import random
from copy import deepcopy

from .node import Node
from .types import State, Action
from .game import get_next_state, check_victory, get_actions

def default_mcts(root: State, iterations: int, weight_factor: float = 2.0) -> Action:
    """Returns the most visited action from a MCTS with the given number of iterations.

    Args:
        root: a State NamedTuple that represents the current game state from which to simulate.
        iterations: the number of iterations to run before selecting an action.
    """
    root_node: Node = Node(action=None, state=root, parent=None, weight=weight_factor)

    for _ in range(iterations):
        current_node: Node = root_node
        state = deepcopy(root_node.state)

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

    return sorted(root_node.children, key=lambda x: x.visits)[-1].action

def decisive_move_mcts(root: State, iterations: int) -> Action:
    """Returns the most visited action from a MCTS with the given number of iterations.

    This function differs from default_mcts in that for each select step, it checks if a child is
    a decisive move (a move that leads immediately to victory).  If a child is decisive, it is
    returned, otherwise MCTS proceeds as normal.

    Args:
        root: a State NamedTuple that represents the starting state
        iterations: an int denoting the number of iterations to run the search.
    """
    root_node: Node = Node(action=None, state=root, parent=None)

    for _ in range(iterations):
        current_node: Node = root_node
        state: State = deepcopy(root_node.state)

        # Select
        while not current_node.unexplored and current_node.children:
            current_node = current_node.select_child_decisive()
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

        # backpropagate
        while current_node is not None:
            current_node.update_node(result)
            current_node = current_node.parent

    return sorted(root_node.children, key=lambda x: x.visits)[-1].action


def weighted_backpropagation_mcts(root: State, iterations: int) -> Action:
    """Returns the most visited action in a MCTS with the weighted backpropagation enhancement.

    Args:
        root: the state from which to search.
        iterations: the number of iterations to run before returning.
    """
    root_node: Node = Node(action=None, state=root, parent=None)

    for _ in range(iterations):
        current_node: Node = root_node
        state = deepcopy(root_node.state)
        depth = 1

        while not current_node.unexplored and current_node.children:
            current_node = current_node.select_child()
            depth += 1
            state = get_next_state(state, current_node.action)

        if current_node.unexplored:
            action = current_node.get_random_action()
            state = get_next_state(state, action)
            current_node = current_node.add_child(action, state)
            depth += 1

        while check_victory(state) is None:
            state = get_next_state(state, random.choice(get_actions(state)))

        weight_factor = 2**(depth-1)
        if check_victory(state) == (1.0, 0.0):
            result = (1.0 * weight_factor, 0.0)
        elif check_victory(state) == (0.0, 1.0):
            result = (0.0, 1.0 * weight_factor)
        else:
            result = (0.5 * weight_factor, 0.5 * weight_factor)

        while current_node is not None:
            current_node.update_node(result, weight_factor)
            current_node = current_node.parent

    return sorted(root_node.children, key=lambda x: x.visits)[-1].action

def multi_simulation_mcts(root: State, iterations: int, leaf_simulations: int = 3) -> Action:
    """Returns the most visited action from a MCTS with the given number of iterations.

    Args:
        root: the State from which the search starts.
        iterations: an int representing the number of iterations to perform.
        leaf_simulations: the number of simulations to run each time a new node is added to the
        tree.
    """
    root_node: Node = Node(action=None, state=root, parent=None)

    for _ in range(iterations//leaf_simulations):
        current_node: Node = root_node
        state = deepcopy(root_node.state)

        # Select
        while not current_node.unexplored and current_node.children:
            current_node = current_node.select_child()
            state = get_next_state(state, current_node.action)

        # Expand
        if current_node.unexplored:
            action = current_node.get_random_action()
            state = get_next_state(state, action)
            current_node = current_node.add_child(action, state)

        # Simulate
        result = (0.0, 0.0)
        for _ in range(leaf_simulations):
            sim_state = deepcopy(state)
            while check_victory(sim_state) is None:
                sim_state = get_next_state(sim_state, random.choice(get_actions(sim_state)))

            if check_victory(sim_state) == (1.0, 0.0):
                result = (result[0] + 1.0, result[1])
            elif check_victory(sim_state) == (0.0, 1.0):
                result = (result[0], result[1] + 1.0)
            else:
                result = (result[0] + 0.5, result[1] + 0.5)

        # Backpropagate
        while current_node is not None:
            current_node.update_node(result, leaf_simulations)
            current_node = current_node.parent

    return sorted(root_node.children, key=lambda x: x.visits)[-1].action
