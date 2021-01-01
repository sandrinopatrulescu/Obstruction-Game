from texttable import Texttable


class Board:
    def __init__(self, lines, columns):
        self.lines = lines
        self.columns = columns
        self._data = [[' '] * self.columns for i in range(self.lines)]

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
    
    def border_move(self, center_line, center_column, radius):
        for column_displacement in range(-radius, radius + 1):
            if center_line - radius in range(1, self.lines + 1):
                if center_column + column_displacement in range(1, self.columns + 1):
                    if self.get_cell(center_line - radius, center_column + column_displacement) == ' ':
                        self.set_cell(center_line - radius, center_column + column_displacement, '-')
            if center_line + radius in range(1, self.lines + 1):
                if center_column + column_displacement in range(1, self.columns + 1):
                    if self.get_cell(center_line + radius, center_column + column_displacement) == ' ':
                        self.set_cell(center_line + radius, center_column + column_displacement, '-')
        for line_displacement in range(-radius, radius + 1):
            if center_line + line_displacement in range(1, self.lines + 1):
                if center_column - radius in range(1, self.columns + 1):
                    if self.get_cell(center_line + line_displacement, center_column - radius) == ' ':
                        self.set_cell(center_line + line_displacement, center_column - radius, '-')
            if center_line + line_displacement in range(1, self.lines + 1):
                if center_column + radius in range(1, self.columns + 1):
                    if self.get_cell(center_line + line_displacement, center_column + radius) == ' ':
                        self.set_cell(center_line + line_displacement, center_column + radius, '-')

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
