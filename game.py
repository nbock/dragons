"""
Board class for a Minesweeper board
-1 represents a mine
An integer represents mines surrounding an x,y point

An array of tuples is meant to represent the board: (adjacent_mines, hidden_status)

adjacent_mines can be -1, 0, 1, 2, 3
hidden_status can be True if the square is visible and False otherwise

Nolan Bock - 10/26/20
"""

import random


class Board:
    """
    Board class represents a Minesweeper board
    """
    def __init__(self, rows, cols, mines):
        """
        Initializes the board based on rows, cols, and number of mines

        :param rows: an int, the number of rows
        :param cols: an int, the number of columns
        :param mines: an int, the number of mines
        """
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.board = [[(0, False) for i in range(rows)] for j in range(cols)]

        # assign the mines to random locations, needs to be a set to make sure 10 are assigned
        mine_points = set()
        while len(mine_points) != self.mines:
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)
            mine_points.add((x, y))
            self.board[x][y] = (-1, self.board[x][y][1])

        # iterate through points, assigning numeric values to non-mine locations
        for row in range(rows):
            for col in range(cols):
                if self.board[row][col][0] == -1:
                    continue

                mines = 0

                # left
                if self.check(row, col - 1):
                    mines += 1
                # right
                if self.check(row, col + 1):
                    mines += 1
                # up left
                if self.check(row - 1, col - 1):
                    mines += 1
                # up
                if self.check(row - 1, col):
                    mines += 1
                # up right
                if self.check(row - 1, col + 1):
                    mines += 1
                # down left
                if self.check(row + 1, col - 1):
                    mines += 1
                # down
                if self.check(row + 1, col):
                    mines += 1
                # down right
                if self.check(row + 1, col + 1):
                    mines += 1

                self.board[row][col] = (mines, self.board[row][col][1])

    def check(self, to_row, to_col):
        """
        Check is a helper function to the initializer

        :param to_row: an int, the row we're verifying exists in this board
        :param to_col: a column, the col we're verying exists in this board
        :return: A boolean representing if the row, col exists in the board
        """
        return 0 <= to_row < self.rows and 0 <= to_col < self.cols and self.board[to_row][to_col][0] == -1

    def reveal(self, row, col):
        """
        Reveals a square on the board

        :param row: an int, the row of the square to reveal
        :param col: an int, the col of the square to reveal
        :return: nothing
        """
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.board[row][col] = (self.board[row][col][0], True)

    def is_loss(self):
        """
        Terminal state evaluation, returns if the current state is a losing state

        :return: a boolean representing if the current state is a loss or not
        """
        for row in range(self.rows):
            for col in range(self.cols):
                # if we uncovered a mine, we lost
                if self.board[row][col][0] == -1 and not self.board[row][col][1]:
                    return True

        return False

    def is_win(self):
        """
        Terminal state evaluation, returns if the current state is a winning state

        :return: a boolean representing if the current state is a win or not
        """
        # if we are on a losing condition, we have not won
        if self.is_loss():
            return False

        for row in range(self.rows):
            for col in range(self.cols):
                # if any non-mine is not uncovered, game is not won
                if self.board[row][col][0] != -1 and self.board[row][col][1]:
                    return False

        # if not, game is won
        return True

    def show(self):
        """
        Pretty prints the rows of the board for inspection

        :return: nothing
        """
        for i in range(self.rows):
            print(self.board[i])


# some tests meant to show functionality, should be deleted eventually
'''
b = Board(9, 9, 10)
b.show()
b.reveal(2, 1)
print()
b.show()

print(b.is_loss())
print(b.is_win())
'''
