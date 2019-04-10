from enum import Enum, auto

class Color(Enum):
    BLACK = 'Black'
    WHITE = 'White'

class Piece(Enum):
    BLACK_FLAT = {
        'type' : 'flat',
        'color': Color.BLACK,
        'str' : 'bf',
    }
    BLACK_STANDING = {
        'type' : 'standing',
        'color': Color.BLACK,
        'str' : 'bs',
    }
    WHITE_FLAT = {
        'type' : 'flat',
        'color': Color.WHITE,
        'str' : 'wf',
    }
    WHITE_STANDING = {
        'type' : 'standing',
        'color': Color.WHITE,
        'str' : 'ws'
    }