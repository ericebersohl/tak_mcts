from src.types import State, default_state
from src.search import default_mcts
from src.enums import Color
from src.game import check_victory, get_next_state
from src.utils import print_state, get_action_string

def play_game():
    """Plays a game using the default MCTS AI"""
    state = default_state
    while not check_victory(state):
        print_state(state)
        if state.to_move == Color.BLACK:
            action = default_mcts(state, 1000)
        else:
            action = default_mcts(state, 100)
        print(get_action_string(action))
        state = get_next_state(state, action)

    result = check_victory(state)
    if result == (1.0, 0.0):
        print("Black wins")
    elif result == (0.0, 1.0):
        print("White wins")
    elif result == (0.5, 0.5):
        print("Draw.")
    else:
        print("Error.")

play_game()