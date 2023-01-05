import gym

class TikTacToeEnv(gym.Env):
    def __init__(self):
        self.board = [['7','8','9'],
                      ['4','5','6'],
                      ['1','2','3']]
        self.x_to_move = True
        self.move_log = []
        self.x_score = Player('x',0)
        self.o_score = Player('o',0)
        self.action_space = gym.spaces.Discrete(9)  # 9 possible actions (one for each square)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(3, 3))  # 3x3 board

    def step(self, action):
        move = MoveAI(action, self.board)
        if move.move_made != ['invalid']:
            self.make_move(move)

        reward = 0
        done = False
        if self.winner(self.x_score.player):
            reward = 1
            done = True
        elif self.winner(self.o_score.player):
            reward = -1
            done = True
        elif len(self.move_log) == 9:
            reward = 0
            done = True

        return self._get_observation(), reward, done, {}

    def make_move(self,action):
        row = action.row
        col = action.col
        if self.board[row][col].isdigit() and (row, col) not in self.move_log:
            if self.x_to_move:
                self.board[row][col] = 'x'
                
            else:
                self.board[row][col] = 'o'
            self.move_log.append((row, col))
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

    def reset(self):
        self.board = [['7','8','9'],
                      ['4','5','6'],
                      ['1','2','3']]
        self.x_to_move = True
        self.move_log = []
        self.x_score = Player('x',0)
        self.o_score = Player('o',0)
        return self._get_observation()

    def _get_observation(self):
        observation = [[0 if square == 'x' else 1 if square == 'o' else 2 for square in row] for row in self.board]
        return observation

class Move:
    def __init__(self,sq,board):
        self.square_row = sq // 3
        self.square_col = sq % 3
        if [self.square_row,self.square_col] not in [[0,0],[0,1],[1,0],[1,1],[1,2],[2,0],[0,2],[2,1],[2,2]]:
            self.move_made = ['invalid']

        else:
            self.move_made = board[self.square_row][self.square_col]

class Player:
    def __init__(self,player,score):
        self.score = score
        self.player = player   

class MoveAI:
    def __init__(self,sq,board):
        self.col = sq % 3
        self.row = sq // 3
        self.move_made = board[self.row][self.col] 