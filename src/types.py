"""Immutable types for board state and actions in Tak.

This module defines a NamedTuple representation of the board state and a NamedTuple representation
for each kind of action a player may take: either move or place.  Finally, the module defines the
union type Action for ease of use in other modules.
"""
from typing import List, NamedTuple, Tuple, Union
from .enums import Color, Piece

class Move(NamedTuple):
    """Defines the Move type.

    Attributes:
        start_coord: An int, int tuple that defines the originating square
        end_coord: An int, int tuple that defines the last square on which a piece is placed during
            a move.
        carry_size: An int which defines how many stones are picked up from the start_coord.
        drop_list: A list of ints which defines how many stones are dropped at each step
            during the move.  Note that no stones are dropped on the starting square.
    """
    start_coord: Tuple[int, int]
    end_coord: Tuple[int, int]
    carry_size: int
    drop_list: List[int]

class Place(NamedTuple):
    """Defines the Place type.

    Attributes:
        coord: An int, int tuple that defines the empty square in which a piece should be placed.
        piece: A Piece (see enums.py) to be placed in the square.
    """
    coord: Tuple[int, int]
    piece: Piece

class State(NamedTuple):
    """Defines the State type.

    Attributes:
        to_move: The Color of the player who is to move next.
        black_stones: An int representing the number of stones the Black player has remaining.
        white_stones: An int representing the number of stones the White player has remaining.
        board: A 3D list of Pieces (see enums.py) representing the board state.
    """
    to_move: Color
    black_stones: int
    white_stones: int
    board: List[List[List[Piece]]]

Action = Union[Move, Place]

default_state = State(
    to_move = Color.BLACK,
    black_stones = 15,
    white_stones = 15,
    board = [
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
    ]
)