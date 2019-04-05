from typing import List, NamedTuple, Tuple, Union 
from .enums import Color, Piece

class Move(NamedTuple):
    start_coord: Tuple[int, int]
    end_coord: Tuple[int, int]
    carry_size: int
    drop_list: List[int]

class Place(NamedTuple):
    coord: Tuple[int, int]
    piece: Piece

class State(NamedTuple):
    to_move: Color
    white_stones: int
    black_stones: int
    board: List[List[List[Piece]]]

Action = Union[Move, Place]