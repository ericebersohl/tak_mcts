from src.game import *
from src.types import State
from src.utils import print_state
from src.node import Node
from src.search import mcts

bf = Piece.BLACK_FLAT
bs = Piece.BLACK_STANDING
wf = Piece.WHITE_FLAT
ws = Piece.WHITE_STANDING

initial_state = State(
    to_move = Color.BLACK,
    black_stones = 12,
    white_stones = 12,
    board = [
        [[wf], [wf], [wf], []],
        [[], [], [], [bf]],
        [[], [], [], [bf]],
        [[], [], [], [bf]],
    ]
)
print_state(initial_state)
print_state(simulate(initial_state))
print_state(initial_state)
