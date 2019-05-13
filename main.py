from typing import Optional, Tuple

from src.types import get_default_state
from src.enums import Color
from src.game import get_next_state, check_victory
from src.utils import print_state
from src.search import default_mcts, decisive_move_mcts,\
    weighted_backpropagation_mcts, multi_simulation_mcts

def play_game(color: Color, black_enh, white_enh, iterations: int = 300) -> Optional[Tuple[float, float]]:
    """Plays a game using the given MCTS enhancement functions.
    
    Args:
        color: the Color enum that indicates which player goes first.
        black_enh: a function from search.py that defines the black player's mcts algorithm.
        white_enh: a function from search.py that defines the white player's mcts algorithm.
        iterations: an int defining how many iterations should run for each MCTS search.
    
    Returns:
        A tuple of the form: (BlackScore, WhiteScore).  The range for each score is [0.0, 1.0] where
        1.0 indicates a win, 0.0 indicates a loss, and 0.5 indicates a draw.
    """
    state = get_default_state(color)

    print(f"Starting a game.  {color.value} is going first.\n"
          f"The player with black stones is using {black_enh.__name__}.\n"
          f"The player with white stones is using {white_enh.__name__}.\n")

    while not check_victory(state):
        if state.to_move == Color.BLACK:
            action = black_enh(state, iterations)
        else:
            action = white_enh(state, iterations)
        state = get_next_state(state, action)
        print_state(state)
    return check_victory(state)

# AVAILABLE ENHANCEMENTS:
# default_mcts,
# decisive_move_mcts,
# weighted_backpropagation_mcts,
# multi_simulation_mcts,

print(play_game(Color.BLACK, default_mcts, decisive_move_mcts))