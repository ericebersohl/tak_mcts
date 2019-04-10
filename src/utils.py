"""Utility functions for the game-driving functions.

This module defines several utility functions that are used by game.py so that that module didn't
become unbearably long.
"""
from typing import List, Tuple
from collections import deque
from itertools import permutations

from .enums import Color, Piece
from .types import State

def split_stack(stack: List, num_removed: int) -> Tuple[List, List]:
    """Splits a list into two sub-lists.

    Args:
        stack: A List to be split
        num_removed: An int representing how many items to remove from the end.

    Returns:
        A tuple containing two lists.  The first list is the items remaining on the square, the
        second list is the items that have been picked up as part of a Move action.

    Raises:
        RuntimeError: Error raised if num_removed is less than 1 or greater than the length of the
        list.
    """
    if num_removed > len(stack) or num_removed < 1:
        raise RuntimeError("num_removed out of bounds")

    split_index = len(stack) - num_removed

    picked_up = stack[split_index:]
    remaining = stack[:split_index]

    return (remaining, picked_up)

def get_drop_lists(carry: int, moves: int) -> List[List[int]]:
    """Returns all possible drop lists for given carry_size and number of steps.

    Args:
        carry: An int representing the number of stones picked up.
        moves: An int representing the number of squares on which stones are dropped as part of a
            Move action.  Note that this does not include the start square.

    Returns:
        A list of lists.  Each inner list will be used as the drop_list attribute in a Move action.
        The outer list will contain a unique list for every possible permutation of the given sets
        of drops.
    """
    possible_drops = list(range(1, carry + 1))
    all_combinations = get_combinations(possible_drops, carry)
    combinations = [x for x in all_combinations if len(x) == moves]

    perms = []
    for combo in combinations:
        for perm in permutations(combo):
            perms.append(perm)

    solution = [list(x) for x in set(perms)]

    return solution

def get_combinations(candidates: List[int], target: int) -> List[List[int]]:
    """Returns a list of lists representing each possible set of drops.

    This function (and its recursive helper function) was adapted from
    https://wlcoding.blogspot.com/2015/03/combination-sum-i-ii.html.

    Args:
        candidates: A list of possible numbers of pieces to drop on a square.  Effectively, this
            arg is equivalent to range(1, carry_size + 1).
        target: The number of stones in the carry_size.  The number of dropped stones must equal the
            number of stones picked up.

    Returns:
        A list of lists of possible combinations.  Note that these lists do not contain every
        permutation of drops, merely every combination of valid ints that sums to the target value.
    """
    def get_combinations_rec(candidates, target, index, partial_sum, list_t, combinations) -> None:
        """A recursive helper function for get_combinations."""
        if partial_sum == target:
            combinations.append(list(list_t))
        for i in range(index, len(candidates)):
            if partial_sum + candidates[i] > target:
                break
            list_t.append(candidates[i])
            get_combinations_rec(
                candidates, target, i, partial_sum+candidates[i], list_t, combinations
            )
            list_t.pop()

    combinations: List = []
    get_combinations_rec(candidates, target, 0, 0, [], combinations)
    return combinations

def get_path(state: State) -> Tuple[bool, bool]:
    """Returns a tuple of booleans representing whether each player has completed a road.

    Args:
        state: A State object (defined in types.py) representing the current board state.

    Returns:
        A tuple of form (bool, bool).  The first bool will be True if the Black player has completed
        a road, and the second will be true if the White player has completed a road.
    """
    north = [(0, 0), (0, 1), (0, 2), (0, 3)]
    east = [(0, 3), (1, 3), (2, 3), (3, 3)]
    south = [(3, 0), (3, 1), (3, 2), (3, 3)]
    west = [(0, 0), (1, 0), (2, 0), (3, 0)]

    black, white = False, False

    for start in north:
        if bfs(state.board, start, south, Color.BLACK):
            black = True
        if bfs(state.board, start, south, Color.WHITE):
            white = True

    for start in east:
        if bfs(state.board, start, west, Color.BLACK):
            black = True
        if bfs(state.board, start, west, Color.WHITE):
            white = True

    return (black, white)

def bfs(board: List[List[List[Piece]]], start: Tuple[int, int],
        goal: List[Tuple[int, int]], color: Color) -> bool:
    """Runs Breadth First Search on the board.

    Args:
        board: A 3D list of Pieces representing the current board state.
        start: An int, int tuple containing the row and col of the starting square.
        goal: A list of int, int tuples representing the four possible end squares for a road.
        color: the Color of piece to test.

    Returns:
        A bool that is True if there is a path from start to goal.
    """

    if not get_controlled(board, start, color):
        return False

    queue = deque([[start]])
    visited = set([start])
    while queue:
        path = queue.popleft()
        row, col = path[-1]
        if (row, col) in goal:
            return True
        for row2, col2 in ((row+1, col), (row-1, col), (row, col+1), (row, col-1)):
            if (0 <= row2 <= 3 and 0 <= col2 <= 3 and get_controlled(board, (row2, col2), color) and
                    (row2, col2) not in visited and board[row2][col2][-1].value['type'] == 'flat'):

                queue.append(path + [(row2, col2)])
                visited.add((row2, col2))
    return False

def get_controlled(board: List[List[List[Piece]]], coord: Tuple[int, int], color: Color) -> bool:
    """Returns true if the top piece on the square in question is of the player's Color.

    Args:
        board: A 3D list of Pieces representing the board state.
        coord: An int, int tuple containing the coordinates of the square to be tested.
        color: The color of the Player.
    """
    row, col = coord
    square: List[Piece] = board[row][col]

    return bool(square and square[-1].value['color'] == color)

def print_state(state: State) -> None:
    """Prints a State object.

    Each Piece is represented as a string of length 2:
        BLACK_FLAT      -> 'bf'
        BLACK_STANDING  -> 'bs'
        WHITE_FLAT      -> 'wf'
        WHITE_STANDING  -> 'ws'

    Each square is represented in brackets and has a fixed width.  If the square has fewer than
    three stones on it, all stones will be represented with the piece on top being the farthest to
    the right.  If the square has greater than three stones, the top two stones will still be
    shown, but the number of remaining stones will be represented as an int in brackets.
    """
    def get_list_str(square: List[Piece]) -> str:
        """Helper function to format a list for print_state"""
        string = [x.value['str'] for x in square]
        if not square:
            return f'[          ]'
        if len(square) == 1:
            return f'[        {string[-1]}]'
        if len(square) == 2:
            return f'[    {string[-2]}, {string[-1]}]'
        if len(square) == 3:
            return f'[{string[-3]}, {string[-2]}, {string[-1]}]'

        return f'[({len(square)-2:02d}){string[-2]}, {string[-1]}]'

    print('To Move:\t', state.to_move.value, sep='')
    print('White Stones:\t', state.white_stones, sep='')
    print('Black Stones:\t', state.black_stones, sep='')
    print('Board:')

    for row in range(4):
        print(f'{get_list_str(state.board[row][0])} {get_list_str(state.board[row][1])}\
                {get_list_str(state.board[row][2])} {get_list_str(state.board[row][3])}')
