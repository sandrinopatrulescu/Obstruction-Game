from domain.exceptions import GameManagerException


class AddMoveException(GameManagerException):
    pass


class MoveValidator(object):
    @staticmethod
    def validate(board, line, column):
        if line not in range(1, board.size + 1):
            raise AddMoveException("Line exceeds board size!")
        if column not in range(1, board.size + 1):
            raise AddMoveException("Column exceeds board size!")
        if board.get_cell(line, column) == '-':
            raise AddMoveException("Cannot move on shadow block!")
        if board.get_cell(line, column) != ' ':
            raise AddMoveException("Place already used!")
