from src.types import State
from src.search import default_mcts
from src.enums import Piece, Color

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

print(default_mcts(initial_state, 100))
