import unittest

from texttable import Texttable

from domain.board import Board


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board(6)

    def test_init(self):
        self.assertEqual(self.board.size, 6)
        for line in range(1, self.board.size + 1):
            for column in range(1, self.board.size + 1):
                self.assertEqual(self.board.get_cell(line, column), ' ')

    def test_get_cell(self):
        self.assertEqual(self.board.get_cell(1, 1), ' ')
        self.assertEqual(self.board.get_cell(2, 5), ' ')
        self.assertEqual(self.board.get_cell(6, 6), ' ')

    def test_set_cell(self):
        for line in range(1, self.board.size + 1):
            for column in range(1, self.board.size + 1):
                if column % 4 == 0:
                    self.board.set_cell(line, column, 'X')
                if column % 4 == 1:
                    self.board.set_cell(line, column, 'O')
                if column % 4 == 2:
                    self.board.set_cell(line, column, '-')
                if column % 4 == 3:
                    self.board.set_cell(line, column, ' ')
        for line in range(1, self.board.size + 1):
            for column in range(1, self.board.size + 1):
                if column % 4 == 0:
                    self.assertEqual(self.board.get_cell(line, column), 'X')
                if column % 4 == 1:
                    self.assertEqual(self.board.get_cell(line, column), 'O')
                if column % 4 == 2:
                    self.assertEqual(self.board.get_cell(line, column), '-')
                if column % 4 == 3:
                    self.assertEqual(self.board.get_cell(line, column), ' ')

    def test_str(self):
        row = [' '] * self.board.size
        for index in range(1, self.board.size + 1):
            if index % 4 == 0:
                row[index - 1] = 'X'
            if index % 4 == 1:
                row[index - 1] = 'O'
            if index % 4 == 2:
                row[index - 1] = '-'
            if index % 4 == 3:
                row[index - 1] = ' '
        table = Texttable()
        for index in range(self.board.size):
            table.add_row(row)

        for line in range(1, self.board.size + 1):
            for column in range(1, self.board.size + 1):
                if column % 4 == 0:
                    self.board.set_cell(line, column, 'X')
                if column % 4 == 1:
                    self.board.set_cell(line, column, 'O')
                if column % 4 == 2:
                    self.board.set_cell(line, column, '-')
                if column % 4 == 3:
                    self.board.set_cell(line, column, ' ')

        self.assertEqual(str(self.board), table.draw())

    def tearDown(self):
        print("TORE DOWN!")
