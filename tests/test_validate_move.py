import unittest
import env

from src.enums import Color, Piece
from src.game import validate_action
from src.types import State, Move, Place

class TestValidateMove(unittest.TestCase):

    def test_valid_coordinates(self):
        # row_s, row_e, col_s, col_e < 0
        move = validate_action(self.blank_state, self.invalid_coord_1, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_coord_2, self.debug)
        self.assertEqual(move, False)
        
        move = validate_action(self.blank_state, self.invalid_coord_3, self.debug)
        self.assertEqual(move, False)
        
        move = validate_action(self.blank_state, self.invalid_coord_4, self.debug)
        self.assertEqual(move, False)

        # row_s, row_e, col_s, col_e > 3
        move = validate_action(self.blank_state, self.invalid_coord_5, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_coord_6, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_coord_7, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_coord_8, self.debug)
        self.assertEqual(move, False)

    def test_player_control(self):
        # attempt to move empty square
        move = validate_action(self.blank_state, self.invalid_control, self.debug)
        self.assertEqual(move, False)

        # attempt to move other player's single piece
        move = validate_action(self.single_state_1, self.invalid_control, self.debug)
        self.assertEqual(move, False)

        # attempt to move other player's stack
        move = validate_action(self.single_state_2, self.invalid_control, self.debug)
        self.assertEqual(move, False)

    def test_stack_size_limit(self):
        # carry size > 4
        move = validate_action(self.valid_move_state_1, self.invalid_carry_size_1, self.debug)
        self.assertEqual(move, False)
    
    def test_actual_stack_size(self):
        # carry size < 1
        move = validate_action(self.valid_move_state_1, self.invalid_carry_size_2, self.debug)
        self.assertEqual(move, False)

        # carry size > 1 with one piece
        move = validate_action(self.valid_move_state_1, self.invalid_carry_size_3, self.debug)
        self.assertEqual(move, False)

        # carry size > stack size
        move = validate_action(self.valid_move_state_2, self.invalid_carry_size_4, self.debug)
        self.assertEqual(move, False)
    
    def test_valid_direction(self):
        # start == end
        move = validate_action(self.valid_move_state_1, self.invalid_direction_1, self.debug)
        self.assertEqual(move, False)

        # diagonal movement
        move = validate_action(self.valid_move_state_1, self.invalid_direction_2, self.debug)
        self.assertEqual(move, False)
    
    def test_drop_list(self):
        # length 0
        move = validate_action(self.valid_move_state_2, self.invalid_drop_list_1, self.debug)
        self.assertEqual(move, False)

        # length > 3
        move = validate_action(self.valid_move_state_2, self.invalid_drop_list_2, self.debug)
        self.assertEqual(move, False)

        # length > row/col delta
        move = validate_action(self.valid_move_state_2, self.invalid_drop_list_3, self.debug)
        self.assertEqual(move, False)

        # length < row/col delta
        move = validate_action(self.valid_move_state_2, self.invalid_drop_list_4, self.debug)
        self.assertEqual(move, False)

        # sum different from carry size
        move = validate_action(self.valid_move_state_2, self.invalid_drop_list_5, self.debug)
        self.assertEqual(move, False)
    
    def test_movement_blocked_by_walls(self):
        # positive row over wall
        move = validate_action(self.wall_state_1, self.invalid_wall_move_1, self.debug)
        self.assertEqual(move, False)

        # negative row over wall
        move = validate_action(self.wall_state_2, self.invalid_wall_move_3, self.debug)
        self.assertEqual(move, False)

        # positive col over wall
        move = validate_action(self.wall_state_1, self.invalid_wall_move_2, self.debug)
        self.assertEqual(move, False)

        # negative col over wall
        move = validate_action(self.wall_state_2, self.invalid_wall_move_4, self.debug)
        self.assertEqual(move, False)

        # end on wall
        move = validate_action(self.wall_state_2, self.invalid_wall_move_5, self.debug)
        self.assertEqual(move, False)

    def test_valid_moves(self):
        # moving a wall
        move = validate_action(self.valid_move_state_2, self.valid_move_5, self.debug)
        self.assertEqual(move, True)

        # move to corners
        move = validate_action(self.valid_move_state_3, self.valid_move_1, self.debug)
        self.assertEqual(move, True)

        move = validate_action(self.valid_move_state_4, self.valid_move_2, self.debug)
        self.assertEqual(move, True)

        move = validate_action(self.valid_move_state_5, self.valid_move_3, self.debug)
        self.assertEqual(move, True)

        move = validate_action(self.valid_move_state_6, self.valid_move_4, self.debug)
        self.assertEqual(move, True)

        # single stack
        move = validate_action(self.valid_move_state_2, self.valid_move_6, self.debug)
        self.assertEqual(move, True)
    
    def test_place_coord(self):
        move = validate_action(self.blank_state, self.invalid_place_coord_1, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_place_coord_2, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_place_coord_3, self.debug)
        self.assertEqual(move, False)

        move = validate_action(self.blank_state, self.invalid_place_coord_4, self.debug)
        self.assertEqual(move, False)

    def test_place_occupied(self):
        move = validate_action(self.single_state_1, self.occupied_place, self.debug)
        self.assertEqual(move, False)

    def test_place_wrong_color(self):
        move = validate_action(self.blank_state, self.wrong_color, self.debug)
        self.assertEqual(move, False)

    def setUp(self):
        self.debug = False
        
        #
        # States
        #

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
        self.single_state_1 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [Piece.BLACK_FLAT], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.single_state_2 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [Piece.BLACK_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.BLACK_STANDING], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.valid_move_state_1 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [Piece.WHITE_FLAT], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.valid_move_state_2 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_STANDING], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.wall_state_1 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_STANDING], [Piece.WHITE_STANDING], []],
                [[], [Piece.WHITE_STANDING], [], []],
                [[], [], [], []],
            ]
        )

        self.wall_state_2 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [], [Piece.WHITE_STANDING], []],
                [[], [Piece.WHITE_STANDING], [Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_STANDING], []],
                [[], [], [], []],
            ]
        )

        self.valid_move_state_3 = self.blank_state._replace(
            board = [
                [[Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.valid_move_state_4 = self.blank_state._replace(
            board = [
                [[], [], [], [Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_FLAT]],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
            ]
        )

        self.valid_move_state_5 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], [Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_STANDING]],
            ]
        )

        self.valid_move_state_6 = self.blank_state._replace(
            board = [
                [[], [], [], []],
                [[], [], [], []],
                [[], [], [], []],
                [[Piece.WHITE_FLAT, Piece.WHITE_FLAT, Piece.WHITE_STANDING], [], [], []],
            ]
        )

        #
        # Moves
        #

        # invalid coordinates
        self.invalid_coord_1 = Move(
            start_coord = (-1, 1),
            end_coord = (1, 1),
            carry_size = 1,
            drop_list = [1],
        )
        self.invalid_coord_2 = self.invalid_coord_1._replace(start_coord = (1, -1))
        self.invalid_coord_3 = self.invalid_coord_2._replace(start_coord = (1, 1), end_coord = (-1, 1))
        self.invalid_coord_4 = self.invalid_coord_3._replace(end_coord = (1, -1))
        self.invalid_coord_5 = self.invalid_coord_1._replace(start_coord = (4, 1))       
        self.invalid_coord_6 = self.invalid_coord_1._replace(start_coord = (1, 4))
        self.invalid_coord_7 = self.invalid_coord_3._replace(end_coord = (4, 1)) 
        self.invalid_coord_8 = self.invalid_coord_7._replace(end_coord = (1, 4))
        
        # invalid player control
        self.invalid_control = Move(
            start_coord = (1, 1),
            end_coord = (1, 2),
            carry_size = 1,
            drop_list = [1],
        )

        # invalid carry size
        self.invalid_carry_size_1 = Move(
            start_coord = (1, 1),
            end_coord = (1, 2),
            carry_size = 5,
            drop_list = [1],
        )
        self.invalid_carry_size_2 = self.invalid_carry_size_1._replace(carry_size = 0)
        self.invalid_carry_size_3 = self.invalid_carry_size_1._replace(carry_size = 2)
        self.invalid_carry_size_4 = self.invalid_carry_size_1._replace(carry_size = 4)

        # valid direction
        self.invalid_direction_1 = Move(
            start_coord = (1, 1),
            end_coord = (1, 1),
            carry_size = 1,
            drop_list = [1],
        )
        self.invalid_direction_2 = self.invalid_direction_1._replace(end_coord = (2, 3))

        # drop list
        self.invalid_drop_list_1 = Move(
            start_coord = (1, 1),
            end_coord = (1, 2),
            carry_size = 1,
            drop_list = [],
        )
        self.invalid_drop_list_2 = self.invalid_drop_list_1._replace(carry_size = 4, drop_list = [1, 1, 1, 1])
        self.invalid_drop_list_3 = self.invalid_drop_list_1._replace(carry_size = 2, drop_list = [1, 1])
        self.invalid_drop_list_4 = self.invalid_drop_list_1._replace(carry_size = 1, drop_list = [1], end_coord = (1, 3))
        self.invalid_drop_list_5 = self.invalid_drop_list_1._replace(carry_size = 1, drop_list = [1, 1], end_coord = (1, 3))

        # wall moves
        self.invalid_wall_move_1 = Move(
            start_coord = (1, 1),
            end_coord = (3, 1),
            carry_size = 3,
            drop_list = [1, 2],
        )
        self.invalid_wall_move_2 = self.invalid_wall_move_1._replace(end_coord = (1, 3))
        self.invalid_wall_move_3 = Move(
            start_coord = (2, 2),
            end_coord = (0, 2),
            carry_size = 3,
            drop_list = [1, 2],
        )
        self.invalid_wall_move_4 = self.invalid_wall_move_3._replace(end_coord = (2, 0))
        self.invalid_wall_move_5 = self.invalid_wall_move_3._replace(
            end_coord = (2, 1),
            drop_list = [3],
        )

        # moves
        self.valid_move_1 = Move(
            start_coord = (0, 0),
            end_coord = (0, 3),
            carry_size = 3,
            drop_list = [1, 1, 1],
        )
        self.valid_move_2 = self.valid_move_1._replace(
            start_coord = (0, 3),
            end_coord = (3, 3),
        )
        self.valid_move_3 = self.valid_move_1._replace(
            start_coord = (3, 3),
            end_coord = (3, 0),
        )
        self.valid_move_4 = self.valid_move_1._replace(
            start_coord = (3, 0),
            end_coord = (0, 0),
        )
        self.valid_move_5 = Move(
            start_coord = (1, 1),
            end_coord = (0, 1),
            carry_size = 1,
            drop_list = [1],
        )
        self.valid_move_6 = self.valid_move_5._replace(carry_size = 3, drop_list = [3])

        #
        # PLACES
        #

        self.invalid_place_coord_1 = Place(
            coord = (-1, 1),
            piece = Piece.WHITE_FLAT
        )
        self.invalid_place_coord_2 = self.invalid_place_coord_1._replace(coord = (1, -1))
        self.invalid_place_coord_3 = self.invalid_place_coord_1._replace(coord = (4, 1))
        self.invalid_place_coord_4 = self.invalid_place_coord_1._replace(coord = (1, 4))

        self.occupied_place = Place(
            coord = (1, 1),
            piece = Piece.WHITE_FLAT,
        )

        self.wrong_color = Place(
            coord = (0, 0),
            piece = Piece.BLACK_STANDING,
        )