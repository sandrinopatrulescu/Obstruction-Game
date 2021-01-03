import unittest

from domain.board import Board
from domain.validators import MoveValidator, AddMoveException
from service.game_manager import GameManager


class TestGameManager(unittest.TestCase):
    def setUp(self) -> None:
        move_validator = MoveValidator()
        self.game_manager = GameManager(Board(6, 6), move_validator)

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
        self.assertRaises(AddMoveException, self.game_manager.move_computer_easy, 'O')

    def test_computer_medium(self):
        current_spaces_left = self.game_manager.board.spaces_left()
        while self.game_manager.game_over() is False:
            line, column = self.game_manager.move_computer_medium('O')
            self.assertNotEqual(current_spaces_left, self.game_manager.board.spaces_left())
            current_spaces_left = self.game_manager.board.spaces_left()
            if 1 <= line - 1 <= self.game_manager.board.lines and 1 <= column - 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line - 1, column - 1), '-')
            if 1 <= line - 1 <= self.game_manager.board.lines and 1 <= column + 0 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line - 1, column + 0), '-')
            if 1 <= line - 1 <= self.game_manager.board.lines and 1 <= column + 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line - 1, column + 1), '-')
            if 1 <= line + 0 <= self.game_manager.board.lines and 1 <= column - 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 0, column - 1), '-')
            if 1 <= line + 0 <= self.game_manager.board.lines and 1 <= column + 0 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 0, column + 0), 'O')
            if 1 <= line + 0 <= self.game_manager.board.lines and 1 <= column + 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 0, column + 1), '-')
            if 1 <= line + 1 <= self.game_manager.board.lines and 1 <= column - 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 1, column - 1), '-')
            if 1 <= line + 1 <= self.game_manager.board.lines and 1 <= column + 0 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 1, column + 0), '-')
            if 1 <= line + 1 <= self.game_manager.board.lines and 1 <= column + 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 1, column + 1), '-')
        self.assertRaises(AddMoveException, self.game_manager.move_computer_medium, 'O')

    def test_move_computer_hard(self):
        current_spaces_left = self.game_manager.board.spaces_left()
        while self.game_manager.game_over() is False:
            line, column = self.game_manager.move_computer_hard('X')
            self.assertNotEqual(current_spaces_left, self.game_manager.board.spaces_left())
            current_spaces_left = self.game_manager.board.spaces_left()
            if 1 <= line - 1 <= self.game_manager.board.lines and 1 <= column - 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line - 1, column - 1), '-')
            if 1 <= line - 1 <= self.game_manager.board.lines and 1 <= column + 0 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line - 1, column + 0), '-')
            if 1 <= line - 1 <= self.game_manager.board.lines and 1 <= column + 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line - 1, column + 1), '-')
            if 1 <= line + 0 <= self.game_manager.board.lines and 1 <= column - 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 0, column - 1), '-')
            if 1 <= line + 0 <= self.game_manager.board.lines and 1 <= column + 0 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 0, column + 0), 'X')
            if 1 <= line + 0 <= self.game_manager.board.lines and 1 <= column + 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 0, column + 1), '-')
            if 1 <= line + 1 <= self.game_manager.board.lines and 1 <= column - 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 1, column - 1), '-')
            if 1 <= line + 1 <= self.game_manager.board.lines and 1 <= column + 0 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 1, column + 0), '-')
            if 1 <= line + 1 <= self.game_manager.board.lines and 1 <= column + 1 <= self.game_manager.board.columns:
                self.assertEqual(self.game_manager.board.get_cell(line + 1, column + 1), '-')

        self.game_manager.board.set_board_size(11, 15)
        line, column = self.game_manager.move_computer_hard('O')
        self.assertEqual(line, 6)
        self.assertEqual(column, 8)
        self.assertEqual(self.game_manager.board.get_cell(5, 7), '-')
        self.assertEqual(self.game_manager.board.get_cell(5, 8), '-')
        self.assertEqual(self.game_manager.board.get_cell(5, 9), '-')
        self.assertEqual(self.game_manager.board.get_cell(6, 7), '-')
        self.assertEqual(self.game_manager.board.get_cell(6, 8), 'O')
        self.assertEqual(self.game_manager.board.get_cell(6, 9), '-')
        self.assertEqual(self.game_manager.board.get_cell(7, 7), '-')
        self.assertEqual(self.game_manager.board.get_cell(7, 8), '-')
        self.assertEqual(self.game_manager.board.get_cell(7, 9), '-')

        while not self.game_manager.game_over():
            line_player_move, column_player_move = self.game_manager.move_computer_medium('X')
            line, column = self.game_manager.move_computer_hard('O')
            # print(line_player_move, column_player_move)
            # print(line, column)
            # print(str(self.game_manager.board))
            self.assertEqual(self.game_manager.board.get_cell(2 * 6 - line_player_move, 2 * 8 - column_player_move), self.game_manager.board.get_cell(line, column))
        self.assertRaises(AddMoveException, self.game_manager.move_computer_hard, 'O')

    def test_game_over(self):
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(5, 5, 'X')
        self.game_manager.board.border_move(5, 5, 1, '-')
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(2, 2, 'O')
        self.game_manager.board.border_move(2, 2, 1, '-')
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(2, 5, 'X')
        self.game_manager.board.border_move(2, 5, 1, '-')
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(4, 3, 'O')
        self.game_manager.board.border_move(4, 3, 1, '-')
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(4, 1, 'O')
        self.game_manager.board.border_move(4, 1, 1, '-')
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(6, 3, 'O')
        self.game_manager.board.border_move(6, 3, 1, '-')
        self.assertFalse(self.game_manager.game_over())
        self.game_manager.board.set_cell(6, 1, 'X')
        self.assertTrue(self.game_manager.game_over())
        print(str(self.game_manager.board))

    def tearDown(self) -> None:
        print("TORE DOWN!")
