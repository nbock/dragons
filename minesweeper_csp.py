'''
Construct and return minesweeper CSP models.
'''

from csp import *
import itertools
import propagators


def minesweeper_csp_model(initial_mine_board):
    '''
    Return a CSP object representing a minesweeper game.

    The input mine field would be represented by a list of lists of integers.
    An example mine field:
       -------------------
       |0|0|1|0|3|0|0|4|0|
       |1|2|2|3|0|4|0|0|2|
       |0|2|0|2|1|2|3|3|2|
       |2|3|2|2|1|0|1|0|1|
       |0|1|2|0|2|0|1|1|1|
       |1|1|2|0|2|0|0|0|0|
       -------------------

    And the solution should look something like this:
       -------------------
       | | |1|*|3|*|*|4|*|
       |1|2|2|3|*|4|*|*|2|
       |*|2|*|2|1|2|3|3|2|
       |2|3|2|2|1| |1|*|1|
       |*|1|2|*|2| |1|1|1|
       |1|1|2|*|2| | | | |
       -------------------
    '''
    variables = []
    variable_array = []
    for i in range(0, len(initial_mine_board)):
        row = []
        for j in range(0, len(initial_mine_board[0])):
            if initial_mine_board[i][j] == 0:
                variable = Variable("V({},{})".format(i, j), [" ", "*"])
            else:
                variable = Variable("V({},{})".format(i, j), [initial_mine_board[i][j]])
            variables.append(variable)
            row.append(variable)
        variable_array.append(row)
    reduce(variable_array, initial_mine_board)
    mine_csp = CSP("Minesweeper", variables)

    # add constraints here
    for i in range(0, len(variable_array)):
        for j in range(0, len(variable_array[0])):
            if initial_mine_board[i][j] != 0:
                constraint = Constraint("C{},{}".format(i, j), get_variables_around(i, j, variable_array))

                domain = []
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if not (k == 0 and l == 0) and 0 <= (i + k) < len(variable_array) and 0 <= (j + l) < len(variable_array[0]):
                            domain.append(variable_array[i + k][j + l].cur_domain())
                holder = [0 for i in range(len(domain))]
                sat_tuples = []
                recursive_sat(domain, holder, sat_tuples, initial_mine_board[i][j])
                constraint.add_satisfying_tuples(sat_tuples)
                mine_csp.add_constraint(constraint)

    return mine_csp, variable_array


def reduce(table, initial):
    for i in range(0, len(initial)):
        for j in range(0, len(initial[0])):
            if initial[i][j] == 0 and no_indicator(initial, i, j):
                table[i][j].prune_value("*")


def no_indicator(initial, i, j):
    for k in range(-1, 2):
        for l in range(-1, 2):
            if 0 <= (i + k) < len(initial) and 0 <= (j + l) < len(initial[0]):
                if initial[i + k][j + l] !=0:
                    return False
    return True


def get_variables_around(i, j, table):
    array = []
    for k in range(-1, 2):
        for l in range(-1, 2):
            if not(k == 0 and l == 0) and 0 <= (i + k) < len(table) and 0 <= (j + l) < len(table[0]):
                array.append(table[i + k][j + l])
    return array


def recursive_sat(domain, holder, sat_tuples, value):
    if len(domain) == 1:
        for item in domain[0]:
            holder[len(holder) - 1] = item
            count = 0
            for i in holder:
                if i == "*":
                    count += 1
            if count == value:
                sat_tuples.append(list(holder))
    else:
        temp = domain.pop(0)
        for item in temp:
            holder[len(holder) - 1 - len(domain)] = item
            recursive_sat(list(domain), list(holder), sat_tuples, value)
