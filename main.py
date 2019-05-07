from typing import Tuple, List
from statistics import mean
import csv
import random
from datetime import datetime, timedelta

from src.types import State, get_default_state
from src.search import default_mcts, decisive_move_mcts, multi_simulation_mcts
from src.enums import Color
from src.game import check_victory, get_next_state, get_actions
from src.utils import print_state, get_action_string

def play_game(color: Color, weight: float) -> Tuple[float, int, float]:
    """Plays a game using the default MCTS AI"""
    branch: List[int] = []
    depth: int = 0
    state = get_default_state(color)
    while not check_victory(state):
        if state.to_move == Color.BLACK:
            action = default_mcts(state, 10, weight)
        else:
            action = default_mcts(state, 10, 2.0)
        depth += 1
        branch.append(len(get_actions(state)))
        state = get_next_state(state, action)

    result = check_victory(state)
    if result == (1.0, 0.0):
        return (1.0, depth, mean(branch))
    if result == (0.0, 1.0):
        return (0.0, depth, mean(branch))
    return (0.5, depth, mean(branch))

def test_weight_factor(sims: int):
    # select random weight (0, 10]
    weight = random.uniform(0.0, 10.0)
    starting_player: Color = Color.BLACK

    points = []
    depth = []
    branch = []

    # play 20 games
    for game in range(sims):
        print(f'{game}, ', end='')
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
    with open ('./output/weight.csv', mode='a') as weight_file:
        weight_writer = csv.writer(weight_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar='"')
        weight_writer.writerow(line)
        print("writing:",line)

n = 3
start = datetime.now()
test_weight_factor(n)
end = datetime.now()

diff: timedelta = end - start
days = diff.days
hours = diff.seconds // 3600
minutes = (diff.seconds // 3600) % 60
seconds = ((diff.seconds // 3600) % 60) % 60

print(f"Ran {n} simulations in {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.")