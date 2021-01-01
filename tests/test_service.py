import unittest

from domain.board import Board
from domain.validaors import MoveValidator, AddMoveException
from service.game_manager import GameManager


class TestGameManager(unittest.TestCase):
    def setUp(self) -> None:
        move_validator = MoveValidator()
        self.game_manager = GameManager(Board(6, 6), move_validator)

    def test_set_board_size(self):
        self.game_manager.set_board_size(5, 5)
        self.assertTrue(self.game_manager.board.get_cell(5, 5), ' ')
        self.assertRaises(IndexError, self.game_manager.board.get_cell, 6, 6)

    def test_add_move(self):
        self.game_manager.add_move(2, 2, 'X')
        self.assertEqual(self.game_manager.last_move_by, 'X')

        self.assertEqual(self.game_manager.board.get_cell(1, 1), '-')
        self.assertEqual(self.game_manager.board.get_cell(1, 2), '-')
        self.assertEqual(self.game_manager.board.get_cell(1, 3), '-')
        self.assertEqual(self.game_manager.board.get_cell(1, 4), ' ')
        self.assertEqual(self.game_manager.board.get_cell(2, 1), '-')
        self.assertEqual(self.game_manager.board.get_cell(2, 2), 'X')
        self.assertEqual(self.game_manager.board.get_cell(2, 3), '-')
        self.assertEqual(self.game_manager.board.get_cell(2, 4), ' ')
        self.assertEqual(self.game_manager.board.get_cell(3, 1), '-')
        self.assertEqual(self.game_manager.board.get_cell(3, 2), '-')
        self.assertEqual(self.game_manager.board.get_cell(3, 3), '-')
        self.assertEqual(self.game_manager.board.get_cell(3, 4), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 1), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 2), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 3), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 4), ' ')

        self.assertRaises(AddMoveException, self.game_manager.add_move, 0, 0, 'X')
        self.assertRaises(AddMoveException, self.game_manager.add_move, 6, 7, 'O')
        self.assertRaises(AddMoveException, self.game_manager.add_move, 7, 6, 'X')
        self.assertRaises(AddMoveException, self.game_manager.add_move, 7, 7, 'O')
        self.assertRaises(AddMoveException, self.game_manager.add_move, 2, 2, 'O')
        self.assertRaises(AddMoveException, self.game_manager.add_move, 1, 1, 'X')
        self.assertEqual(self.game_manager.last_move_by, 'X')

        self.game_manager.add_move(6, 6, 'O')
        self.assertEqual(self.game_manager.board.get_cell(4, 3), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 4), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 5), ' ')
        self.assertEqual(self.game_manager.board.get_cell(4, 6), ' ')
        self.assertEqual(self.game_manager.board.get_cell(5, 4), ' ')
        self.assertEqual(self.game_manager.board.get_cell(5, 5), '-')
        self.assertEqual(self.game_manager.board.get_cell(5, 6), '-')
        self.assertEqual(self.game_manager.board.get_cell(6, 4), ' ')
        self.assertEqual(self.game_manager.board.get_cell(6, 5), '-')
        self.assertEqual(self.game_manager.board.get_cell(6, 6), 'O')

    def test_move_computer_easy(self):
        self.game_manager.move_computer_easy('O')
        self.assertEqual(self.game_manager.board.get_cell(1, 1), 'O')
        self.assertEqual(self.game_manager.board.get_cell(1, 2), '-')
        self.assertEqual(self.game_manager.board.get_cell(1, 3), ' ')
        self.assertEqual(self.game_manager.board.get_cell(2, 1), '-')
        self.assertEqual(self.game_manager.board.get_cell(2, 2), '-')
        self.assertEqual(self.game_manager.board.get_cell(2, 3), ' ')
        self.assertEqual(self.game_manager.board.get_cell(3, 1), ' ')

        self.game_manager.add_move(2, 3, 'X')
        self.game_manager.add_move(2, 6, 'O')
        self.game_manager.add_move(3, 1, 'O')
        self.game_manager.add_move(5, 5, 'X')
        self.game_manager.add_move(6, 2, 'X')
        self.assertEqual(self.game_manager.move_computer_easy('O'), (4, 3))
        self.assertEqual(self.game_manager.last_move_by, 'O')
        self.assertEqual(self.game_manager.move_computer_easy('O'), (None, None))

    def test_game_over(self):
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(5, 5, 'X')
        self.game_manager.board.border_move(5, 5, 1)
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(2, 2, 'O')
        self.game_manager.board.border_move(2, 2, 1)
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(2, 5, 'X')
        self.game_manager.board.border_move(2, 5, 1)
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(4, 3, 'O')
        self.game_manager.board.border_move(4, 3, 1)
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(4, 1, 'O')
        self.game_manager.board.border_move(4, 1, 1)
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(6, 3, 'O')
        self.game_manager.board.border_move(6, 3, 1)
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(6, 1, 'X')
        self.assertTrue(self.game_manager.game_over())
        print(str(self.game_manager.board))

    def tearDown(self) -> None:
        print("TORE DOWN!")
