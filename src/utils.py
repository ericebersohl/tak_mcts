class InvalidMoveError(Exception):
    def __init__(self, message):
        self.message = message

initial_state = {
    'to_move': 'w',
    'board': [
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
        [[], [], [], []],
    ],
}