"""Class for Nodes in a MCTS tree.

A node represents a specific action taken in the game being simulated.  It stores a record of wins
and attempts that pass through that action, and it uses that information to give itself a weight
that signifies its attractiveness for exploration.

The Node class contains several methods:
    calculate_uct: calculates the "exploration-attractiveness" of the node based on its wins and
    visits.
    select_child: returns the child with the highest UCT weight
    add_child: adds a child node in the tree
    update_node: updates the wins and visits properties of the node given a result from a simulated
    game.
    get_random_action: returns a random action from the list of unexplored actions.
    tree_to_string: prints a representation of the subtree that has this node as its root.

Adapted from: http://mcts.ai/code/python.html
"""

# from __future__ import annotations  # required in Python 3.7
from typing import Union, List, Tuple, Optional
from math import sqrt, log
import random

from .types import Action, State
from .enums import Color
from .game import get_actions, get_next_state, check_victory
from .utils import get_action_string, calculate_uct

class Node:
    """Represents a node in a Monte-Carlo Tree Search."""
    def __init__(self, action: Union[Action, None], state: State, parent, weight: float = 2.0):
        """Initializes a node.  Gets a list of possible actions from this state."""
        self._action = action
        self._state = state
        self._parent = parent
        self._children: List = []
        self._visits: int = 0
        self._wins: float = 0
        self._weight = weight
        self._unexplored: List[Action] = get_actions(self._state)

    def select_child(self):
        """Returns the child node with the highest UCT weight.

        Uses the calculate_uct function on each Node in self._children.
        """
        best_child = sorted(
            self._children, key=lambda child: calculate_uct(child.wins, child.visits, self._visits, self._weight)
        )[-1]
        return best_child

    def select_child_decisive(self):
        """Returns the child that leads to immediate victory or, if no such child exists, the child
        with the highest UCT1 value.

        Uses the calculate_uct function on each Node in self._children.
        """
        for child in self._children:
            decisive: Optional[Tuple] = check_victory(get_next_state(self._state, child.action))
            if (decisive == (1.0, 0.0) and self._state.to_move == Color.BLACK or
                    decisive == (0.0, 1.0) and self._state.to_move == Color.WHITE):
                return child

        best_child = sorted(
            self._children, key=lambda child: calculate_uct(child.wins, child.visits, self._visits, self._weight)
        )[-1]
        return best_child

    def add_child(self, add_action: Action, add_state: State):
        """Creates and returns a new node taking an action from _unexplored.

        Args:
            action: an action taken from the _unexplored list of possible actions.

        Returns:
            The new node that is created and added to the list of children.
        """
        new_node = Node(add_action, add_state, self, self._weight)
        self._unexplored.remove(add_action)
        self._children.append(new_node)
        return new_node

    def update_node(self, result: Tuple[float, float], simulations: int = 1) -> None:
        """Updates the _wins and _visits properties of the node.

        Args:
            result: a tuple of floats in range [0.0, 1.0] representing the result of a simulated
            game.
            simulations: an int indicating how many simulations are being updated.
        """
        self._visits += simulations
        if self._state.to_move == Color.BLACK:
            self._wins += result[0]
        else:
            self._wins += result[1]

    def get_random_action(self) -> Action:
        """Returns a random member of _unexplored."""
        return random.choice(self._unexplored)

    def __repr__(self):
        if self._action is not None:
            action_str = get_action_string(self._action)
        else:
            action_str = "None"
        return f"[A: {action_str}  W/V: {self._wins}/{self._visits} U: {len(self._unexplored)}]"

    def tree_to_string(self, indent: int) -> str:
        """Returns a string representation of the tree.

        Args:
            indent: an integer representing the number of indents to use.
        """
        string = self.indent_string(indent) + str(self)
        for child in self._children:
            string += child.tree_to_string(indent + 1)
        return string

    def indent_string(self, indent: int) -> str:
        """Helper method for tree_to_string."""
        string = "\n"
        for _ in range(1, indent + 1):
            string += "| "
        return string

    @property
    def wins(self):
        """Property definition for _wins."""
        return self._wins

    @property
    def visits(self):
        """Property definition for _visits."""
        return self._visits

    @property
    def unexplored(self):
        """Property definition for _unexplored."""
        return self._unexplored

    @property
    def state(self):
        """Property definition for _state."""
        return self._state

    @property
    def children(self):
        """Property definition for _children."""
        return self._children

    @property
    def parent(self):
        """Property definition for _parent."""
        return self._parent

    @property
    def action(self):
        """Property definition for _action."""
        return self._action
