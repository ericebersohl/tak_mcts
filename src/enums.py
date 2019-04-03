from enum import Enum

class Color(Enum):
    BLACK = 'b'
    WHITE = 'w'

class Piece(Enum):
    BLACK_FLAT = 'bf'
    BLACK_STANDING = 'bs'
    WHITE_FLAT = 'wf'
    WHITE_STANDING = 'ws'