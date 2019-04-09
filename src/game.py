from typing import Dict, List, Union, NamedTuple, Tuple
from itertools import permutations

from .types import Action, Move, Place, State
from .enums import Piece, Color

def validate_action(state: State, action: Action, debug: bool = False) -> bool:
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
        if len(start_square) == 0 or start_square[-1].value['color'] != state.to_move:
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
        piece_color = action.piece.value['color']
        if state.to_move != piece_color:
            if debug: print(f'Colors do not match: {state.to_move} vs {piece_color}.')
            return False
    
    return True

def get_next_state(state: State, action: Action) -> State:    
    if not validate_action(state, action):
        raise RuntimeError('Action failed validation.')
    
    # color
    if state.to_move == Color.BLACK:
        to_move = Color.WHITE
    else:
        to_move = Color.BLACK

    # stones
    if isinstance(action, Place):
        if state.to_move == Color.BLACK:
            white_stones = state.white_stones
            black_stones = state.black_stones - 1
        else: # to_move == WHITE
            white_stones = state.white_stones - 1
            black_stones = state.black_stones
    else:
        white_stones, black_stones = state.white_stones, state.black_stones

    # board
    board: List[List[List[Piece]]] = state.board
    
    if isinstance(action, Place):
        board[action.coord[0]][action.coord[1]].append(action.piece)
    else:
        row, col = action.start_coord[0], action.start_coord[1]
        row_end, col_end = action.end_coord[0], action.end_coord[1]

        # split the stack
        stack: List[Piece] = board[row][col]
        remain, moved = split_stack(stack, action.carry_size)
        board[row][col] = remain

        # get direction, move stones
        if abs(row_end - row) > abs(col_end - col):
            direction = ( row_end - row ) // len(action.drop_list)
            for step in range(1, len(action.drop_list) + 1):
                drop = moved[:action.drop_list[step - 1]]
                del moved[:action.drop_list[step - 1]]
                board[row + (step * direction)][col].extend(drop)
        else:
            direction = ( col_end - col ) // len(action.drop_list)
            for step in range(1, len(action.drop_list) + 1):
                drop = moved[:action.drop_list[step - 1]]
                del moved[:action.drop_list[step - 1]]
                board[row][col + (step * direction)].extend(drop)


    return State(
        to_move = to_move,
        white_stones = white_stones,
        black_stones = black_stones,
        board = board,
    )

def get_actions(state: State) -> List[Action]:
    action_list: List[Action] = []
    
    if state.white_stones == 0 or state.black_stones == 0:
        raise RuntimeError("get_actions called when a player has no stones.")

    # append all possible actions
    board = state.board
    if state.to_move == Color.WHITE:
        available_pieces = [
            Piece.WHITE_FLAT,
            Piece.WHITE_STANDING,
        ]
    else:
        available_pieces = [
            Piece.BLACK_FLAT,
            Piece.BLACK_STANDING,
        ]

    for row in range(len(board)):
        for col in range(len(board[row])):
            
            # possible placements
            if len(board[row][col]) == 0:
                action_list.extend([
                    Place(coord = (row, col), piece = available_pieces[0]),
                    Place(coord = (row, col), piece = available_pieces[1]),
                ])

            # possible movements
            elif len(board[row][col]) > 0 and board[row][col][-1].value['color'] == state.to_move:
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                max_carry_size = min(4, len(board[row][col]))
                # directions
                for direction in directions:
                    # carry sizes
                    for carry in range(1, max_carry_size + 1):
                        # endpoints
                        for moves in range(1, carry + 1):
                            drop_lists = get_drop_lists(carry, moves)
                            # drop lists
                            for drop in drop_lists:
                                action_list.append(Move(
                                    start_coord = (row, col),
                                    end_coord = (row + direction[0] * moves, col + direction[1] * moves),
                                    carry_size = carry,
                                    drop_list = drop,
                                ))

    return [action for action in action_list if validate_action(state, action)]

def simulate(state: Dict) -> bool:
    pass

def check_victory(state: Dict) -> bool:
    pass

#
#   UTILITY
#

def split_stack(stack: List, num_removed: int) -> Tuple[List, List]:
    if num_removed > len(stack) or num_removed < 1:
        raise RuntimeError("num_removed out of bounds")
    
    split_index = len(stack) - num_removed

    picked_up = stack[split_index:]
    remaining = stack[:split_index]

    return ( remaining, picked_up )

def get_combinations(candidates: List[int], target: int):
    combinations: List = []
    get_combinations_rec(candidates, target, 0, 0, [], combinations)
    return combinations
    
def get_combinations_rec(candidates, target, index, sum, listT, combinations):
    """
    Adapted from https://wlcoding.blogspot.com/2015/03/combination-sum-i-ii.html
    """
    if sum == target:
        combinations.append(list(listT))
    for i in range(index,len(candidates)):
        if sum + candidates[i] > target:
            break
        listT.append(candidates[i])
        get_combinations_rec(candidates, target, i, sum+candidates[i], listT, combinations)
        listT.pop()

def get_drop_lists(carry: int, moves: int):
    possible_drops = list(range(1, carry + 1))
    all_combinations = get_combinations(possible_drops, carry)
    combinations = [x for x in all_combinations if len(x) == moves]

    perms = []
    for c in combinations:
        for p in permutations(c):
            perms.append(p)

    solution = [list(x) for x in set(perms)]

    return solution