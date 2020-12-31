

class Cli:

    def __init__(self, manager):
        self.game_service = manager
        self.players = {'O': {'number': 1, 'name': 'Player1', 'function': 'game_service.add_move', 'status': 'free'},
                        'X': {'number': 2, 'name': 'Player2', 'function': 'game_service.add_move', 'status': 'free'}}

    def start_console(self):
        print("     Available commands (commands are case sensitive):")
        print("         quit")
        print("         board size lines x columns (n x n, n >= 1)")
        print("         vs human/computer easy/computer medium/computer hard")
        print("         name player O/X -name-")
        print("         play")
        print()
        print()
        is_computer = {}
        while True:
            user_command = input(">").strip()
            if user_command == 'quit':
                print('bye')
                return
            elif user_command.find('board size') == 0:
                arguments = user_command.split(' ')
                if arguments[0] != 'board':
                    print("Invalid command")
                if arguments[0] != 'size':
                    print("Invalid command")
                if arguments[3] != 'x':
                    print("Invalid command")
                width = arguments[2]
                length = arguments[4]
                try:
                    width = int(width)
                    length = int(length)
                except ValueError:
                    print("Size must be int over int")
                if width < 1 or length < 1:
                    print("Sizes must be greater or equal to 1")
                if width != length:
                    print("Size must be of -n x n- form")
            elif user_command.find('vs'):
                arguments = user_command.split(' ')
                if arguments[0] != 'vs':
                    print("Invalid command")
                if arguments[1] == 'human' and len(arguments) == 2:
                    self.players['O']['function'] = 'game_manager.add_move'
                    self.players['X']['function'] = 'game_manager.add_move'
                elif arguments[1] == 'computer' and len(arguments) == 3:
                    if arguments[2] == 'easy':
                        pass
                    elif arguments[2] == 'medium':
                        pass
                    elif arguments[2] == 'hard':
                        pass
                    else:
                        print("Invalid command!")
                else:
                    print("Invalid command!")
            elif user_command.find('name') == 0:
                arguments = user_command.split(' ')
                if arguments[0] != 'name':
                    print("Invalid command")
            elif user_command == 'play':
                self.start_game()
            else:
                print("Invalid command")

    def start_game(self):
        '''
        print board
        get user command
        convert it for execution
        execute
        check if game over

        commands:
        vs human
        vs computer

        '''
        player = self.players['O']['number']
        while not self.game_service.game_over():
            print(str(self.game_service.board))
            user_command = 1

