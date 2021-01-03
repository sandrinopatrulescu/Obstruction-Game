from texttable import Texttable


class Board:
    def __init__(self, lines, columns):
        self.lines = lines
        self.columns = columns
        self._data = [[' '] * self.columns for i in range(self.lines)]

    def set_board_size(self, lines, columns):
        """
        modify the current size of the board
        :param lines: an integer between 1 and very much
        :param columns: an integer between 1 and very much
        :return: no return, board size is modified
        """
        self.__init__(lines, columns)

    def set_cell(self, line, column, value):
        """
        set the a a cell given by line and column to a certain value
        :param line: integer between 1 and self.lines
        :param column: integer between 1 and self.columns
        :param value: usually 'X', 'O', '-' or ' '
        :return: no return
        """
        self._data[line - 1][column - 1] = value

    def get_cell(self, line, column):
        """
        return the value of a cell given by line and column
        :param line: integer between 1 and self.lines
        :param column: integer between 1 and self.columns
        :return: string - the value of the cell at given line and column
        """
        return self._data[line - 1][column - 1]
    
    def border_move(self, center_line, center_column, radius, value):
        """
        replace empty cells at a given distance from a given point on the board with a given value
        :param center_line: an integer between 1 and self.lines
        :param center_column: an integer between 1 and self.columns
        :param radius: an integer between 1 and at most [(self.lines ** 2 + self.columns ** 2) ** (1/2) - 1]
        :param value: string '-' when used for adding player/computer moves
        :return: nothing, just updates the game board
        """
        for column_displacement in range(-radius, radius + 1):
            if center_line - radius in range(1, self.lines + 1):
                if center_column + column_displacement in range(1, self.columns + 1):
                    if self.get_cell(center_line - radius, center_column + column_displacement) == ' ':
                        self.set_cell(center_line - radius, center_column + column_displacement, value)
            if center_line + radius in range(1, self.lines + 1):
                if center_column + column_displacement in range(1, self.columns + 1):
                    if self.get_cell(center_line + radius, center_column + column_displacement) == ' ':
                        self.set_cell(center_line + radius, center_column + column_displacement, value)
        for line_displacement in range(-radius, radius + 1):
            if center_line + line_displacement in range(1, self.lines + 1):
                if center_column - radius in range(1, self.columns + 1):
                    if self.get_cell(center_line + line_displacement, center_column - radius) == ' ':
                        self.set_cell(center_line + line_displacement, center_column - radius, value)
            if center_line + line_displacement in range(1, self.lines + 1):
                if center_column + radius in range(1, self.columns + 1):
                    if self.get_cell(center_line + line_displacement, center_column + radius) == ' ':
                        self.set_cell(center_line + line_displacement, center_column + radius, value)

    def spaces_left(self):
        """
        calculate how many free positions are left
        :return: the number of free positions
        """
        spaces_left = 0
        for line in range(1, self.lines + 1):
            for column in range(1, self.columns + 1):
                if self.get_cell(line, column) == ' ':
                    spaces_left = spaces_left + 1
        return spaces_left

    def __str__(self):
        """
        turn the board into a string, to use it for printing
        :return: a string which contains the string version of the table
        """
        table = Texttable()
        for line in range(self.lines):
            table.add_row(self._data[line])
        return table.draw()
