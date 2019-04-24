import tests.env
import unittest

from src.node import Node
from src.types import State, Place
from src.enums import Color, Piece

class TestNode(unittest.TestCase):
    def setUp(self):
        self.initial_state = State(
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

        self.test_state_1 = State(
            to_move = Color.WHITE,
            black_stones = 14,
            white_stones = 15,
            board = [
                [[Piece.BLACK_FLAT], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.test_action = Place(
            coord = (0, 0),
            piece = Piece.BLACK_FLAT,
        )

        self.test_node = Node(None, self.initial_state, None)
        self.test_node._visits = 6
        self.test_node._wins = 3

        self.test_child_1 = Node(None, self.initial_state, self.test_node)
        self.test_child_1._visits = 2
        self.test_child_1._wins = 0
        self.test_child_2 = Node(None, self.initial_state, self.test_node)
        self.test_child_2._visits = 2
        self.test_child_2._wins = 2
        self.test_child_3 = Node(None, self.initial_state, self.test_node)
        self.test_child_3._visits = 2
        self.test_child_3._wins = 1

        self.test_node._children = [self.test_child_1, self.test_child_2, self.test_child_3]

    def test_calculate_uct(self):
        with self.assertRaises(ValueError):
            self.test_node.calculate_uct(0, -1)
        
        with self.assertRaises(ValueError):
            self.test_node.calculate_uct(0, 15)

        with self.assertRaises(ValueError):
            self.test_node.calculate_uct(5, 3)

        self.assertEqual(self.test_node.calculate_uct(0, 0), float("inf"))
        self.assertAlmostEqual(self.test_node.calculate_uct(2,3), 2.8525361)

    def test_select_child(self):
        self.assertEqual(self.test_node.select_child(), self.test_child_2)

    def test_add_child(self):
        previous = len(self.test_node._unexplored)
        self.test_node.add_child(self.test_action)
        self.assertEqual(len(self.test_node._children), 4)
        self.assertEqual(previous-1, len(self.test_node._unexplored))