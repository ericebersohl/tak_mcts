from typing import List, Union, Tuple
from collections import deque
from itertools import permutations

from .enums import Color, Piece
from .types import State

def split_stack(stack: List, num_removed: int) -> Tuple[List, List]:
    if num_removed > len(stack) or num_removed < 1:
        raise RuntimeError("num_removed out of bounds")
    
    split_index = len(stack) - num_removed

    picked_up = stack[split_index:]
    remaining = stack[:split_index]

    return ( remaining, picked_up )

def get_combinations(candidates: List[int], target: int) -> List[List[int]]:
    combinations: List = []
    get_combinations_rec(candidates, target, 0, 0, [], combinations)
    return combinations
    
def get_combinations_rec(candidates, target, index, sum, listT, combinations) -> None:
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

def get_drop_lists(carry: int, moves: int) -> List[List[int]]:
    possible_drops = list(range(1, carry + 1))
    all_combinations = get_combinations(possible_drops, carry)
    combinations = [x for x in all_combinations if len(x) == moves]

    perms = []
    for c in combinations:
        for p in permutations(c):
            perms.append(p)

    solution = [list(x) for x in set(perms)]

    return solution

def get_path(state: State) -> Tuple[bool, bool]:
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

def bfs(board: List[List[List[Piece]]], start: Tuple[int, int], goal: List[Tuple[int, int]], color: Color) -> bool:
    
    if not get_controlled(board, start, color):
        return False
    
    q = deque([[start]])
    visited = set([start])
    while q:
        path = q.popleft()
        row, col = path[-1]
        if (row, col) in goal:
            return True
        for row2, col2 in ((row+1, col), (row-1, col), (row, col+1), (row, col-1)):
            if (0 <= row2 <= 3 and 0 <= col2 <= 3 and get_controlled(board, (row2, col2), color)
                and (row2, col2) not in visited and board[row2][col2][-1].value['type'] == 'flat'):

                q.append(path + [(row2, col2)])
                visited.add((row2, col2))
    return False

def get_controlled(board: List[List[List[Piece]]], coord: Tuple[int, int], color: Color) -> bool:
    row, col = coord
    square: List[Piece] = board[row][col]
    if len(square) > 0 and square[-1].value['color'] == color:
        return True
    else:
        return False