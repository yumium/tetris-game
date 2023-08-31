

# Additional Notes

Just wanted to make a few additional comments on performance here.

I ran a line-by-line profiler on the `TetrisGame` class on a large sequence of `'Q0,Q2,Q4,Q6' * int(1E5) + 'Q8' * int(1E5 / 4)`

Below is the per-line breakdown:

```
Timer unit: 1e-06 s

Total time: 10.9243 s
File: TetrisGame.py
Function: add at line 52

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================

    52                                               @profile
    53                                               def add(self, piece, pos):
    54                                                   '''
    55                                                   Adds piece `piece` to the board, at position where leftmost block is at column index `pos`
    56                                           
    57                                                   Args:
    58                                                       piece (str): capital letter representing the piece type
    59                                                       pos (int): column index of leftmost block of the piece
    60                                                   '''
    61    300001     172580.0      0.6      1.6          piece = self.pieces[piece]
    62    300001     198110.0      0.7      1.8          H, W = len(piece), len(piece[0])
    63    300001    3998458.0     13.3     36.6          row = self._lock(piece, pos)
    64                                           
    65                                                   # Add additional rows
    66    500001     369354.0      0.7      3.4          for i in range(row+1-len(self.board)):
    67    200000     149838.0      0.7      1.4              self.board.append([0]*self.board_width)
    68                                           
    69                                                   # Update board
    70    900003     500990.0      0.6      4.6          for i in range(H):
    71   1800006     995436.0      0.6      9.1              for j in range(W):
    72   1200004     664574.0      0.6      6.1                  if piece[i][j] == 1:
    73   1200004     728842.0      0.6      6.7                      self.board[row-i][pos+j] = 1
    74   1200004     980017.0      0.8      9.0                      self.heights[pos+j] = max(self.heights[pos+j], row-i+1)
    75                                           
    76                                                   # Clear full rows
    77    300001     163195.0      0.5      1.5          i = row - H + 1
    78    900003     505481.0      0.6      4.6          for _ in range(H):  # We only need to check rows occupied by the newly added piece
    79    600002    1175321.0      2.0     10.8              if all([x == 1 for x in self.board[i]]):
    80                                                           self.board.pop(i)
    81                                                           self.heights = [x-1 for x in self.heights]
    82                                                       else:
    83    600002     322117.0      0.5      2.9                  i += 1

Total time: 2.1753 s
File: TetrisGame.py
Function: _lock at line 91

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================

    91                                               @profile
    92                                               def _lock(self, piece, pos):
    93                                                   '''
    94                                                   Return the row index of the top of the piece after it lands
    95                                           
    96                                                   Args:
    97                                                       piece (list of list of int): shape of the piece
    98                                                       pos (int): column index of the leftmost block of the piece
    99                                                   '''

   100    300001     177448.0      0.6      8.2          H, W = len(piece), len(piece[0])
   101    300001     221822.0      0.7     10.2          lowest = [None] * W
   102    900003     464173.0      0.5     21.3          for col in range(W):
   103    600002     879820.0      1.5     40.4              lowest[col] = max([row for row in range(H) if piece[row][col] == 1])  # row index of lowest 1 in each column of `piece`, can cache this value if pieces are large
   104                                           
   105                                                   # The row index of the top of the piece after it lands is the largest row index of each column landing individually
   106    300001     432041.0      1.4     19.9          return max([self.heights[pos+col] + lowest[col] for col in range(W)])
```



Here I have a few suggestions on performance enhancements for larger sequences:

- We can calculate the `lowest` array for each piece ahead of time, instead of calculating it every time as seen on line 102 and 103. This will reduce the majority of runtime inside function `_lock`, which takes up a huge portion of runtime in function `add`.
- If we are allowed to use external libraries, we can use `numpy` and make the arrays of `self.heights` and `self.board` numpy arrays. This allows us to write Vectorized code which will run faster with the underlying pre-compiled C code, compared to explicitly writing for loops, as seen in line 81 and  106, for example.



