"""Class for Nodes in a MCTS tree.

The Node class contains several methods:
    ...

Adapted from: http://mcts.ai/code/python.html
"""

from __future__ import annotations  # required in Python 3.7
from typing import Union, List, Tuple
from math import sqrt, log
import random

from .types import Action, State
from .enums import Color
from .game import get_actions, get_next_state
from .utils import get_action_string

class Node:
    def __init__(self, action: Union[Action, None], state: State, parent: Union[Node, None]):
        self._action = action
        self._state = state
        self._parent = parent
        self._children: List[Node] = []
        self._visits = 0.0
        self._wins = 0.0
        self._unexplored: List[Action] = get_actions(self._state)

    def calculate_uct(self, child_wins: int, child_visits: int, weight: float = 1.0) -> float:
        """Returns a float that represents its attractiveness for MCTS exploration
        
        Note that if the node's _visits property is 0, float("inf") is returned.

        Args:
            child_wins: the number of times the child node (or one of its children) has won.
            child_visits: the total number of visits to the child node.
            weight: an optional additional weighting factor

        Raises:
            ValueError:
                child_visits < 1 
                self._visits < child_visits
                child_wins > child_visits
        """
        if child_visits < 0:
            raise ValueError(f"child_visits cannot be less than zero: {child_visits}.")

        if self._visits < child_visits:
            raise ValueError(f"child_visits cannot be greater than parent._visits:\
                               {child_visits} > {self._visits}.")
        
        if child_wins > child_visits:
            raise ValueError(f"child_visits cannot be greater than child_wins:\
                               {child_visits} > {child_wins}")

        if child_visits == 0:
            return float("inf")

        win_loss = child_wins / child_visits
        weight = 2 * weight
        uct = sqrt(2*log(self._visits)/child_visits)

        return win_loss + weight * uct

    def select_child(self) -> Node:
        """Returns the child node with the highest UCT weight.

        Uses the calculate_uct function on each Node in self._children.
        """
        best_child: Node = sorted(
            self._children, key = lambda child: self.calculate_uct(child.wins, child.visits)
        )[-1]
        return best_child

    def add_child(self, add_action: Action, add_state: State) -> Node:
        """Creates and returns a new node taking an action from _unexplored.

        Args:
            action: an action taken from the _unexplored list of possible actions.

        Returns:
            The new node that is created and added to the list of children.
        """
        new_node = Node(add_action, add_state, self)
        self._unexplored.remove(add_action)
        self._children.append(new_node)
        return new_node

    def update_node(self, result: Tuple[float, float]) -> None:
        """Updates the _wins and _visits properties of the node.

        Args:
            result: a tuple of floats in range [0.0, 1.0] representing the result of a simulated
            game.
        """
        self._visits += 1
        if self._state.to_move == Color.BLACK:
            self._wins += result[0]
        else:
            self._wins += result[1]

    def get_random_action(self) -> Action:
        """Returns a random member of _unexplored."""
        return random.choice(self._unexplored)
    
    @property
    def wins(self):
        return self._wins

    @property
    def visits(self):
        return self._visits

    @property
    def unexplored(self):
        return self._unexplored

    @property
    def state(self):
        return self._state
    
    @property
    def children(self):
        return self._children
    
    @property
    def parent(self):
        return self._parent

    @property
    def action(self):
        return self._action

    def __repr__(self):
        if self._action is not None:
            action_str = get_action_string(self._action)
        else:
            action_str = "None"
        return f"[A: {action_str}  W/V: {self._wins}/{self._visits} U: {len(self._unexplored)}]"

    def tree_to_string(self, indent: int) -> str:
        string = self.indent_string(indent) + str(self)
        for child in self._children:
            string += child.tree_to_string(indent + 1)
        return string
    
    def indent_string(self, indent: int) -> str:
        string = "\n"
        for _ in range(1, indent + 1):
            string += "| "
        return string
