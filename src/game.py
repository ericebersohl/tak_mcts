"""Functions for running and simulating a Tak game.

This module contains five functions:
    validate_action(state, action) -> bool
    get_next_state(state, action) -> State
    get_actions(state) -> List[Action]
    check_victory(state) -> Union[None, Tuple[float, float]]
    simulate(state) -> Tuple[float, float]

    Validate_action returns true if the proposed action is valid for the given state.
    Get_next_state returns the new (immutable) state that results from applying the passed action
    to the passed state.  Get_actions returns a list of all possible actions for a given state.
    Check_victory if the state is terminal, returns a tuple indicating which player won.
    Simulate runs a game from the current state to an end state choosing all actions randomly.
    This is used for the standard implementation of a Monte-Carlo Tree Search algorithm.
"""
from typing import List, Union, Tuple
from copy import deepcopy

from .types import Action, Move, Place, State
from .enums import Piece, Color
from .utils import split_stack, get_drop_lists, get_path

def validate_action(state: State, action: Action, debug: bool = False) -> bool:
    """Validates proposed action for the given state.

    The various ways in which a move can be invalid are outlined in the Tak rules (available
    online).  If debug is True, then each time the function returns False it will give the specific
    reason the action failed.

    Args:
        state: An immutable State object (NamedTuple) containing board state information.
        action: An immutable Action object (NamedTuple) containing the action information.
        debug: A flag for printing which case failed for invalid actions.

    Returns:
        A bool.  True if the action is valid and False if it is not.
    """
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
            if debug:
                print(f'Invalid starting coordinate: ( {row_s} , {col_s} ).')
            return False
        if not 0 <= row_e < 4 or not 0 <= col_e < 4:
            if debug:
                print(f'Invalid ending coordinate: ( {row_e} , {col_e} ).')
            return False

        start_square = state.board[row_s][col_s]

        # player has control
        if not start_square or start_square[-1].value['color'] != state.to_move:
            if debug:
                print(f'Player {state.to_move.value} does not have control of ({row_s}, {col_s}).')
            return False

        # stack size limit
        if action.carry_size > 4:
            if debug:
                print(f'Carry size greater than global max: {action.carry_size}')
            return False

        # actual stack size
        if action.carry_size > len(start_square):
            if debug:
                print(f'Carry size greater than square stack size: \
                              {action.carry_size} > {len(start_square)}.')
            return False

        # valid direction
        if delta_row != 0 and delta_col != 0:
            if debug:
                print(f'Movement is neither horizontal nor vertical. \
                              E - S = ( {delta_row} , {delta_col} ).')
            return False
        if delta_row == delta_col == 0:
            if debug:
                print(f'Start and end coordinates are the same. \
                              S: {action.start_coord}, E: {action.end_coord}.')
            return False

        # valid drop list
        if not 0 < abs(num_steps) < 4:
            if debug:
                print(f'Drop list length out of range. L: {num_steps}.')
            return False

        if len(action.drop_list) > abs(num_steps):
            if debug:
                print(f'Drop list too long. L: {action.drop_list}.')
            return False

        if len(action.drop_list) < abs(num_steps):
            if debug:
                print(f'Drop list too short. L {action.drop_list}.')
            return False

        if sum(action.drop_list) != action.carry_size:
            if debug:
                print(f'Drop list and carry size do not agree. \
                              DL: {action.drop_list}, CS: {action.carry_size}.')
            return False

        for drop in action.drop_list:
            if drop < 1:
                if debug:
                    print(f'Drop list has nonpositive entry: {drop}.')
                return False

        # movement blocked by walls
        if delta_row == 0:
            if delta_col > 0:
                for step in range(1, num_steps + 1):
                    if board[row_s][col_s + step] and board[row_s][col_s + step][-1] in standing:
                        if debug:
                            print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False
            else:  # delta_col < 0:
                for step in range(-1, num_steps - 1, -1):
                    if board[row_s][col_s + step] and board[row_s][col_s + step][-1] in standing:
                        if debug:
                            print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False
        else:  # delta_col == 0:
            if delta_row > 0:
                for step in range(1, num_steps + 1):
                    if board[row_s + step][col_s] and board[row_s + step][col_s][-1] in standing:
                        if debug:
                            print(f'Encountered standing wall at ( {row_s} , {col_s + step} )')
                        return False
            else:  # delta_row < 0:
                for step in range(-1, num_steps - 1, -1):
                    if (board[row_s + step][col_s] and
                            board[row_s + step][col_s][-1] in standing):
                        if debug:
                            print(f'Encountered standing wall \
                                          at ( {row_s} , {col_s + step} )')
                        return False

    else:  # isinstance(action, Place):
        row, col = action.coord[0], action.coord[1]
        board = state.board

        # bad coord
        if not 0 <= row < 4 or not 0 <= col < 4:
            if debug:
                print(f'Coordinate out of bounds: ( {row} , {col} ).')
            return False

        # place occupied
        if board[row][col]:
            if debug:
                print(f'Square already occupied: ( {row} , {col} ).')
            return False

        # colors agree
        piece_color = action.piece.value['color']
        if state.to_move != piece_color:
            if debug:
                print(f'Colors do not match: {state.to_move} vs {piece_color}.')
            return False

    return True

def get_next_state(passed_state: State, action: Action) -> State:
    """
    Returns the State that results from applying the passed action to the passed State.

    Args:
        state: An immutable State object (NamedTuple) containing board state information.
        action: An immutable Action object (NamedTuple) containing the action information.

    Returns:
        A State type (see types.py) which is implemented as a NamedTuple with the following
        attributes:
            to_move: the Color of the player that moves next
            black_stones: the number of stones the black player has remaining
            white_stones: the number of stones the white player has remaining
            board: a 3D list of Pieces

    Raises:
        RuntimeError: Occurs when an invalid action is passed to the function.
    """
    state = deepcopy(passed_state)

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
            direction = (row_end - row) // len(action.drop_list)
            for step in range(1, len(action.drop_list) + 1):
                drop = moved[:action.drop_list[step - 1]]
                del moved[:action.drop_list[step - 1]]
                board[row + (step * direction)][col].extend(drop)
        else:
            direction = (col_end - col) // len(action.drop_list)
            for step in range(1, len(action.drop_list) + 1):
                drop = moved[:action.drop_list[step - 1]]
                del moved[:action.drop_list[step - 1]]
                board[row][col + (step * direction)].extend(drop)


    return State(
        to_move=to_move,
        white_stones=white_stones,
        black_stones=black_stones,
        board=board,
    )

def get_actions(state: State) -> List[Action]:
    """Returns a list of all possible actions available in the current board state.

    Args:
        state: An immutable State object (NamedTuple) containing board state information.

    Returns:
        A list of Actions (see types.py) that are immutable NamedTuples.

    Raises:
        RuntimeError: An error occurs when this function is called from a terminal state.
    """
    action_list: List[Action] = []

    if state.white_stones == 0 or state.black_stones == 0:
        raise RuntimeError(f"get_actions called when a player has no stones {state}.")

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
            if not board[row][col]:
                action_list.extend([
                    Place(coord=(row, col), piece=available_pieces[0]),
                    Place(coord=(row, col), piece=available_pieces[1]),
                ])

            # possible movements
            elif board[row][col] and board[row][col][-1].value['color'] == state.to_move:
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
                                    start_coord=(row, col),
                                    end_coord=(
                                        row + direction[0] * moves, col + direction[1] * moves
                                    ),
                                    carry_size=carry,
                                    drop_list=drop,
                                ))

    return [action for action in action_list if validate_action(state, action)]

def check_victory(state: State) -> Union[None, Tuple[float, float]]:
    """Determines whether the passed state is terminal.

    This function determines if the game has reached a terminal state.
    A game can end in three ways:
        1) if either player has built a road from one side of the board to the opposite side,
        2) if there are no more open spaces on the board
        3) if one player is out of stones

    Args:
        state: An immutable State object (NamedTuple) containing board state information.

    Returns:
        A tuple of floats containing the score for each player: (Black, White).  If the state
        is not terminal, returns None.
    """
    board = state.board
    open_squares = 0

    for row in range(len(board)):
        for col in range(len(board[row])):
            if not board[row][col]:
                open_squares += 1

    # count flat pieces
    if state.white_stones < 1 or state.black_stones < 1 or open_squares == 0:
        white_flats, black_flats = 0, 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] and board[row][col][-1] == Piece.WHITE_FLAT:
                    white_flats += 1
                elif board[row][col] and board[row][col][-1] == Piece.BLACK_FLAT:
                    black_flats += 1

        if white_flats == black_flats:
            return (0.5, 0.5)
        if white_flats > black_flats:
            return (0.0, 1.0)
        if white_flats < black_flats:
            return (1.0, 0.0)

    paths = get_path(state)
    if paths == (True, False):
        return (1.0, 0.0)
    if paths == (False, True):
        return (0.0, 1.0)
    if paths == (True, True) and state.to_move == Color.BLACK:
        return (0.0, 1.0)
    if paths == (True, True) and state.to_move == Color.WHITE:
        return (1.0, 0.0)

    return None
