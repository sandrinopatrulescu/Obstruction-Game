import unittest

from texttable import Texttable

from domain.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(6, 6)

    def test_init(self):
        self.assertEqual(self.board.lines, 6)
        self.assertEqual(self.board.columns, 6)
        for line in range(1, self.board.lines + 1):
            for column in range(1, self.board.columns + 1):
                self.assertEqual(self.board.get_cell(line, column), ' ')

    def test_set_board_size(self):
        self.board.set_board_size(5, 5)
        self.assertTrue(self.board.get_cell(5, 5), ' ')
        self.assertRaises(IndexError, self.board.get_cell, 6, 6)

    def test_get_cell(self):
        self.assertEqual(self.board.get_cell(1, 1), ' ')
        self.assertEqual(self.board.get_cell(2, 5), ' ')
        self.assertEqual(self.board.get_cell(6, 6), ' ')

    def test_set_cell(self):
        for line in range(1, self.board.lines + 1):
            for column in range(1, self.board.columns + 1):
                if column % 4 == 0:
                    self.board.set_cell(line, column, 'X')
                if column % 4 == 1:
                    self.board.set_cell(line, column, 'O')
                if column % 4 == 2:
                    self.board.set_cell(line, column, '-')
                if column % 4 == 3:
                    self.board.set_cell(line, column, ' ')
        for line in range(1, self.board.lines + 1):
            for column in range(1, self.board.columns + 1):
                if column % 4 == 0:
                    self.assertEqual(self.board.get_cell(line, column), 'X')
                if column % 4 == 1:
                    self.assertEqual(self.board.get_cell(line, column), 'O')
                if column % 4 == 2:
                    self.assertEqual(self.board.get_cell(line, column), '-')
                if column % 4 == 3:
                    self.assertEqual(self.board.get_cell(line, column), ' ')

    def test_str(self):
        row = [' '] * self.board.columns
        for index in range(1, self.board.columns + 1):
            if index % 4 == 0:
                row[index - 1] = 'X'
            if index % 4 == 1:
                row[index - 1] = 'O'
            if index % 4 == 2:
                row[index - 1] = '-'
            if index % 4 == 3:
                row[index - 1] = ' '
        table = Texttable()
        for index in range(self.board.lines):
            table.add_row(row)

        for line in range(1, self.board.lines + 1):
            for column in range(1, self.board.columns + 1):
                if column % 4 == 0:
                    self.board.set_cell(line, column, 'X')
                if column % 4 == 1:
                    self.board.set_cell(line, column, 'O')
                if column % 4 == 2:
                    self.board.set_cell(line, column, '-')
                if column % 4 == 3:
                    self.board.set_cell(line, column, ' ')

        self.assertEqual(str(self.board), table.draw())

    def test_border_move(self):
        self.board.set_cell(1, 1, 'X')
        self.board.border_move(1, 1, 1, '-')
        self.assertTrue(self.board.get_cell(1, 1), 'X')
        self.assertTrue(self.board.get_cell(1, 2), '-')
        self.assertTrue(self.board.get_cell(2, 1), '-')
        self.assertTrue(self.board.get_cell(2, 2), '-')
        self.assertTrue(self.board.get_cell(1, 3), ' ')
        self.assertTrue(self.board.get_cell(2, 3), ' ')
        self.assertTrue(self.board.get_cell(2, 3), ' ')
        self.assertTrue(self.board.get_cell(3, 1), ' ')
        self.assertTrue(self.board.get_cell(3, 2), ' ')
        self.assertTrue(self.board.get_cell(3, 3), ' ')

        self.board.set_cell(2, 5, 'O')
        self.board.border_move(2, 5, 1, '-')
        self.assertTrue(self.board.get_cell(1, 4), '-')
        self.assertTrue(self.board.get_cell(1, 5), '-')
        self.assertTrue(self.board.get_cell(1, 6), '-')
        self.assertTrue(self.board.get_cell(2, 4), '-')
        self.assertTrue(self.board.get_cell(2, 5), 'O')
        self.assertTrue(self.board.get_cell(2, 6), '-')
        self.assertTrue(self.board.get_cell(3, 4), '-')
        self.assertTrue(self.board.get_cell(3, 5), '-')
        self.assertTrue(self.board.get_cell(3, 6), '-')

        self.board.set_cell(5, 4, 'X')
        self.board.border_move(5, 4, 1, '-')
        self.assertTrue(self.board.get_cell(4, 3), '-')
        self.assertTrue(self.board.get_cell(4, 4), '-')
        self.assertTrue(self.board.get_cell(4, 5), '-')
        self.assertTrue(self.board.get_cell(5, 3), '-')
        self.assertTrue(self.board.get_cell(5, 4), 'X')
        self.assertTrue(self.board.get_cell(5, 5), '-')
        self.assertTrue(self.board.get_cell(6, 3), '-')
        self.assertTrue(self.board.get_cell(6, 4), '-')
        self.assertTrue(self.board.get_cell(6, 5), '-')

    def test_spaces_left(self):
        self.assertEqual(self.board.spaces_left(), 36)
        self.board.set_cell(2, 2, 'X')
        self.assertEqual(self.board.spaces_left(), 35)
        self.board.set_cell(3, 3, 'O')
        self.assertEqual(self.board.spaces_left(), 34)
        self.board.set_cell(6, 6, '-')
        self.assertEqual(self.board.spaces_left(), 33)

    def tearDown(self):
        print("TORE DOWN!")
