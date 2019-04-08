from enum import Enum, auto

class Color(Enum):
    BLACK = auto()
    WHITE = auto()

class Piece(Enum):
    BLACK_FLAT = {
        'type' : 'flat',
        'color': Color.BLACK,
    }
    BLACK_STANDING = {
        'type' : 'standing',
        'color': Color.BLACK,
    }
    WHITE_FLAT = {
        'type' : 'flat',
        'color': Color.WHITE,
    }
    WHITE_STANDING = {
        'type' : 'standing',
        'color': Color.WHITE,
    }