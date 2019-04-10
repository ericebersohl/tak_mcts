"""Enumerated types for Tak.

This module enumerates two types: Color and Piece.  A Color can be either BLACK or WHITE and is used
to distinguish between the two players of a Tak game.  A 4x4 game of Tak has only two stone types:
flat and standing.  As such, there are four types of Piece: BLACK_FLAT, BLACK_STANDING, WHITE_FLAT,
and WHITE_STANDING.
"""
from enum import Enum

class Color(Enum):
    """Defines the Color type."""
    BLACK = 'Black'
    WHITE = 'White'

class Piece(Enum):
    """Defines the Piece type.

    The value of a Piece is stored as a Dict with three keys: 'type', 'color', and 'str':
        'type': Used to determine whether the piece is flat or standing.
        'color': Stores the color of the Piece.
        'str': a string representation of the piece for easy printing.
    """
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
