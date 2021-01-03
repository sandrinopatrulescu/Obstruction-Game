import random
from copy import deepcopy

from domain.validators import AddMoveException


class GameManager:
    def __init__(self, board, validator):
        self.board = board
        self.move_validator = validator
        self.last_move_by = None

    def add_move(self, line, column, value):
        """
        add, and validate, a new move, given by its value and its position, to the game board
        :param line: an integer between 1 and self.board.lines
        :param column: an integer between 1 and self.board.columns
        :param value: either 'O' or 'X'
        :return: no return
        """
        self.move_validator.validate(self.board, line, column)
        self.board.set_cell(line, column, value)
        self.board.border_move(line, column, 1, '-')
        self.last_move_by = value

    def move_computer_easy(self, value):
        """
        put the value on the first place available on the board
        :param value: a string -'X' or 'O'
        :return: a tuple consisting of the position where the computer made the move
        """
        for line in range(1, self.board.lines + 1):
            for column in range(1, self.board.columns + 1):
                try:
                    self.add_move(line, column, value)
                    return line, column
                except AddMoveException:
                    pass
        raise AddMoveException("It shouldn't arrive at move_computer when board if full. Most probably caused by lack "
                               "of game over verification at the start of the game loop")

    def move_computer_medium(self, value):
        """
        put the value on a random place on the board
        :param value: a string -'X' or 'O'
        :return: a tuple consisting of the position where the computer made the move
        """
        while True:
            line = random.randint(1, self.board.lines)
            column = random.randint(1, self.board.lines)
            try:
                self.add_move(line, column, value)
                return line, column
            except AddMoveException:
                pass
            # code won't be reached, but for extra protection
            if self.game_over() is True:
                raise AddMoveException(
                    "It shouldn't arrive at move_computer when board if full. Most probably caused by lack "
                    "of game over verification at the start of the game loop")

    def move_computer_hard(self, value):
        """
        when board size is odd and computer is first, it starts putting the value in the middle and then
        mirrors with respect to the middle every move made by the player
        when it's not the case the computer will move using move_computer_medium instead
        """
        ''' strategy for board size: odd x odd'''
        board_size = self.board.lines * self.board.columns
        middle_line = self.board.lines // 2 + 1
        middle_column = self.board.columns // 2 + 1
        if board_size % 2 == 1:
            if self.board.spaces_left() == board_size:
                self.add_move(middle_line, middle_column, value)
                return middle_line, middle_column
            else:
                for line in range(1, self.board.lines + 1):
                    for column in range(1, self.board.columns + 1):
                        if self.board.get_cell(line, column) not in [' ', '-', value]:
                            # means self.board.get_cell(line,column) == opposite sign of value
                            if self.board.get_cell(2 * middle_line - line, 2 * middle_column - column) == ' ':
                                self.board.set_cell(2 * middle_line - line, 2 * middle_column - column, value)
                                self.board.border_move(2 * middle_line - line, 2 * middle_column - column, 1, '-')
                                self.last_move_by = value
                                return 2 * middle_line - line, 2 * middle_column - column
                return self.move_computer_medium(value)
        else:
            return self.move_computer_medium(value)

    def game_over(self):
        """
        check if the board is full (meaning no ' ' left on the board) and return a truth value
        :return: boolean True/False - board full/board not full
        """
        if self.board.spaces_left() == 0:
            return True
        else:
            return False


'''
recursion limit exceeded
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
                copy_board.border_move(line, column, 1, '-')
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
