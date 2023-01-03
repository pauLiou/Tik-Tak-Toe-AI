class GameState:
    def __init__(self):

        self.board = [
            ['7','8','9'],
            ['4','5','6'],
            ['1','2','3']
        ]
        self.human_to_move = True
        self.move_log = []

    def make_move(self,move):
        self.board[move.square_row][move.square_col] = 'x'
        self.move_log.append(move)
        self.human_to_move = not self.human_to_move

    def get_valid_moves(self):
        pass

class Move:
    
    def __init__(self,sq,board):
        self.square_row = sq[0]
        self.square_col = sq[1]
        self.move_made = board[self.square_row][self.square_col]       


