import unittest
import tests.env

from src.utils import split_stack, get_drop_lists, get_controlled, bfs, get_path
from src.types import State
from src.enums import Color, Piece

class TestUtils(unittest.TestCase):
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
    
    def test_split_stack(self):
        a = ['a', 'b', 'c', 'd', 'e', 'f']
        b = []
        c = ['a']

        expected_1 = ['a', 'b', 'c']
        expected_2 = ['d', 'e', 'f']
        actual_1, actual_2 = split_stack(a, 3)
        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)

        expected_1 = []
        expected_2 = ['a']
        actual_1, actual_2 = split_stack(c, 1)
        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)

        expected_1 = []
        expected_2 = ['a', 'b', 'c', 'd', 'e', 'f']
        actual_1, actual_2 = split_stack(a, 6)
        self.assertEqual(actual_1, expected_1)
        self.assertEqual(actual_2, expected_2)
        
        with self.assertRaises(RuntimeError):
            split_stack(a, 0)
        
        with self.assertRaises(RuntimeError):
            split_stack(b, 1)

    def test_get_controlled(self):
        board = self.blank_state.board
        coord = (1, 1)
        color = Color.BLACK
        self.assertEqual(False, get_controlled(board, coord, color))

        board = self.test_state_1.board
        self.assertEqual(False, get_controlled(board, coord, color))

        color = Color.WHITE
        self.assertEqual(True, get_controlled(board, coord, color))

    def test_bfs(self):
        board = self.blank_state.board
        start = (0,0)
        goal = [(3, 0), (3, 1), (3, 2), (3, 3)]
        color = Color.WHITE
        self.assertEqual(False, bfs(board, start, goal, color))
    
        board = self.bfs_state_1.board
        self.assertEqual(True, bfs(board, start, goal, color))

        board = self.bfs_state_2.board
        self.assertEqual(True, bfs(board, start, goal, color))

        color = Color.BLACK
        self.assertEqual(False, bfs(board, start, goal, color))

        board = self.bfs_state_3.board
        self.assertEqual(False, bfs(board, start, goal, color))

    def test_get_path(self):
        state = self.blank_state
        self.assertEqual((False, False), get_path(state))

        state = self.bfs_state_1
        self.assertEqual((False, True), get_path(state))

        state = self.get_path_1
        self.assertEqual((True, True), get_path(state))

    def setUp(self):
        self.blank_state = State(
            to_move = Color.BLACK,
            black_stones = 15,
            white_stones = 15,
            board = [
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.test_state_1 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [Piece.WHITE_FLAT], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.bfs_state_1 = self.blank_state._replace(
            board = [
                [[Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT], [], [], []],
            ]
        )

        self.bfs_state_2 = self.blank_state._replace(
            board = [
                [[Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT], [Piece.WHITE_FLAT], [Piece.WHITE_FLAT], [Piece.WHITE_FLAT]],
                [[], [], [], [Piece.WHITE_FLAT]],
                [[], [], [], [Piece.WHITE_FLAT]],
            ]
        )

        self.bfs_state_3 = self.blank_state._replace(
            board = [
                [[Piece.WHITE_FLAT], [], [], []],
                [[Piece.WHITE_FLAT], [Piece.WHITE_FLAT], [Piece.WHITE_FLAT], [Piece.WHITE_FLAT]],
                [[], [], [], [Piece.WHITE_STANDING]],
                [[], [], [], [Piece.WHITE_FLAT]],
            ]
        )

        self.get_path_1 = self.blank_state._replace(
            board = [
                [[Piece.WHITE_FLAT],    [],                 [],                 []],
                [[Piece.WHITE_FLAT],    [Piece.WHITE_FLAT], [Piece.WHITE_FLAT], [Piece.WHITE_FLAT]],
                [[Piece.BLACK_FLAT],    [Piece.BLACK_FLAT], [Piece.BLACK_FLAT], [Piece.BLACK_FLAT]],
                [[],                    [],                 [],                 [Piece.WHITE_FLAT]],
            ]
        )