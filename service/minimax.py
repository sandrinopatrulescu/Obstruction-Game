from copy import deepcopy
from functools import reduce
'''
http://www.lkozma.net/game.html
https://en.wikipedia.org/wiki/Nim#Proof_of_the_winning_formula
http://www.papg.com/article?HDT
'''

print(reduce(lambda x, y: x + y, [1]))
nim_values = {0: 0, 1: 1, 2: 1, 3: 2, 4: 0, 5: 3}


# table[type][size] = nim-value
nim_values_table = {'bar': {0: 0, 1: 1},
                    'square': {1: 1, 2: 1}}
# for table[square][2] : the successors of a square with size 2 are : 0, nim of 0 is 0 and mex(0) = 1


def nim_of_board_calculator(board):
    if board.type in nim_values_table.keys():
        if board.size in nim_values_table[board.type].keys():
            return nim_values_table[board.type][board.size]
        else:
            successors = []
            if board.type == 'bar':
                if board.size == 0:
                    nim_values_table[board.type][board.size] = 0
                    return nim_values_table[board.type][board.size]
                elif board.size == 1:
                    nim_values_table[board.type][board.size] = 1
                    return nim_values_table[board.type][board.size]
                if board.size >= 2:
                    successor = BoardPartition()
                    successor.type = board.type
                    successor.size = board.size - 2
                    successors.append(successor)

            elif board.type == 'square':
                pass

"""
nim_of_board_calculator(board):
    if board.type in nim_values_table.keys():
    if board.size in nim_values_table[board.type].keys():
        return nim_values_table[board.type][board.size]
    else:
        successors = []

"""

    if board in nim_values.keys():
        return nim_values[board]
    else:
        successors = []
        if board == 0:
            nim_values[0] = 0
            return 0
        if board == 1:
            nim_values[1] = 1
            return 1
        if board - 2 >= 0:
            successors.append(board - 2)
        if board - 3 >= 0:
            successors.append(board - 3)
        for a in range(1, (board - 3) // 2 + 1):
            b = board - 3 - a
            if b in range(1, board - 3):
                successors.append('{}+{}'.format(a, b))
        minimum_excluded_value = 0
        maximum = -1
        nim_of_successors = set()
        for successor in successors:
            # print('board:', board)
            # print('sucs:', successors)
            if isinstance(successor, int):
                nim_value = nim_of_board_calculator(successor)
                # print('suc:', successor, 'nim:', nim_value)
                nim_of_successors.add(nim_value)
                if nim_value > maximum:
                    maximum = nim_value
            elif isinstance(successor, str):
                plus_index = successor.find('+')
                first_number = int(successor[0:plus_index])
                second_number = int(successor[plus_index + 1:])
                nim_value = nim_of_board_calculator(first_number) ^ nim_of_board_calculator(second_number)
                nim_of_successors.add(nim_value)
                if nim_value > maximum:
                    maximum = nim_value
        for minimum_excluded_value in range(0, maximum + 2):
            if minimum_excluded_value not in nim_of_successors:
                # print('mex and nims:', minimum_excluded_value, nim_of_successors)
                nim_values[board] = minimum_excluded_value
                return minimum_excluded_value


for index in range(0, 41):
    print(index, nim_of_board_calculator(index))


class BoardPartition:
    pass


def color(board, line, column, k, board_partition):
    board.set_cell(line, column, k)

    board_partition.size = board_partition.size + 1
    board_partition.list.append((line, column))
    if line not in board_partition.lines_dictionary.keys():
        board_partition.lines_dictionary[line] = [column]
    else:
        board_partition.lines_dictionary[line].append(column)
    if column not in board_partition.columns_dictionary.keys():
        board_partition.columns_dictionary[column] = [line]
    else:
        board_partition.columns_dictionary[column].append(line)

    if board.get_cell(line - 1, column) == ' ':
        color(board, line - 1, column, k, board_partition)
    if board.get_cell(line, column + 1) == ' ':
        color(board, line, column + 1, k, board_partition)
    if board.get_cell(line + 1, column) == ' ':
        color(board, line + 1, column, k, board_partition)
    if board.get_cell(line, column - 1) == ' ':
        color(board, line, column - 1, k, board_partition)


def determine_type(board_partition):
    # TODO: complete
    if len(board_partition.lines_dictionary) == 1 or len(board_partition.columns_dictionary) == 1:
        return 'bar'


def convert_to_board_partitions(board):
    board_partitions = []
    # board_partitions.append = BoardPartition()
    k = 0
    for line in range(1, board.lines + 1):
        for column in range(1, board.columns + 1):
            if board.get_cell(line, column) == ' ':
                board_partition = BoardPartition()
                board_partition.size = 0
                board_partition.color = k
                board_partition.list = []
                board_partition.lines_dictionary = {}
                board_partition.columns_dictionary = {}
                color(board, line, column, k, board_partition)
                for line_of_dictionary in board_partition.lines_dictionary.keys():
                    sorted(board_partition.lines_dictionary[line_of_dictionary])
                for column_of_dictionary in board_partition.columns_dictionary.keys():
                    sorted(board_partition.columns_dictionary[column_of_dictionary])
                board_partition.type = determine_type(board_partition)
                board_partitions.append(board_partition)
                k = k + 1
    return board_partitions


def nim_sum(board_partitions):
    if len(board_partitions) == 0:
        raise AddMoveException(
            "It shouldn't arrive at move_computer when board if full. Most probably caused by lack "
            "of game over verification at the start of the game loop")
    nim_value = reduce(lambda partition1, partition2: nim_of_board_calculator(partition1) ^ nim_of_board_calculator(partition2), board_partitions)
    return nim_value


def next_move(board, value):
    for line in range(1, board.lines + 1):
        for column in range(1, board.columns + 1):
            if board.get_cell(line, column) == ' ':
                copy_board = deepcopy(board)
                copy_board.set_cell(line, column, value)
                board_partitions = convert_to_board_partitions(board)
                # board_partitions - a list consisting of all current available
                if nim_sum(board_partitions) != 0:
                    return line, column


'''
nim_values = {0: 0, 1: 1, 2: 1, 3: 2, 4: 0, 5: 3}

def nim_value_calculator(board):
    if board in nim_values.keys():
        return nim_values[board]
    else:
        successors = []
        if board == 0:
            nim_values[0] = 0
            return 0
        if board == 1:
            nim_values[1] = 1
            return 1
        if board - 2 >= 0:
            successors.append(board - 2)
        if board - 3 >= 0:
            successors.append(board - 3)
        for a in range(1, (board - 3) // 2 + 1):
            b = board - 3 - a
            if b in range(1, board - 3):
                successors.append('{}+{}'.format(a,b))
        minimum_excluded_value = 0
        maximum = -1
        nim_of_successors = set()
        for successor in successors:
            #print('board:', board)
            #print('sucs:', successors)

            if isinstance(successor, int):
                nim_value = nim_value_calculator(successor)
                #print('suc:', successor, 'nim:', nim_value)
                nim_of_successors.add(nim_value)
                if nim_value > maximum:
                    maximum = nim_value
            elif isinstance(successor, str):
                plus_index = successor.find('+')
                first_number = int(successor[0:plus_index])
                second_number = int(successor[plus_index + 1:])
                nim_value = nim_value_calculator(first_number) ^ nim_value_calculator(second_number)
                nim_of_successors.add(nim_value)
                if nim_value > maximum:
                    maximum = nim_value
        for minimum_excluded_value in range(0, maximum + 2):
            if minimum_excluded_value not in nim_of_successors:
                #print('mex and nims:', minimum_excluded_value, nim_of_successors)
                nim_values[board] = minimum_excluded_value
                return minimum_excluded_value
for index in range(0, 41):
    print(index, nim_value_calculator(index))
'''