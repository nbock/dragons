from CSP import *
import itertools

ROWS = 9
COLS = 9
MINES = 10

# TODO: NOTE TO SELF (NOLAN): might need to initilaize the board with position
# ...now I think I might want to remove it
def model(board):
    csp = CSP()

    variables = list()

    # initialize the domains
    for row in range(ROWS):
        temp_row = list()
        for col in range(COLS):
            name = str(row) + " " + str(col)
            if board.is_flag(row, col):
                domain = [1]
            elif board.is_show(row, col):
                domain = [0]
            else:
                domain = [0, 1]
            var = Variable(name, domain)
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
            if board.is_show(row, col) and not board.get_value(row, col) == 0:
                surrounding = board.get_surrounding(row, col)
                scope = list()
                sum1 = board.get_value(row, col)
                for neighbor in surrounding:
                    # checks the flag status
                    if neighbor[2]:
                        sum1 -= 1
                    if not neighbor[1] and not neighbor[2]:
                        # if hidden and not flagged
                        scope.append(variables[row][col])
                name = str(row) + " " + str(col)
                if scope:
                    constraints.append([scope, sum1])

        # Not sure if we need this so didn't implement remaining mines
        """
        if len(unassigned) <= 20:
            constraints.append(["endgame", unassigned, board.remaining_mines])
        """

        # sort by length of scope
        constraints.sort(key=lambda x: len(x[0]))

        # Add a new constraint if two constraints have at least two same vars
        # Create a new variable for the overlap
        for i in range(len(constraints) - 1):
            con1 = constraints[i]
            for j in range(i+1, len(constraints)):
                con2 = constraints[j]
                if set(con1[0]) == set(con2[1]):
                    continue
                if set(con1[0]) & set(con2[0]) == set(con1[0]):
                    con2[0] = list(set(con2[0]).difference(set(con1[0])))
                    con2[1] = con2[1] - con1[1]

        # sort constraints by length of scope (again)
        constraints.sort(key=lambda x: len(x[0]))

        # overlap the constraints
        ol_cons = list()
        ol_set = list()
        ol_var = list()

        # Add new constraints if two constraints have at least two same variables in scope
        for i in range(len(constraints) - 1):
            con1 = constraints[i]
            for j in range(i + 1, len(constraints)):
                con2 = constraints[j]
                if set(con1[0]) == set(con2[0]):
                    ol_vars = set(con1[0]) & set(con2[0])
                    con1_vars = set(con1[0]) - ol_vars
                    con2_vars = set(con2[0]) - ol_vars
                    con1_sum = con1[1]
                    con2_sum = con2[1]
                    name = ""

                    if not ol_vars in ol_set:
                        for i in ol_vars:
                            name += i.name + ", "
                        name = "(" + name + ")"
                        var = Variable(list(range(len(ol_vars)+1)))
                        csp.add_var(var)
                        ol_var.append(var)
                        ol_set.append(ol_vars)
                    else:
                        index = ol_set.index(ol_vars)
                        var = ol_var[index]

                    con1_vars.add(var)
                    con2_vars.add(var)
                    ol_cons.append(["", list(con1_vars), con1_sum])
                    ol_cons.append(["", list(con2_vars), con2_sum])

        constraints.extend(ol_cons)

        for con in constraints:
            constraint = Constraint(con[0])
            tuples = satisfy_tuples(con[0], con[1])
            constraint.add_satisfying_tuples(tuples)
            csp.add_constraint(constraint)

        return csp


def satisfy_tuples(scope, sum1):
    product_list = list()

    for variable in scope:
        product_list.append(variable.domain)

    product = list(itertools.product(*product_list))
    tuples = list()

    for tuple in product:
        if sum(tuple) == sum1:
            tuples.append(tuple)

    return tuples
