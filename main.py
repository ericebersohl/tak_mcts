from src.game import *
from src.types import State
from src.utils import print_state

initial_state = State(
    to_move = Color.BLACK,
    black_stones = 15,
    white_stones = 15,
    board = [
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
    ]
)
print_state(initial_state)
print_state(simulate(initial_state))
print_state(initial_state)