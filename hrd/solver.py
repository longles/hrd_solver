import heapq
from collections import deque
from .board import Board


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
                if board.hash_key() not in visited:
                    visited.add(board.hash_key())
                    stack.append(board)
                    parent[board] = curr_board

        solution = deque([])
        while True:
            solution.appendleft(f'{curr_board.hash_key()}\n\n')
            if curr_board == initial:
                break
            curr_board = parent[curr_board]
            
        with open(output_file, 'w') as f:
            f.write(f'Cost of the solution: {len(solution) - 1}\n')
            for b in solution:
                f.write(b)


    def a_star(self, output_file: str):
        visited = set()
        costs = {self.board: 0}
        parent = {self.board: None}
        pq = [(0, id(self.board), self.board)]
        initial = curr_board = self.board

        while len(pq) > 0:
            curr_board = heapq.heappop(pq)[2]
            if curr_board.is_solved():
                break
            
            for board in curr_board.get_next_boards():
                if board.hash_key() not in visited:
                    visited.add(board.hash_key())
                    new_cost = costs[curr_board] + 1  # every move costs 1
                    if board not in costs or new_cost < costs[board]:
                        heapq.heappush(pq, (new_cost + self.heuristic(board), id(board), board))
                        costs[board] = new_cost
                        parent[board] = curr_board

        solution = deque([])
        while True:
            solution.appendleft(f'{curr_board.hash_key()}\n\n')
            if curr_board == initial:
                break
            curr_board = parent[curr_board]
            
        with open(output_file, 'w') as f:
            f.write(f'Cost of the solution: {len(solution) - 1}\n')
            for b in solution:
                f.write(b)


def manhattan_distance(board: Board):
    for piece in board.pieces:
        if piece.name == '1':   
            piece_pos = piece.curr_coords[3]
            return abs(4 - piece_pos[0]) + abs(2 - piece_pos[1])  # (4, 2) is bottom right coord of the solution

    return 0  # should never get here


# manhattan + number of pieces in the solution area
def advanced_heuristic(board: Board):
    man_dist = manhattan_distance(board)
    num_in_sol = 0
    
    for piece in board.pieces:
        for coord in piece.curr_coords:
            if coord in {(4, 1), (4, 2), (3, 1), (3, 2)}:
                num_in_sol += 1
                break
    
    return man_dist + num_in_sol
