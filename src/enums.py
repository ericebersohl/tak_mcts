from enum import Enum

class Color(Enum):
    BLACK = 'b'
    WHITE = 'w'

class Piece(Enum):
    BLACK_FLAT = Color.BLACK
    BLACK_STANDING = Color.BLACK
    WHITE_FLAT = Color.WHITE
    WHITE_STANDING = Color.WHITE