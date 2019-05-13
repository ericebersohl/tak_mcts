"""
Defines functions to run a round-robin tournament among all four MCTS algorithms defined in
src/search.py.

As defined, the output .csv file should be placed in build/tournament.csv.  This script will NOT
overwrite previous data, it will simply add more lines a the end of the file.
"""
import csv
from typing import List, Tuple, Optional
from datetime import datetime

from src.game import get_next_state, check_victory
from src.types import get_default_state
from src.enums import Color
from src.search import default_mcts, decisive_move_mcts,\
    weighted_backpropagation_mcts, multi_simulation_mcts
from src.utils import pretty_time_delta

FUNCTIONS = [
    (default_mcts, 'def'),
    (decisive_move_mcts, 'dec'),
    (weighted_backpropagation_mcts, 'wbp'),
    (multi_simulation_mcts, 'msm'),
]

def tournament(funcs: List) -> None:
    """Runs a round-robin tournament among algorithms.

    Args:
        funcs: a list of tuples of the form (function, short_name)
    """
    for black in funcs:
        for white in funcs:
            record_result(black, white)

def record_result(player_1: Tuple, player_2: Tuple) -> None:
    """Writes the result of a game in the tournament to the csv file.

    Args:
        player_1, player_2: Tuples containing a MCTS function from search.py and a short string for
        ease of reading.
    """
    line = [player_1[1], player_2[1], play_game(player_1[0], player_2[0])]
    with open('./build/tournament.csv', mode='a') as tourn_file:
        t_writer = csv.writer(tourn_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
        t_writer.writerow(line)
        print('writing:', line)

def play_game(black, white) -> Optional[Tuple[float, float]]:
    """Returns the result of a game between two algorithms.

    Args:
        black: the function that decides the Black player's actions.
        white: the function that decides the White player's actions.
    """
    state = get_default_state(Color.BLACK)
    while not check_victory(state):
        if state.to_move == Color.BLACK:
            action = black(state, 150)
        else:
            action = white(state, 150)
        state = get_next_state(state, action)

    return check_victory(state)

ROUNDS = 10
START = datetime.now()
for rnd in range(ROUNDS):
    tournament(FUNCTIONS)
END = datetime.now()
RUNTIME = pretty_time_delta((END-START).total_seconds())

print(f'Tournament of {ROUNDS} rounds complete.  Runtime: {RUNTIME}.')
