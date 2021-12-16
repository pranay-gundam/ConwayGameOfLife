def validPos(width, height, row, col):
    if row < 0:
        return False
    if col < 0:
        return False
    if row >= height:
        return False
    if col >= width:
        return False

    return True

def nextLife(board, row, col):
    iter = [-1,0,1]
    count = 0
    for irow in iter:
        c_row = row + irow
        for icol in iter:
            c_col = col + icol
            if validPos(len(board[0]), len(board), c_row, c_col) and not (irow == 0 and icol == 0):
                if board[c_row][c_col] == 1:
                    count += 1
                
    if board[row][col] == 0 and count == 3: return True
    if board[row][col] == 1 and (count == 2 or count == 3): return True
    
    return False

class playGame(object):
    def __init__(self, grid):
        self.grid = grid
    
    def getGrid(self):
        return self.grid

    def next_gen(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[0])):
                if nextLife(self.grid, row, col): 
                    self.grid[row][col] = 1
                else:
                    self.grid[row][col] = 0
        return self.grid
