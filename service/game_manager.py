import random

from domain.board import Board
from domain.validaors import AddMoveException


class GameManager:
    def __init__(self, board, validator):
        self.board = board
        self.move_validator = validator
        self.last_move_by = None

    def set_board_size(self, lines, columns):
        self.board = Board(lines, columns)

    def add_move(self, line, column, value):
        self.move_validator.validate(self.board, line, column)
        self.board.set_cell(line, column, value)
        self.board.border_move(line, column, 1)
        self.last_move_by = value

    def move_computer_easy(self, value):
        """

        :param value:
        :return:
        """
        for line in range(1, self.board.lines + 1):
            for column in range(1, self.board.columns + 1):
                if self.board.get_cell(line, column) == ' ':
                    self.board.set_cell(line, column, value)
                    self.board.border_move(line, column, 1)
                    self.last_move_by = value
                    return line, column
        return None, None

    def move_computer_medium(self, value):
        """

        """
        while True:
            line = random.randint(1, self.board.lines)
            column = random.randint(1, self.board.lines)
            if self.board.get_cell(line, column) == ' ':
                self.add_move(line, column, value)
                return line, column

    def move_computer_hard(self, value):
        """

        """

        ''' strategy for board size: odd x odd'''
        board_size = self.board.lines * self.board.columns
        middle_line = self.board.lines // 2 + 1
        middle_column = self.board.columns // 2 + 1
        if board_size % 2 == 1:
            if self.board.spaces_left() == board_size:
                self.add_move(middle_line, middle_column, value)
            else:
                for line in range(1, self.board.lines + 1):
                    for column in range(1, self.board.columns + 1):
                        if self.board.get_cell(line, column) not in [' ', '-', value]:
                            # means self.board.get_cell(line,column) == opposite sign of value
                            if self.board.get_cell(line - middle_line, column - middle_column) == ' ':
                                self.add_move(line - middle_line, column - middle_column, value)
                                return line, column
                            else:
                                return self.move_computer_easy(value)
                        else:
                            return self.move_computer_easy(value)
        else:
            return self.move_computer_easy(value)
        '''
        copy_board = Board(self.board.lines, self.board.columns)
        for line in range(1, copy_board.lines + 1):
            for column in range(1, copy_board.lines + 1):
                value = self.board.get_cell(line, column)
                copy_board.set_cell(line, column, value)
        stack = []
        solution = (None, None)

        def backtracking(is_computer_turn):
            for line in range(1, copy_board.lines + 1):
                for column in range(1, copy_board.lines + 1):
                    stack.append((line, column))
                    if copy_board.get_cell(line, column) == ' ':  # if partial solution
                        copy_board.set_cell(line, column, value)
                        copy_board.border_move(line, column, 1)
                        if copy_board.spaces_left() == 0 and is_computer_turn is True:  # if total solution
                            return stack[0][0], stack[0][1]
                        elif copy_board.spaces_left() == 0 and is_computer_turn is False:
                            return self.move_computer_easy(value)
                        else:
                            backtracking(not is_computer_turn)
                    else:
                        continue

        solution = backtracking(True)

        if solution == (None, None):
            solution = self.move_computer_easy(value)
        try:
            self.add_move(solution[0], solution[1])
        except AddMoveException as ame:
            print('medium mode error', ame)
        return solution
        '''

    def game_over(self):
        if self.board.spaces_left() == 0:
            return True
        else:
            return False
