DEFAULT_WIDTH = 10  # Default width of Tetris board

class TetrisGame:
    '''
    A simulator for Tetris that takes in Tetris pieces and positions, and return the height of the board at any point.
    - Pieces are rigid and comes to rest if bottom touches bottom of board or any existing piece
    - If an entire row is filled, it disappears and higher rows drop to fill the space, but without changes in any internal structure in any row    
    '''
    pieces = {
        'Q': [
            [1,1],
            [1,1]
        ],
        'Z': [
            [1,1,0],
            [0,1,1]
        ],
        'S' : [
            [0,1,1],
            [1,1,0]
        ],
        'T' : [
            [1,1,1],
            [0,1,0]
        ],
        'I' : [
            [1,1,1,1]
        ],
        'L' : [
            [1,0],
            [1,0],
            [1,1]
        ],
        'J' : [
            [0,1],
            [0,1],
            [1,1]
        ]
    }

    def __init__(self, board_width=DEFAULT_WIDTH):
        '''
        Constructor

        Args:
            board_width (int): width of the board
        '''
        self.board = []     # The board as a list of rows, each row is a list of 0 and 1s representing empty and block respectively. Higher rows are appended to the end of this list.
        self.board_width = board_width
        self.heights = [0] * board_width    # Height of each column (1-based)

    def add(self, piece, pos, board=None, heights=None):
        '''
        Adds piece `piece` to the board, at position where leftmost block is at column index `pos`, and return new board

        Args:
            piece (str): capital letter representing the piece type
            pos (int): column index of leftmost block of the piece
            board (list of list of int): current board, used for testing
            heights (list of int): height of each column (1-based), used for testing
        '''
        board = board[::-1] if board is not None else self.board
        piece = self.pieces[piece]
        H, W = len(piece), len(piece[0])
        row = self._lock(piece, pos, heights=heights)

        # Add additional rows
        for i in range(row+1-len(board)):
            board.append([0]*self.board_width)

        # Update board
        for i in range(H):
            for j in range(W):
                if piece[i][j] == 1:
                    board[row-i][pos+j] = 1
                    self.heights[pos+j] = max(self.heights[pos+j], row-i+1)

        # Clear full rows
        i = row - H + 1
        for _ in range(H):  # We only need to check rows occupied by the newly added piece
            if all([x == 1 for x in board[i]]):
                board.pop(i)
                self.heights = [x-1 for x in self.heights]
            else:
                i += 1

        return board[::-1]
    
    def get_height(self, board=None):
        '''
        Return the height of the current board

        Args:
            board (list of list of int): current board, used for testing
        '''
        if board is None:
            board = self.board
        return len(board)
    
    def _lock(self, piece, pos, heights=None):
        '''
        Return the row index of the top of the piece after it lands

        Args:
            piece (list of list of int): shape of the piece
            pos (int): column index of the leftmost block of the piece
            heights (list of int): height of each column (1-based), used for testing
        '''
        if heights is None:
            heights = self.heights
        H, W = len(piece), len(piece[0])
        lowest = [None] * W
        for col in range(W):
            lowest[col] = max([row for row in range(H) if piece[row][col] == 1])  # row index of lowest 1 in each column of `piece`, can cache this value if pieces are large

        # The row index of the top of the piece after it lands is the largest row index of each column landing individually
        return max([heights[pos+col] + lowest[col] for col in range(W)])