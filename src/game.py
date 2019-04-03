from typing import Dict, List, Union, NamedTuple, Tuple
from utils import initial_state
from collections import namedtuple
from enums import Piece, Color
from utils import InvalidMoveError

class Move(NamedTuple):
    start_coord: Tuple[int, int]
    end_coord: Tuple[int, int]
    carry_limit: int
    drop_list: List[int]

class Place(NamedTuple):
    coord: Tuple[int, int]
    piece: Piece

Action = Union[Move, Place]

def next(state: Dict, action: Action) -> Dict:
    board = state['board']
    
    if state['to_move'] == Color.BLACK:
        to_move = (Piece.BLACK_FLAT, Piece.BLACK_STANDING)
    else:
        to_move = (Piece.WHITE_FLAT, Piece.WHITE_STANDING)

    walls = (Piece.BLACK_STANDING, Piece.WHITE_STANDING)

    if isinstance(action, Move):
        
        #
        # Validity Checks
        #

        start: Tuple[int, int] = action.start_coord
        end: Tuple[int, int] = action.end_coord

        # Control of Start Coord
        if not board[start[0]][start[1]][-1] in to_move:
            raise InvalidMoveError(f"Player does not have control of {start}.")
        
        # Stack Size Under Limit
        if action.carry_limit > 4:
            raise InvalidMoveError(f"Cannot move more than 4 stones.")

        # Valid Coords
        if start[0] < 0 or start[0] > 4 or start[1] < 0 or start[1] > 4:
            raise InvalidMoveError(f"Start coordinate invalid: {start}.")
        if end[0] < 0 or end[0] > 4 or end[1] < 0 or end[1] > 4:
            raise InvalidMoveError(f"End coordinate invalid: {end}.")

        # Valid Direction
        if not (start[0] - end[0] == 0 or start[1] - end[1] == 0):
            raise InvalidMoveError(f"Invalid direction.  Start: {start}, End: {end}")

        # Valid Drop List
        if len(action.drop_list) < 1:
            raise InvalidMoveError(f"Empty drop list.")

        if sum(action.drop_list) != action.carry_limit:
            raise InvalidMoveError(f"Drop list doesn't equal stack size.")
        
        for drop in action.drop_list:
            if drop < 1:
                raise InvalidMoveError(f"Player must drop at least one stone: {action['drop_list']}.")

        # No Standing Stones in Path (or at end)
        if start[0] - end[0] == 0:
            if start[1] - end[1] > 0:
                for step in range(start[1] - end[1]):
                    if board[start[0]][start[1] + step][-1] in walls:
                        raise InvalidMoveError(f"Found a wall in path: {start[0]}, {start[1] + step}.")
            elif start[1] - end[1] < 0:
                for step in range(0, start[1] - end[1], -1):
                    if board[start[0]][start[1] + step][-1] in walls:
                        raise InvalidMoveError(f"Found a wall in path: {start[0]}, {start[1] + step}.")
            else:
                raise InvalidMoveError(f"Start and End are the same: {start}, {end}.")
        else:
            if start[0] - end[0] > 0:
                for step in range(start[0] - end[0]):
                    if board[start[0] + step][start[1]][-1] in walls:
                        raise InvalidMoveError(f"Found a wall in path: {start[0]}, {start[1] + step}.")
            elif start[0] - end[0] < 0:
                for step in range(0, start[0] - end[0], -1):
                    if board[start[0] + step][start[1]][-1] in walls:
                        raise InvalidMoveError(f"Found a wall in path: {start[0]}, {start[1] + step}.")
            else:
                raise InvalidMoveError(f"Start and End are the same: {start}, {end}.")

        # make changes
    else: # Place
        pass
    
    return {}

def get_actions(state: Dict) -> List[Action]:
    pass

def simulate(state: Dict) -> bool:
    pass

def check_victory(state: Dict) -> bool:
    pass