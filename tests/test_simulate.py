import unittest
import tests.env

from src.game import simulate
from src.types import State
from src.enums import Color
from src.utils import print_state

class TestSimulate(unittest.TestCase):
    def setUp(self):
        self.start_state = State(
            to_move = Color.BLACK,
            black_stones = 15,
            white_stones = 15,
            board = [
                [[],[],[],[]],
                [[],[],[],[]],
                [[],[],[],[]],
                [[],[],[],[]],
            ],
        )

        self.end_state = self.start_state._replace()

    def test_immutability(self):
        simulate(self.start_state)
        self.assertEqual(self.start_state, self.end_state)