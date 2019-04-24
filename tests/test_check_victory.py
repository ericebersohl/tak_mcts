import env
import unittest

from src.game import check_victory
from src.types import State
from src.enums import Color, Piece

class TestCheckVictory(unittest.TestCase):
    def setUp(self):
        bf = Piece.BLACK_FLAT
        bs = Piece.BLACK_STANDING
        wf = Piece.WHITE_FLAT
        ws = Piece.WHITE_STANDING

        # full board
        self.full_state = State(
            to_move = Color.BLACK,
            white_stones = 5,
            black_stones = 5,
            board = [
                [[bf], [bf], [bf], [bf]],
                [[bf], [bf], [bf], [bf]],
                [[wf, wf], [wf], [wf], [wf]],
                [[wf], [wf], [wf], [wf]],
            ]
        )

        # white_stones == 0
        self.stones_1 = self.full_state._replace(
            white_stones = 0,
            board = [
                [[bf], [bf], [bf], [bf]],
                [[], [], [bf], [bf]],
                [[], [wf], [wf], [wf]],
                [[wf], [wf], [wf], [wf]],
            ]
        )

        # black_stones == 0
        self.stones_2 = self.full_state._replace(
            black_stones = 0,
            board = [
                [[bf], [bf], [bf], [bf]],
                [[bf], [bf], [bf], [bf]],
                [[], [wf], [wf], [wf]],
                [[wf], [wf], [wf], [wf]],
            ]
        )

        self.path_1 = State(
            to_move = Color.BLACK,
            white_stones = 5,
            black_stones = 5,
            board = [
                [[ws], [wf], [], [bs]],
                [[bf], [wf], [bs], [bs]],
                [[bf], [wf], [wf], [bs]],
                [[ws], [bs], [wf], [bs]],
            ]
        )

        self.path_2 = self.path_1._replace(
            board = [
                [[ws], [wf], [bs], []],
                [[bf], [bf], [bf], [bf]],
                [[bf], [wf], [wf], [bs]],
                [[ws], [bs], [wf], [bs]],
            ]
        )

        self.path_3 = self.path_1._replace(
            board = [
                [[ws], [wf], [bs], []],
                [[bf], [bf], [bf], [bf]],
                [[wf], [wf], [wf], [bs]],
                [[ws], [bs], [wf], [wf]],
            ]
        )

        self.no_victory = self.path_1._replace(
            board = [
                [[ws], [wf], [bs], []],
                [[bf], [bs], [bf], [bf]],
                [[wf], [wf], [ws], [bs]],
                [[ws], [bs], [wf], [wf]],
            ]
        )

    def test_check_victory(self):
        # full board
        state = self.full_state
        self.assertEqual((0.5, 0.5), check_victory(state))

        # white stones == 0
        state = self.stones_1
        self.assertEqual((0.0, 1.0), check_victory(state))

        # black stones == 0
        state = self.stones_2
        self.assertEqual((1.0, 0.0), check_victory(state))

        # white path
        state = self.path_1
        self.assertEqual((0.0, 1.0), check_victory(state))
        
        # black path
        state = self.path_2
        self.assertEqual((1.0, 0.0), check_victory(state))
        
        # dual paths
        state = self.path_3
        self.assertEqual((0.0, 1.0), check_victory(state))

        # no victory
        state = self.no_victory
        self.assertEqual(None, check_victory(state))