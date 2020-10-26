'''
Board for a 9x9 Minesweeper board
X represents a mine
An integer represents mines surrounding an x,y point

An array of tuples is meant to represent the board: (adjacent_mines, hidden_status)

adjacent_mines can be -1, 0, 1, 2, 3
hidden_status can be True if the square is covered and False otherwise
'''

import random

rows = 9
cols = 9
board = [[(0, True) for i in range(rows)] for j in range(cols)]


def check(curr_row, curr_col, to_row, to_col):
    '''

    :param curr_row:
    :param curr_col:
    :param to_row:
    :param to_col:
    :return:
    '''
    return to_row >= 0 and to_col >= 0 and to_row < rows and to_col < cols and board[to_row][to_col][0] == -1


mine_points = set()
while len(mine_points) != 10:
    x = random.randint(0, rows - 1)
    y = random.randint(0, cols - 1)
    mine_points.add((x, y))
    board[x][y] = (-1, True)



for row in range(rows):
    for col in range(cols):
        if board[row][col][0] == -1:
            continue

        mines = 0

        # comparing bounded row and column

        # left
        if check(row, col, row, col - 1):
            mines += 1

        # right
        if check(row, col, row, col + 1):
            mines += 1

        # up left
        if check(row, col, row - 1, col - 1):
            mines += 1
        # up
        if check(row, col, row - 1, col):
            mines += 1
        # up right
        if check(row, col, row - 1, col + 1):
            mines += 1

        # down left
        if check(row, col, row + 1, col - 1):
            mines += 1

        # down
        if check(row, col, row + 1, col):
            mines += 1

        # down right
        if check(row, col, row + 1, col + 1):
            mines += 1

        board[row][col] = (mines, board[row][col][1])


# just for seeing the board
for i in range(rows):
    print(board[i])
