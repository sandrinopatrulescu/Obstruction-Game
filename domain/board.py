from texttable import Texttable


class Board:
    def __init__(self, size):
        self.size = size
        self._data = [[' '] * self.size for i in range(self.size)]

    def set_cell(self, line, column, value):
        self._data[line - 1][column - 1] = value

    def get_cell(self, line, column):
        return self._data[line - 1][column - 1]

    def __str__(self):
        table = Texttable()
        for line in range(self.size):
            table.add_row(self._data[line])
        return table.draw()
