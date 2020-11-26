"""
Board class for a Minesweeper board
-1 represents a mine
An integer represents mines surrounding an x,y point

An array of tuples is meant to represent the board: (adjacent_mines, hidden_status, flag_status)

adjacent_mines can be -1, 0, 1, 2, 3
visbility_status can be True if the square is visible and False otherwise
flag_status can be True if there is a flag on the current square and False otherwise
pos is the x,y position of the current tile

Nolan Bock - 10/26/20
"""

import random
from CSP import *
from propagators import *

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
        self.board = [[(0, False, False, (i, j)) for i in range(rows)] for j in range(cols)]

        # assign the mines to random locations, needs to be a set to make sure 10 are assigned
        mine_points = set()
        while len(mine_points) != self.mines:
            x = random.randint(0, rows - 1)
            y = random.randint(0, cols - 1)
            mine_points.add((x, y))
            self.board[x][y] = (-1, self.board[x][y][1], self.board[x][y][2], (x, y))

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

                self.board[row][col] = (mines, self.board[row][col][1], False, (row, col))

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
        # if we already revealed it or have it marked as a flag
        if self.is_show(row, col) or self.is_flag(row, col):
            return

        # Case: hits a non-mine
        self.show(row, col)
        if self.is_mine():
            self.gameover(row, col)

        # Case: hits a free space, we show all empty neighbors from here
        elif self.board[row][col][0] == 0:
            tiles = [self.board[row][col]]
            while tiles:
                temp_tile = tiles.pop()
                surrounding = self.get_surrounding(temp_tile[3][0], temp_tile[3][1])
                for neighbor in surrounding:
                    row = neighbor[3][0]
                    col = neighbor[3][1]
                    if not self.is_show(row, col) and neighbor[0] == 0:
                        tiles.append(neighbor)
                    self.show(row, col)

        # Did we win?
        if self.is_win():
            self.gameover()


    def gameover(self, row=None, col=None):
        self.is_over = True
        # we won, baby
        if row == None and col == None:
            print("You won! Hell ya!")
        else:
            print("You lost!")
            print("Hit mine on (" + str(row) + ", " + str(col) + ").")

    def show(self, row, col):
        self.board[row][col] = (self.board[row][col][0], True, self.board[row][col][2], self.board[row][col][3])

    def is_show(self, row, col):
        return self.board[row][col][1]

    def is_mine(self, row, col):
        return self.board[row][col][0] == -1

    def flag(self, row, col):
        """
        Flags the input row and column
        """
        self.board[row][col][2] = True

    def is_flag(self, row, col):
        """
        Boolean representing if the current location is marked with a is_flag
        """
        return self.board[row][col][2]

    def is_show(self, row, col):
        """
        Boolean representing if the current location is revealed
        """
        return self.board[row][col][0] >= 0 and self.board[row][col][1] == True

    def is_loss(self):
        """
        Terminal state evaluation, returns if the current state is a losing state

        :return: a boolean representing if the current state is a loss or not
        """
        for row in range(self.rows):
            for col in range(self.cols):
                # if we uncovered a mine, we lost
                if self.board[row][col][0] == -1 and self.board[row][col][1]:
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
                if self.board[row][col][0] != -1 and not self.board[row][col][1]:
                    return False

        # if not, game is won
        return True

    def get_surrounding(self, row, col):
        """
        Gets the surrounding tiles to be updated
        """
        surrounding = ((-1, -1), (-1,  0), (-1,  1),
                       (0 , -1),           (0 ,  1),
                       (1 , -1), (1 ,  0), (1 ,  1))

        neighbors = list()

        for pos in surrounding:
            temp_row = row + pos[0]
            temp_col = col + pos[1]
            if 0 <= temp_row < self.rows and 0 <= temp_col < self.cols:
                neighbors.append(self.board[temp_row][temp_col])

        return neighbors

    def solve(self):
        """
        Solve the game (we hope)
        """
        if self.is_loss() or self.is_win():
            return

        for row in range(self.rows):
            for col in range(self.cols):
                # make sure everything is unflagged
                if self.is_flag(row, col):
                    self.board[row][col] = (self.board[row][col][0], self.board[row][col][1], False, self.board[row][col][3])

        while not self.is_loss() and not self.is_win():
            assigned = self.solve_step()
            if not assigned:
                choice = self.guess_move() # need to make sure this returns correctly
                self.reveal(choice) # need to make sure this returns correctly

    def solve_step(self):
        is_assigned = False

        csp = CSP.model(self)

        solver = BT(csp)
        solver.bt_search_MS(prop_GAC)
        for var in csp.get_vars():


    # TODO: CLARA AND NOLAN DISCUSS: do we need an update surrounding? I think how we hide or show value naturally does this
    def update_surrounding(self, row, col):
        """
        Update the surrounding values adding the passed in value to the current
        """
        cells = self.get_surrounding(row, col)
        # for now does nothing pending if we need this
        # formerly, it updated the surrounding values
        # I took value out of the parameters, too

    def show(self):
        """
        Pretty prints the rows of the board for inspection

        :return: nothing
        """
        for i in range(self.rows):
            print(self.board[i])


# some tests meant to show functionality, should be deleted eventually
b = Board(9, 9, 10)
b.show()
b.reveal(2, 1)
print()
b.show()

print(b.is_loss())
print(b.is_win())
