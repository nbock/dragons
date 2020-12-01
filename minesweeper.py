from minesweeper_csp import *
from propagators import *
from game import *

def print_solution(var_array):
    for row in var_array:
        print([var.get_assigned_value() for var in row])


if __name__ == "__main__":
    #the amount of tests to be run
    test_count = 1

    #board size
    height = 16
    width = 16
    depth = 0
    step = 3

    while test_count > 0:
        board, field = mine_board_generator(height, width)
        print("Solving board: ")
        for row in board:
            print(row)
        print("Using Board Model")
        csp, var_array = minesweeper_csp_model(board)
        solver = BT(csp)
        print("=======================================================")
        print("GAC")
        solver.bt_search(prop_GAC)
        print("Solution")
        print_solution(var_array)

        answer = []
        for row in var_array:
            new_row = []
            for item in row:
                new_row.append(item.assignedValue)
            answer.append(new_row)

        if(answer == field):
            print("Answer is correct!")
        else:
            print("Answer is wrong!")

        test_count = test_count - 1
        height += step
        width += step*2
        depth += step*3
