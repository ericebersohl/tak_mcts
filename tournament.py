import csv
from typing import List, Tuple, Optional
from random import choice
from datetime import datetime

from src.game import get_next_state, check_victory
from src.types import get_default_state, State
from src.enums import Color
from src.search import default_mcts, decisive_move_mcts,\
    weighted_backpropagation_mcts, multi_simulation_mcts

functions = [
    (default_mcts, 'def'),
    (decisive_move_mcts, 'dec'),
    (weighted_backpropagation_mcts, 'wbp'),
    (multi_simulation_mcts, 'msm'),
]

def tournament(funcs: List) -> None:
    for black in funcs:
        for white in funcs:
            record_result(black, white)

def record_result(p1: Tuple, p2: Tuple) -> None:
    line = [p1[1], p2[1], play_game(p1[0], p2[0])]
    with open('./build/tournament.csv', mode='a') as tourn_file:
        tourn_writer = csv.writer(tourn_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
        tourn_writer.writerow(line)
        print('writing:', line)

def play_game(black, white) -> Optional[Tuple[float, float]]:
    state = get_default_state(Color.BLACK)
    while not check_victory(state):
        if state.to_move == Color.BLACK:
            action = black(state, 150)
        else:
            action = white(state, 150)
        state = get_next_state(state, action)

    return check_victory(state)

# courtesy of https://gist.github.com/thatalextaylor/7408395
def pretty_time_delta(seconds):
    seconds = int(seconds)
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%dd%dh%dm%ds' % (days, hours, minutes, seconds)
    elif hours > 0:
        return '%dh%dm%ds' % (hours, minutes, seconds)
    elif minutes > 0:
        return '%dm%ds' % (minutes, seconds)
    else:
        return '%ds' % (seconds,)

sims = 0
while True:
    start = datetime.now()
    tournament(functions)
    end = datetime.now()
    sims+=1
    runtime = pretty_time_delta((end-start).total_seconds())
    print(f'Tournament {sims} complete.  Runtime: {runtime}.')