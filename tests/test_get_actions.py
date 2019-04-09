import unittest
import env
import pprint as pp

from src.game import get_drop_lists, get_actions
from src.types import State, Place, Move
from src.enums import Piece, Color

class TestGetActions(unittest.TestCase):
    def test_get_drop_lists(self):
        carry = 1
        moves = 1
        self.assertEqual(get_drop_lists(carry, moves), [[1]])

        carry = 2
        moves = 1
        self.assertEqual(get_drop_lists(carry, moves), [[2]])

        carry = 2
        moves = 2
        self.assertEqual(get_drop_lists(carry, moves), [[1, 1]])

        carry = 3
        moves = 2
        self.assertEqual(get_drop_lists(carry, moves), [[1, 2], [2, 1]])

        carry = 6
        moves = 3
        self.assertEqual(get_drop_lists(carry, moves), [
            [2, 2, 2], [3, 1, 2], [1, 3, 2],
            [3, 2, 1], [2, 1, 3], [1, 4, 1],
            [2, 3, 1], [1, 2, 3], [4, 1, 1],
            [1, 1, 4],
        ])

    def test_get_actions(self):
        expected = [
            Place(coord = (0, 0), piece = Piece.WHITE_FLAT),
            Place(coord = (0, 1), piece = Piece.WHITE_FLAT),
            Place(coord = (0, 2), piece = Piece.WHITE_FLAT),
            Place(coord = (0, 3), piece = Piece.WHITE_FLAT),
            Place(coord = (1, 0), piece = Piece.WHITE_FLAT),
            Place(coord = (1, 1), piece = Piece.WHITE_FLAT),
            Place(coord = (1, 2), piece = Piece.WHITE_FLAT),
            Place(coord = (1, 3), piece = Piece.WHITE_FLAT),
            Place(coord = (2, 0), piece = Piece.WHITE_FLAT),
            Place(coord = (2, 1), piece = Piece.WHITE_FLAT),
            Place(coord = (2, 2), piece = Piece.WHITE_FLAT),
            Place(coord = (2, 3), piece = Piece.WHITE_FLAT),
            Place(coord = (3, 0), piece = Piece.WHITE_FLAT),
            Place(coord = (3, 1), piece = Piece.WHITE_FLAT),
            Place(coord = (3, 2), piece = Piece.WHITE_FLAT),
            Place(coord = (3, 3), piece = Piece.WHITE_FLAT),
            Place(coord = (0, 0), piece = Piece.WHITE_STANDING),
            Place(coord = (0, 1), piece = Piece.WHITE_STANDING),
            Place(coord = (0, 2), piece = Piece.WHITE_STANDING),
            Place(coord = (0, 3), piece = Piece.WHITE_STANDING),
            Place(coord = (1, 0), piece = Piece.WHITE_STANDING),
            Place(coord = (1, 1), piece = Piece.WHITE_STANDING),
            Place(coord = (1, 2), piece = Piece.WHITE_STANDING),
            Place(coord = (1, 3), piece = Piece.WHITE_STANDING),
            Place(coord = (2, 0), piece = Piece.WHITE_STANDING),
            Place(coord = (2, 1), piece = Piece.WHITE_STANDING),
            Place(coord = (2, 2), piece = Piece.WHITE_STANDING),
            Place(coord = (2, 3), piece = Piece.WHITE_STANDING),
            Place(coord = (3, 0), piece = Piece.WHITE_STANDING),
            Place(coord = (3, 1), piece = Piece.WHITE_STANDING),
            Place(coord = (3, 2), piece = Piece.WHITE_STANDING),
            Place(coord = (3, 3), piece = Piece.WHITE_STANDING),
        ]
        self.assertEqual(set(expected), set(get_actions(self.blank_state)))

        expected_2 = [
            Move(start_coord = (3, 3), end_coord = (0, 3), carry_size = 4, drop_list = [1, 1, 2]),
            Move(start_coord = (3, 3), end_coord = (0, 3), carry_size = 4, drop_list = [1, 2, 1]),
            Move(start_coord = (3, 3), end_coord = (0, 3), carry_size = 4, drop_list = [2, 1, 1]),
            Move(start_coord = (3, 3), end_coord = (0, 3), carry_size = 3, drop_list = [1, 1, 1]),
            Move(start_coord = (3, 3), end_coord = (1, 3), carry_size = 4, drop_list = [2, 2]),
            Move(start_coord = (3, 3), end_coord = (1, 3), carry_size = 4, drop_list = [1, 3]),
            Move(start_coord = (3, 3), end_coord = (1, 3), carry_size = 4, drop_list = [3, 1]),
            Move(start_coord = (3, 3), end_coord = (1, 3), carry_size = 3, drop_list = [2, 1]),
            Move(start_coord = (3, 3), end_coord = (1, 3), carry_size = 3, drop_list = [1, 2]),
            Move(start_coord = (3, 3), end_coord = (1, 3), carry_size = 2, drop_list = [1, 1]),
            Move(start_coord = (3, 3), end_coord = (2, 3), carry_size = 4, drop_list = [4]),
            Move(start_coord = (3, 3), end_coord = (2, 3), carry_size = 3, drop_list = [3]),
            Move(start_coord = (3, 3), end_coord = (2, 3), carry_size = 2, drop_list = [2]),
            Move(start_coord = (3, 3), end_coord = (2, 3), carry_size = 1, drop_list = [1]),
            Move(start_coord = (3, 3), end_coord = (3, 0), carry_size = 4, drop_list = [1, 1, 2]),
            Move(start_coord = (3, 3), end_coord = (3, 0), carry_size = 4, drop_list = [1, 2, 1]),
            Move(start_coord = (3, 3), end_coord = (3, 0), carry_size = 4, drop_list = [2, 1, 1]),
            Move(start_coord = (3, 3), end_coord = (3, 0), carry_size = 3, drop_list = [1, 1, 1]),
            Move(start_coord = (3, 3), end_coord = (3, 1), carry_size = 4, drop_list = [2, 2]),
            Move(start_coord = (3, 3), end_coord = (3, 1), carry_size = 4, drop_list = [1, 3]),
            Move(start_coord = (3, 3), end_coord = (3, 1), carry_size = 4, drop_list = [3, 1]),
            Move(start_coord = (3, 3), end_coord = (3, 1), carry_size = 3, drop_list = [2, 1]),
            Move(start_coord = (3, 3), end_coord = (3, 1), carry_size = 3, drop_list = [1, 2]),
            Move(start_coord = (3, 3), end_coord = (3, 1), carry_size = 2, drop_list = [1, 1]),
            Move(start_coord = (3, 3), end_coord = (3, 2), carry_size = 4, drop_list = [4]),
            Move(start_coord = (3, 3), end_coord = (3, 2), carry_size = 3, drop_list = [3]),
            Move(start_coord = (3, 3), end_coord = (3, 2), carry_size = 2, drop_list = [2]),
            Move(start_coord = (3, 3), end_coord = (3, 2), carry_size = 1, drop_list = [1]),
            Move(start_coord = (1, 1), end_coord = (0, 1), carry_size = 2, drop_list = [2]),
            Move(start_coord = (1, 1), end_coord = (1, 0), carry_size = 2, drop_list = [2]),
            Move(start_coord = (1, 1), end_coord = (2, 1), carry_size = 2, drop_list = [2]),
            Move(start_coord = (1, 1), end_coord = (1, 2), carry_size = 2, drop_list = [2]),
            Move(start_coord = (1, 1), end_coord = (1, 3), carry_size = 2, drop_list = [1, 1]),
            Move(start_coord = (1, 1), end_coord = (3, 1), carry_size = 2, drop_list = [1, 1]),
            Move(start_coord = (1, 1), end_coord = (0, 1), carry_size = 1, drop_list = [1]),
            Move(start_coord = (1, 1), end_coord = (1, 0), carry_size = 1, drop_list = [1]),
            Move(start_coord = (1, 1), end_coord = (2, 1), carry_size = 1, drop_list = [1]),
            Move(start_coord = (1, 1), end_coord = (1, 2), carry_size = 1, drop_list = [1]),
        ]
        self.assertEqual(len(expected_2), len(get_actions(self.test_state_1)))

        with self.assertRaises(RuntimeError):
            get_actions(self.error_state)

    def setUp(self):
        self.blank_state = State(
            to_move = Color.WHITE,
            white_stones = 10,
            black_stones = 10,
            board = [
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        ws = Piece.WHITE_STANDING
        wf = Piece.WHITE_FLAT
        bs = Piece.BLACK_STANDING
        bf = Piece.BLACK_FLAT

        self.test_state_1 = State(
            to_move = Color.WHITE,
            white_stones = 10,
            black_stones = 10,
            board = [
                [[bf], [bf], [bf], [bf]],
                [[bf], [bf, ws], [bf], [bf]],
                [[bf], [bf], [bf], [bf]],
                [[bf], [bf], [bf], [bf, wf, wf, ws]],
            ] 
        )

        self.error_state = self.blank_state._replace(black_stones = 0)