import unittest
import tests.env

from src.enums import Color, Piece
from src.game import get_next_state, split_stack
from src.types import State, Place, Move

class TestGetNextState(unittest.TestCase):

    def test_place(self):
        place_1 = Place(
            coord = (1, 2),
            piece = Piece.WHITE_FLAT,
        )
        expected_1 = self.blank_state._replace(
            to_move = Color.BLACK,
            white_stones = 9,
            board = [
                [[], [], [], []],
                [[], [], [Piece.WHITE_FLAT], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )
        actual_1 = get_next_state(self.blank_state, place_1)
        self.assertEqual(expected_1, actual_1)

        place_2 = Place(
            coord = (3, 3),
            piece = Piece.BLACK_STANDING,
        )
        expected_2 = expected_1._replace(
            to_move = Color.WHITE,
            black_stones = 9,
            board = [
                [[], [], [], []],
                [[], [], [Piece.WHITE_FLAT], []],
                [[], [], [], []],
                [[], [], [], [Piece.BLACK_STANDING]],
            ]
        )
        actual_2 = get_next_state(actual_1, place_2)
        self.assertEqual(expected_2, actual_2)

        place_3 = place_2._replace(piece = Piece.WHITE_STANDING)
        with self.assertRaises(RuntimeError):
            get_next_state(actual_2, place_3)
    
    def test_move(self):
        move_1 = Move(
            start_coord = (1, 0),
            end_coord = (1, 3),
            carry_size = 3,
            drop_list = [1, 1, 1],
        )
        expected_1 = self.row_move._replace(
            to_move = Color.BLACK,
            board = [
                [[], [], [], []],
                [[], [Piece.WHITE_FLAT], [Piece.BLACK_FLAT], [Piece.WHITE_STANDING]],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )
        actual_1 = get_next_state(self.row_move, move_1)
        self.assertEqual(expected_1, actual_1)

        move_2 = Move(
            start_coord = (1, 2),
            end_coord = (0, 2),
            carry_size = 1,
            drop_list = [1],
        )
        expected_2 = expected_1._replace(
            to_move = Color.WHITE,
            board = [
                [[], [], [Piece.BLACK_FLAT], []],
                [[], [Piece.WHITE_FLAT], [], [Piece.WHITE_STANDING]],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )
        actual_2 = get_next_state(expected_1, move_2)
        self.assertEqual(expected_2, actual_2)

        move_3 = Move(
            start_coord = (0, 0),
            end_coord = (3, 0),
            carry_size = 4,
            drop_list = [2, 1, 1],
        )

        actual_3 = get_next_state(self.stack_move, move_3)
        expected_3 = self.blank_state._replace(
            black_stones = 6,
            white_stones = 3,
            board = [
                [[], [], [], []],
                [[Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.BLACK_FLAT, Piece.BLACK_FLAT], [], [], []],
                [[Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.BLACK_FLAT], [], [], []],
                [[Piece.WHITE_FLAT, Piece.BLACK_STANDING], [], [], []],
            ],
        )

        self.assertEqual(expected_3, actual_3)

    def setUp(self):
        self.blank_state = State(
            to_move = Color.WHITE,
            black_stones = 10,
            white_stones = 10,
            board = [
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.row_move = State(
            to_move = Color.WHITE,
            black_stones = 9,
            white_stones = 8,
            board = [
                [[], [], [], []],
                [[Piece.WHITE_FLAT, Piece.BLACK_FLAT, Piece.WHITE_STANDING], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.stack_move = State(
            to_move = Color.BLACK,
            black_stones = 6,
            white_stones = 3,
            board = [
                [[Piece.BLACK_FLAT, Piece.BLACK_FLAT, Piece.BLACK_FLAT, Piece.BLACK_STANDING], [], [], []],
                [[Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT], [], [], []],
            ],
        )