from domain.board import Board
from domain.validaors import AddMoveException


class Cli:
    difficulties = {'easy': 'game_service.move_computer_easy',
                    'medium': 'game_service.move_computer_medium',
                    'hard': 'game_service.move_computer_hard'}

    def __init__(self, manager):
        self.game_service = manager

    def start_console(self):

        print("     Available commands (commands are case sensitive):")
        print("         quit - quit the game")
        print("         board size m x n  - default size is 6 x 6 (m x n integers, m, n >= 1)")
        print("         vs human/computer easy/computer medium/computer hard - choose difficulty")
        print("         name player O/X -name- - choose names")
        print("         play [X/O] - play vs human or choose difficulty if playing vs computer")
        print("         end - ends the current session")
        print()

        players = {
            'O': {'number': 1, 'name': 'Player 1', 'function': 'game_service.add_move', 'status': 'empty'},
            'X': {'number': 2, 'name': 'Player 2', 'function': 'game_service.add_move', 'status': 'empty'}}
        mode = {'against computer': False, 'difficulty': 'human'}
        while True:
            print()
            print()
            print()
            print("O name: {}".format(players['O']['name']))
            print('X name: {}'.format(players['X']['name']))
            print('vs computer: {}, difficulty: {}'.format(mode['against computer'], mode['difficulty']))
            print('board size: {} x {}'.format(self.game_service.board.lines, self.game_service.board.columns))
            user_command = input(">").strip()
            if user_command == 'quit':
                print('bye')
                return
            elif user_command.find('board size') == 0:
                arguments = user_command.split(' ')
                if arguments[0] == 'board' and arguments[1] == 'size' and len(arguments) == 5:
                    if arguments[3] != 'x':
                        print("Invalid command")
                    lines = arguments[2]
                    columns = arguments[4]
                    try:
                        lines = int(lines)
                        columns = int(columns)
                        if lines < 1 or columns < 1:
                            print("Sizes must be greater or equal to 1")
                        self.game_service.set_board_size(lines, columns)
                        if self.game_service.board.lines == lines and self.game_service.board.columns == columns:
                            print("Board size was set!")
                    except ValueError:
                        print("Size must be int over int")
                else:
                    print("Invalid command")
            elif user_command.find('vs') == 0:
                arguments = user_command.split(' ')
                if arguments[0] == 'vs' and len(arguments) == 2:
                    if arguments[1] == 'human':
                        mode['against computer'] = False
                        mode['difficulty'] = 'human'
                elif arguments[0] == 'vs' and len(arguments) == 3:
                    if arguments[1] == 'computer':
                        if arguments[2] == 'easy':
                            mode['against computer'] = True
                            mode['difficulty'] = arguments[2]  # 'easy'
                        elif arguments[2] == 'medium':
                            mode['against computer'] = True
                            mode['difficulty'] = arguments[2]  # 'medium'
                        elif arguments[2] == 'hard':
                            mode['against computer'] = True
                            mode['difficulty'] = arguments[2]  # 'hard'
                        else:
                            print("Invalid command!")
                    else:
                        print("Invalid command!")
                else:
                    print("Invalid command!")
            elif user_command.find('name') == 0:
                arguments = user_command.split(' ')
                if arguments[0] != 'name':
                    print("Invalid command")
                if arguments[1] == 'O':
                    players['O']['name'] = arguments[2]
                elif arguments[1] == 'X':
                    players['X']['name'] = arguments[2]
                else:
                    print("Invalid command")
            elif user_command.find('play') == 0:
                arguments = user_command.split(' ')
                if arguments[0] == 'play':
                    if len(arguments) == 1:
                        if mode['against computer'] is False:
                            mode['difficulty'] = 'human'
                            players['O']['status'] = 'human'
                            players['O']['function'] = 'game_service.add_move'
                            players['X']['status'] = 'human'
                            players['X']['function'] = 'game_service.add_move'
                            self.start_game(players)
                        else:
                            print("Error: Against computer you must specify if you want to play as O or X")
                    elif len(arguments) == 2:
                        if mode['against computer'] is False:
                            print("Error: Against human you don't have to specify if you want to play as O as X")
                        else:
                            if arguments[1] == 'O':
                                players['O']['status'] = 'human'
                                players['O']['function'] = 'game_service.add_move'
                                players['X']['status'] = 'computer'
                                players['X']['function'] = self.difficulties[mode['difficulty']]
                                self.start_game(players)
                            elif arguments[1] == 'X':
                                players['O']['status'] = 'computer'
                                players['O']['function'] = self.difficulties[mode['difficulty']]
                                players['X']['status'] = 'human'
                                players['X']['function'] = 'game_service.add_move'
                                self.start_game(players)
                            else:
                                print("Invalid command")
                    else:
                        print("Invalid command")
                else:
                    print("Invalid command")
            else:
                print("Invalid command")

    def start_game(self, players):
        turn = 'O'
        while not self.game_service.game_over():
            print('start test', turn)
            print(str(self.game_service.board))
            print("It's {}'s turn!".format(players[turn]['name']))
            if players[turn]['status'] == 'human':
                user_command = input(">").strip()
                if user_command == 'end':
                    print("Game session ended")
                    return
                else:
                    arguments = user_command.split(' ')
                    if len(arguments) == 3 and arguments[0] == 'move':
                        try:
                            line = int(arguments[1])
                            column = int(arguments[2])
                            if line in range(1, self.game_service.board.lines + 1) and column in range(1, self.game_service.board.columns + 1):

                                try:
                                    # move_function = eval("self." + players[turn]['function'])
                                    # move_function(line, column, turn)
                                    self.game_service.add_move(line, column, turn)
                                    if self.game_service.board.get_cell(line, column) == turn:
                                        print(players[turn]['name'] + ' put {} at {}, {}'.format(turn, line, column))
                                    if turn == 'O':
                                        turn = 'X'
                                    elif turn == 'X':
                                        turn = 'O'
                                except AddMoveException as ame:
                                    print(ame)
                            else:
                                print("Line and/or column of out of the board")
                        except ValueError:
                            print("Line and column must be integers")
                    else:
                        print("Invalid command")
            elif players[turn]['status'] == 'computer':
                move_function = eval('self.' + players[turn]['function'])
                line, column = move_function(turn)
                if line and column:
                    print(players[turn]['name'] + ' put {} at {}, {}'.format(turn, line, column))
                if turn == 'O':
                    turn = 'X'
                elif turn == 'X':
                    turn = 'O'
        if self.game_service.last_move_by == 'O':
            print("{} won!".format(players['O']['name']))
        else:
            print("{} won!".format(players['X']['name']))
        self.game_service.board = Board(self.game_service.board.lines, self.game_service.board.columns)
