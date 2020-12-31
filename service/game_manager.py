

class GameManager:
    def __init__(self, board, validator):
        self.board = board
        self.move_validator = validator
        self.last_move_by = None

    def border_move(self, center_line, center_column, radius):
        for column_displacement in range(-radius, radius + 1):
            if center_line - radius in range(1, self.board.size + 1):
                if center_column + column_displacement in range(1, self.board.size + 1):
                    if self.board.get_cell(center_line - radius, center_column + column_displacement) == ' ':
                        self.board.set_cell(center_line - radius, center_column + column_displacement, '-')
            if center_line + radius in range(1, self.board.size + 1):
                if center_column + column_displacement in range(1, self.board.size + 1):
                    if self.board.get_cell(center_line + radius, center_column + column_displacement) == ' ':
                        self.board.set_cell(center_line + radius, center_column + column_displacement, '-')
        for line_displacement in range(-radius, radius + 1):
            if center_line + line_displacement in range(1, self.board.size + 1):
                if center_column - radius in range(1, self.board.size + 1):
                    if self.board.get_cell(center_line + line_displacement, center_column - radius) == ' ':
                        self.board.set_cell(center_line + line_displacement, center_column - radius, '-')
            if center_line + line_displacement in range(1, self.board.size + 1):
                if center_column + radius in range(1, self.board.size + 1):
                    if self.board.get_cell(center_line + line_displacement, center_column + radius) == ' ':
                        self.board.set_cell(center_line + line_displacement, center_column + radius, '-')

    def add_move(self, line, column, value):
        self.move_validator.validate(self.board, line, column)
        self.board.set_cell(line, column, value)
        self.border_move(line, column, 1)
        self.last_move_by = value

    def game_over(self):
        spaces_left = 0
        for line in range(1, self.board.size + 1):
            for column in range(1, self.board.size + 1):
                if self.board.get_cell(line, column) == ' ':
                    spaces_left = spaces_left + 1
        if spaces_left == 0:
            return True
        return False
