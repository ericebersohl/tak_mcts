from typing import Dict, List, Union, NamedTuple, Tuple

from .types import Action, Move, Place, State
from .enums import Piece, Color

def validate_move(state: State, action: Action, debug: bool = False) -> bool:
    if isinstance(action, Move):

        # variables
        row_s, col_s = action.start_coord[0], action.start_coord[1]
        row_e, col_e = action.end_coord[0], action.end_coord[1]
        delta_row, delta_col = row_e - row_s, col_e - col_s
        num_steps = delta_row + delta_col
        board = state.board
        standing = [Piece.BLACK_STANDING, Piece.WHITE_STANDING]

        # valid coordinates
        if not 0 <= row_s < 4 or not 0 <= col_s < 4:
            if debug: print(f'Invalid starting coordinate: ( {row_s} , {col_s} ).')
            return False
        if not 0 <= row_e < 4 or not 0 <= col_e < 4:
            if debug: print(f'Invalid ending coordinate: ( {row_e} , {col_e} ).')
            return False
        
        start_square = state.board[row_s][col_s]

        # player has control
        if len(start_square) == 0 or start_square[-1].value != state.to_move:
            if debug: print(f'Player does not have control of ( {row_s} , {col_s} ).')
            return False

        # stack size limit
        if action.carry_size > 4:
            if debug: print(f'Carry size greater than global max: {action.carry_size}')
            return False
        
        # actual stack size
        if action.carry_size > len(start_square):
            if debug: print(f'Carry size greater than square stack size: {action.carry_size} > {len(start_square)}.')
            return False

        # valid direction
        if delta_row != 0 and delta_col != 0:
            if debug: print(f'Movement is neither horizontal nor vertical.  E - S = ( {delta_row} , {delta_col} ).')
            return False
        elif delta_row == delta_col == 0:
            if debug: print(f'Start and end coordinates are the same. S: {action.start_coord}, E: {action.end_coord}.')
            return False
        
        # valid drop list
        if not 0 < abs(num_steps) < 4:
            if debug: print(f'Drop list length out of range. L: {num_steps}.')
            return False
        
        if len(action.drop_list) > abs(num_steps):
            if debug: print(f'Drop list too long. L: {action.drop_list}.')
            return False

        if len(action.drop_list) < abs(num_steps):
            if debug: print(f'Drop list too short. L {action.drop_list}.')
            return False

        if sum(action.drop_list) != action.carry_size:
            if debug: print(f'Drop list and carry size do not agree. DL: {action.drop_list}, CS: {action.carry_size}.')
            return False
        
        for drop in action.drop_list:
            if drop < 1:
                if debug: print(f'Drop list has nonpositive entry: {drop}.')
                return False

        # movement blocked by walls
        if delta_row == 0:
            if delta_col > 0:
                for step in range(1, num_steps + 1):
                    # print(step, num_steps)
                    # print(board[row_s][col_s + step])
                    if len(board[row_s][col_s + step]) > 0 and board[row_s][col_s + step][-1] in standing:
                        if debug: print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False
            else:  # delta_col < 0:
                for step in range(-1, num_steps - 1, -1):
                    if len(board[row_s][col_s + step]) > 0 and board[row_s][col_s + step][-1] in standing:
                        if debug: print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False
        else:  # delta_col == 0:
            if delta_row > 0:
                for step in range(1, num_steps + 1):
                    if len(board[row_s + step][col_s]) > 0 and board[row_s + step][col_s][-1] in standing:
                        if debug: print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False
            else:  # delta_row < 0:
                for step in range(-1, num_steps - 1, -1):
                    if len(board[row_s + step][col_s]) > 0 and board[row_s + step][col_s][-1] in standing:
                        if debug: print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False

    else:  # isinstance(action, Place):
        row, col = action.coord[0], action.coord[1]
        board = state.board

        # bad coord
        if not 0 <= row < 4 or not 0 <= col < 4:
            if debug: print(f'Coordinate out of bounds: ( {row} , {col} ).')
            return False

        # place occupied
        if len(board[row][col]) != 0:
            if debug: print(f'Square already occupied: ( {row} , {col} ).')
            return False

        # colors agree
        if state.to_move != action.piece.value:
            if debug: print(f'Colors do not match: {state.to_move} vs {action.piece.value}.')
            return False
    
    return True

def get_next_state(state: State, action: Action) -> State:
    pass

def get_actions(state: Dict) -> List[Action]:
    pass

def simulate(state: Dict) -> bool:
    pass

def check_victory(state: Dict) -> bool:
    pass