from queue import PriorityQueue
from .board import Board
from dataclasses import dataclass, field
from collections import deque


# For use in the priority queue
@dataclass(order=True)
class PriorityBoard:
    priority: int
    board: Board=field(compare=False)

    def __init__(self, priority, board) -> None:
        self.priority = priority
        self.board = board


class Solver:
    def __init__(self, board) -> None:
        self.board = board
        self.heuristic = manhattan_distance

        
    def dfs(self, output_file: str):
        visited = set()
        parent = {self.board: None}
        stack = [self.board]
        initial = curr_board = self.board

        while len(stack) > 0:
            curr_board = stack.pop()
            if curr_board.is_solved():
                break
            for board in curr_board.get_next_boards():
                if board not in visited:
                    visited.add(board)
                    stack.append(board)
                    parent[board] = curr_board

        solution = deque([])
        while True:
            solution.appendleft(str(curr_board) + '\n')
            if curr_board == initial:
                break
            curr_board = parent[curr_board]

        with open(output_file, 'w') as f:
            f.write(f'Cost of the solution: {len(solution) - 1}\n')
            for b in solution:
                f.write(str(b))


    def a_star(self, output_file: str):
        visited = set()
        costs = {self.board: 0}
        parent = {self.board: None}
        pq = PriorityQueue()
        pq.put(PriorityBoard(0, self.board))
        initial = curr_board = self.board

        while not pq.empty():
            curr_board = pq.get().board
            if curr_board.is_solved():
                break
            for board in curr_board.get_next_boards():
                if board not in visited:
                    visited.add(board)
                    new_cost = costs[curr_board] + 1  # every move costs 1
                    if board not in costs or new_cost < costs[board]:
                        costs[board] = new_cost
                        priority = new_cost + self.heuristic(board)
                        pq.put(PriorityBoard(priority, board))
                        parent[board] = curr_board

        solution = deque([])
        while True:
            solution.appendleft(str(curr_board) + '\n')
            if curr_board == initial:
                break
            curr_board = parent[curr_board]

        with open(output_file, 'w') as f:
            f.write(f'Cost of the solution: {len(solution) - 1}\n')
            for b in solution:
                f.write(str(b))


def manhattan_distance(board: Board):
    for piece in board.pieces:
        if piece.name == '1':
            piece_pos = piece.curr_coords[3]
            return abs(4 - piece_pos[0]) + abs(2 - piece_pos[1])  # (4, 2) is bottom right coord of the solution
    return 0


def heuristic_2():
    raise NotImplementedError
