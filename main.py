from domain.board import Board
from domain.validators import MoveValidator
from service.game_manager import GameManager
from ui.cli import Cli

if __name__ == '__main__':
    board = Board(6, 6)
    move_validator = MoveValidator()
    game_manager = GameManager(board, move_validator)
    console = Cli(game_manager)
    console.start_console()
