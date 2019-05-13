"""
Defines functions used to test random weight values for the UCB1 MCTS algorithm.

The module takes a random weight factor in the range (0.0, 10.0] and plays 20 games against the
default weight value of 2.  The result of 20 games of simulations is written to build/weight.csv
in the form: Points,WeightFactor,AvgDepth,AvgBranchFactor

Where average depth and branching factor are included for reference.
"""

from typing import Tuple, List
from statistics import mean
import csv
import random
from datetime import datetime

from src.types import get_default_state
from src.search import default_mcts
from src.enums import Color
from src.game import check_victory, get_next_state, get_actions
from src.utils import pretty_time_delta

def play_game(color: Color, weight: float) -> Tuple[float, int, float]:
    """Plays a game using the default MCTS AI and specified weight factor.

    Args:
        color: the enumerated Color that moves first.  The color with the new weight value is always
        Black.
        weight: the float value weight factor.

    Returns:
        A tuple containing the points that this player acheived as well as the depth of the final
        tree and the average branching factor.
    """
    branch: List[int] = []
    depth: int = 0
    state = get_default_state(color)
    while not check_victory(state):
        if state.to_move == Color.BLACK:
            action = default_mcts(state, 100, weight)
        else:
            action = default_mcts(state, 100, 2.0)
        depth += 1
        branch.append(len(get_actions(state)))
        state = get_next_state(state, action)

    result = check_victory(state)
    if result == (1.0, 0.0):
        return (1.0, depth, mean(branch))
    if result == (0.0, 1.0):
        return (0.0, depth, mean(branch))
    return (0.5, depth, mean(branch))

def test_weight_factor(sims: int) -> None:
    """Plays n games using a randomly generated weight factor.  Appends the result to
    build/weight.csv along with depth and branching factor data.

    Args:
        sims: the number of sims to run.
    """
    # select random weight (0, 10]
    weight = random.uniform(0.0, 10.0)
    starting_player: Color = Color.BLACK

    points = []
    depth = []
    branch = []

    # play 20 games
    for game in range(sims):
        print(f'({game}/{sims})')
        if game%2 == 0:
            starting_player == Color.BLACK
        else:
            starting_player == Color.WHITE

        result = play_game(starting_player, weight)
        points.append(result[0])
        depth.append(result[1])
        branch.append(result[2])

    line = [sum(points), weight, mean(depth), mean(branch)]

    # output results to csv
    with open('./build/weight.csv', mode='a') as weight_file:
        w_writer = csv.writer(weight_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
        w_writer.writerow(line)
        print("writing:", line)

GAMES = 20
RUNS = 200
START = datetime.now()

for run in range(RUNS):
    print(f'Beginning run {run+1} of {RUNS}')
    test_weight_factor(GAMES)

END = datetime.now()

print(f'\nRan {GAMES} simulations in {pretty_time_delta((END - START).total_seconds())}')
