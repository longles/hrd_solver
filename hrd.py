import sys
from hrd.board import Board
from hrd.solver import Solver


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Incorrect number of arguments!')
        print('Usage: hrd.py [input_file] [dfs_output_file] [a_star_output_file]')
        exit(1)

    input_file = sys.argv[1]
    dfs_output_file = sys.argv[2]
    a_star_output_file  = sys.argv[3]

    board = Board()
    board.generate_board_and_pieces(input_file)
    solver = Solver(board)

    solver.dfs(dfs_output_file)
    solver.a_star(a_star_output_file)
