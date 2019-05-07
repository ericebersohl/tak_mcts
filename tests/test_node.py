import tests.env
import unittest

from src.node import Node
from src.types import State, Place, get_default_state
from src.enums import Color, Piece
from src.game import get_next_state
from src.utils import calculate_uct

class TestNode(unittest.TestCase):
    def setUp(self):
        # States and Actions
        self.action_1 = Place(coord=(0,0), piece=Piece.BLACK_FLAT)
        self.action_2 = Place(coord=(1,0), piece=Piece.BLACK_FLAT)
        self.action_3 = Place(coord=(2,0), piece=Piece.BLACK_FLAT)

        # Create Tree
        self.root_node = Node(None, get_default_state(Color.BLACK), None)
        self.child_1 = self.root_node.add_child(
            self.action_1,
            get_next_state(get_default_state(Color.BLACK), self.action_1)
        )
        self.child_2 = self.root_node.add_child(
            self.action_2,
            get_next_state(get_default_state(Color.BLACK), self.action_2)
        )
        self.child_3 = self.root_node.add_child(
            self.action_3,
            get_next_state(get_default_state(Color.BLACK), self.action_3)
        )

        # Set Wins and Visits
        self.root_node._wins = 5
        self.root_node._visits = 10
        self.child_1._wins = 0
        self.child_1._visits = 3
        self.child_2._wins = 2
        self.child_2._visits = 3
        self.child_3._wins = 3
        self.child_3._visits = 4

    def test_calculate_uct(self):
        c1_actual = calculate_uct(self.child_1._wins, self.child_1._visits, self.root_node._visits)
        c2_actual = calculate_uct(self.child_2._wins, self.child_2._visits, self.root_node._visits)
        c3_actual = calculate_uct(self.child_3._wins, self.child_3._visits, self.root_node._visits)
        c1_expected = 2.4779481
        c2_expected = 3.1446148
        c3_expected = 2.8959660
        self.assertAlmostEqual(c1_actual, c1_expected)
        self.assertAlmostEqual(c2_actual, c2_expected)
        self.assertAlmostEqual(c3_actual, c3_expected)

    def test_select_child(self):
        self.assertEqual(self.root_node.select_child(), self.child_2)

    def test_update_node(self):
        result_1 = (1.0, 0.0)
        result_2 = (0.0, 1.0)
        result_3 = (0.5, 0.5)

        self.child_1.update_node(result_1)
        self.assertEqual(self.child_1._visits, 4)
        self.assertEqual(self.child_1._wins, 0)

        self.child_1.update_node(result_2)
        self.assertEqual(self.child_1._visits, 5)
        self.assertEqual(self.child_1._wins, 1)

        self.child_1.update_node(result_3)
        self.assertEqual(self.child_1._visits, 6)
        self.assertEqual(self.child_1._wins, 1.5)
