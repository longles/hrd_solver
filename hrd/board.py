WIDTH = 4
HEIGHT = 5


def idx_to_coord(idx: int) -> tuple:
    r = idx // WIDTH
    c = idx % WIDTH
    return (r, c)


def get_board(pieces):
    board = [['0'] * WIDTH for _ in range(HEIGHT)]
    for piece in pieces:
        for r, c in piece.curr_coords:
            board[r][c] = piece.name
    return board


class Piece:
    def __init__(self, name, curr_coords) -> None:
        self.name = name
        self.curr_coords = curr_coords


    def __eq__(self, other):
        return self.name == other.name and set(self.curr_coords) == set(other.curr_coords)


    def get_possible_moves(self, board: list) -> list:
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        return [self.move_piece(dir) for dir in directions if self.is_valid_move(board, dir)]


    def is_valid_move(self, board: list, move: tuple) -> bool:
        for r, c in self.curr_coords:
            new_coord = (r + move[0], c + move[1])
            if not (0 <= new_coord[0] < HEIGHT and 0 <= new_coord[1] < WIDTH):
                return False 
            if board[new_coord[0]][new_coord[1]] not in {'0', self.name if self.name != '7' else '0'}:
                return False
        return True


    def move_piece(self, move: tuple):
        new_coords = [(r + move[0], c + move[1]) for r, c in self.curr_coords]
        return Piece(self.name, new_coords)

 
class Board:
    def __init__(self, pieces = []) -> None:
        self.pieces = pieces
        self.board = get_board(pieces)


    def hash_key(self):
        def orientation(piece: Piece):
            if piece.name not in {'1', '7'}:
                c1 = piece.curr_coords[0] 
                c2 = piece.curr_coords[1]
                if (abs(c1[0] - c2[0]), abs(c1[1] - c2[1])) == (1, 0):
                    return '3'  # up
                else:
                    return '2'  # side
            elif piece.name == '7':
                return '4'
            else:
                return '1'

        b = [['0'] * WIDTH for _ in range(HEIGHT)]
        for piece in self.pieces:
            for r, c in piece.curr_coords:
                b[r][c] = orientation(piece)

        return '\n'.join(''.join(p for p in c) for c in b)


    def generate_board_and_pieces(self, board_file: str):
        def dict_add(d, k, v):
            if k in d:
                d[k].append(v)
            else:
                d[k] = [v]

        curr_idx = 0
        piece_coords = {}
        board = [['0'] * WIDTH for _ in range(HEIGHT)]
        pieces = []

        with open(board_file) as f:
            for line in f.readlines():
                for char in line:
                    if char != '\n':  # artifact while reading txt lines
                        dict_add(piece_coords, char, idx_to_coord(curr_idx))
                        curr_idx += 1
        
            for name, idx_list in piece_coords.items():
                if name != '0':
                    if name == '7':
                        for coord in idx_list:
                            pieces.append(Piece(name, [coord]))
                    else:
                        pieces.append(Piece(name, idx_list))
                for r, c in idx_list:
                    board[r][c] = name
                    
            self.board = board
            self.pieces = pieces


    def get_next_boards(self):
        next_boards = []
        for piece in self.pieces:
            for next_piece in piece.get_possible_moves(self.board):
                next_boards.append(self.make_move(piece, next_piece))
        return next_boards


    def make_move(self, curr_piece, dst_piece):
        new_pieces = self.pieces.copy()
        for i in range(len(new_pieces)):
            if new_pieces[i] == curr_piece:
                new_pieces[i] = dst_piece
                return Board(new_pieces)


    def is_solved(self):
        return self.board[4][1] == '1' and self.board[4][2] == '1'
