'''
Board for a 9x9 Minesweeper board
X represents a mine
An integer represents mines surrounding an x,y point
'''

import random

rows = 9
cols = 9
board = [[(0, True) for i in range(rows)] for j in range(cols)]

mine_points = set()
while len(mine_points) != 10:
    x = random.randint(0, rows - 1)
    y = random.randint(0, cols - 1)
    mine_points.add((x, y))
    board[x][y] = (-1, True)

for row in range(rows):
    for col in range(cols):
        mines = 0
        if board[min(rows - 1, row + 1)][col][0] == -1:
            mines += 1
        if board[max(0, row - 1)][col][0] == -1:
            mines += 1
        if board[row][min(cols - 1, col + 1)][0] == -1:
            mines += 1
        if board[row][max(0, col - 1)][0] == -1:
            mines += 1

        if board[row][col][0] != -1:
            board[row][col] = (mines, board[row][col][1])

for i in range(rows):
    print(board[i])
