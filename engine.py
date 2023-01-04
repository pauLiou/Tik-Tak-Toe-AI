

class GameState:
    def __init__(self):

        self.board = [
            ['7','8','9'],
            ['4','5','6'],
            ['1','2','3']
        ]
        self.x_to_move = True
        self.move_log = []

    def make_move(self,move):
        if self.x_to_move:
            if self.board[move.square_row][move.square_col].isdigit() and move not in self.move_log:
                self.board[move.square_row][move.square_col] = 'x'
                self.move_log.append(move)
                self.x_to_move = not self.x_to_move
        else:
            if self.board[move.square_row][move.square_col].isdigit() and move not in self.move_log:
                self.board[move.square_row][move.square_col] = 'o'
                self.move_log.append(move)
                self.x_to_move = not self.x_to_move

    def winner(self, symbol):
        for row in self.board:
            if all(square == symbol for square in row):
                return True
                        # Check columns
        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True

        # Check diagonals
        if all(self.board[i][i] == symbol for i in range(3)):
            return True
        if all(self.board[i][2-i] == symbol for i in range(3)):
            return True

        return False
        
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

class Move:
    def __init__(self,sq,board):
        self.square_row = sq[0]
        self.square_col = sq[1]
        self.move_made = board[self.square_row][self.square_col] 

class Player:
    def __init__(self,player,score):
        self.score = score
        self.player = player    


