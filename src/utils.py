class InvalidMoveError(Exception):
    def __init__(self, message):
        self.message = message

initial_state = {
    'to_move': 'w',
    'w_stones': 10,
    'b_stones': 10,
    'board': [
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
    ],
}