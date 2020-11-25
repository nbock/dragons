from game import *
from CSP import *
import itertools

ROWS = 9
COLS = 9
MINES = 10

# NOTE TO SELF (NOLAN): might need to initilaize the board with position
def model():
    csp = CSP()

    variables = list()
    board = Board(ROWS, COLS, MINES)

    # initialize the domains
    for row in range(ROWS):
        temp_row = list()
        for col in range(COLS):
            # name = str(row) + " " + str(col)
            if board.is_flag(row, col):
                domain = [1]
            elif board.is_show(row, col):
                domain = [0]
            else:
                domain = [0, 1]
            var = Variable(domain)
            temp_row.append(var)
            csp.add_variable(var)
        variables.append(temp_row)

    # initialize the constraints
    constraints = list()
    unassigned = list()

    for row in range(ROWS):
        for col in range(COLS):
            if board.is_show(row, col):
                variables[row][col].assign(0)
            elif board.is_flag(row, col):
                variables[row][col].assign(1)
            else:
                unassigned.append(variables[row][col])

            # below is broken
            if board.is_show(row, col): # does this need to check value is 0?
                surrounding = board.get_surrounding(row, col)
                scope = list()
                sum1 = board[row][col][0]
                for sur in surrounding:
                    if board.is_flag()
