import pygame
import numpy as np
import environment
from pygame.locals import *
import sys
from keras.models import Sequential
from keras.layers import Dense, Flatten
import keras
from rl.agents import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

WIDTH = HEIGHT = 512
DIMENSION = 3
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

x_score = environment.Player('x',0) # Player object X
o_score = environment.Player('o',0) # Player object O

# Load images for the x and o pieces
def load_images():
    pieces = ['x','o']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('./Assets/' + piece + '.png'),(SQ_SIZE,SQ_SIZE))


def main():
    pygame.init()
    load_images()
    border_size = 50 # the size of the outer border
    # Initialize pygame window and clock
    screen = pygame.display.set_mode((WIDTH + 50 * 2, HEIGHT + 50 * 2))
    clock = pygame.time.Clock()

    # Initialize game environment and DQN agent
    env = environment.TikTacToeEnv()
    model = Sequential()
    model.add(Flatten(input_shape=(3,3)))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(24, activation='relu'))
    model.add(Dense(9, activation='linear'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    # dqn = DQNAgent(model=model, policy=BoltzmannQPolicy())

    
    # Initialize game variables
    running = True
    counter = 10
    sq_selected = ()
    move = []
    
    # Train the agent using DQN
    model.fit(env, epochs=50000, verbose=2)
    
    while running:
        # Handle pygame events
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                sq_selected = get_user_action(50)
                move = environment.Move(sq_selected, env.board)
                if move.move_made != ['invalid']:
                    env.make_move(move)
                    counter = 10
                observation, reward, done, info = env.step(sq_selected)
                sq_selected = ()
                
        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
        counter -= elapsed_time
        start_time = pygame.time.get_ticks()
        clock.tick(MAX_FPS)

        # Check if X or O has won the game
        if env.winner(x_score.player):
            x_score.score += 1
            draw_game_state(screen,env,border_size,counter,x_score,o_score)
            draw_winner(screen,'X')
            pygame.display.update()
            while True:
                event = pygame.event.wait()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_f:
                        if __name__ == "__main__":
                            main()
                            


        if env.winner(o_score.player):
            o_score.score += 1
            draw_game_state(screen,env,border_size,counter,x_score,o_score)
            draw_winner(screen,'O')
            pygame.display.update()
            while True:
                event = pygame.event.wait()
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_f:
                        if __name__ == "__main__":
                            main()

        # Draw the current game state
        draw_game_state(screen,env,border_size,counter,x_score,o_score)
        pygame.display.flip()

def draw_game_state(screen,env,border_size,counter,x,o):
    draw_board(screen,border_size)
    draw_pieces(screen,env.board,border_size)
    draw_clock(screen,counter)
    draw_player_turn(screen,env.x_to_move)
    draw_score(screen,x,o)
    
# Draw the board on the screen
def draw_board(screen,border_size):
    # Clear the outer border area before drawing the new border
    screen.fill((0, 0, 0), pygame.Rect(0, 0, WIDTH + border_size * 2, border_size))
    screen.fill((0, 0, 0), pygame.Rect(0, HEIGHT + border_size, WIDTH + border_size * 2, border_size))
    screen.fill((0, 0, 0), pygame.Rect(0, 0, border_size, HEIGHT + border_size * 2))
    screen.fill((0, 0, 0), pygame.Rect(WIDTH + border_size, 0, border_size, HEIGHT + border_size * 2))

    colours = [pygame.Color('white'),pygame.Color('light blue')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c)) % 2]
            pygame.draw.rect(screen, colour, pygame.Rect(c * SQ_SIZE + border_size, r * SQ_SIZE + border_size, SQ_SIZE, SQ_SIZE))

# Draw the x and o pieces on the board
def draw_pieces(screen,board,border_size):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece in ['x','o']:
                screen.blit(IMAGES[piece],pygame.Rect(c * SQ_SIZE + border_size, r * SQ_SIZE + border_size, SQ_SIZE, SQ_SIZE))

# Draw the countdown timer on the screen
def draw_clock(screen,counter):
    font = pygame.font.SysFont(None, 75)
    counter = round(counter)
    text = font.render(str(counter), True, (0, 128, 0)) 
    text_rect = text.get_rect()
    text_rect.top = screen.get_rect().top
    text_rect.right = screen.get_rect().right
    
    screen.blit(text,text_rect)

# Draw the player turn indicator on the screen
def draw_player_turn(screen,gs):
    font = pygame.font.SysFont(None, 100)
    
    if gs == True:
        text = font.render(str('*'), True, (0,128,0))
        text_rect = text.get_rect()
        text_rect.bottom = screen.get_rect().bottom
        text_rect.left = screen.get_rect().left
    else:
        text = font.render(str('*'), True, (0,128,0))
        text_rect = text.get_rect()
        text_rect.topleft = screen.get_rect().topleft

    screen.blit(text,text_rect)

# Draw the score to the border at the top and bottom
def draw_score(screen,x,o):
    font = pygame.font.SysFont(None,50)
    colour = 128
    textx = font.render('Player X: ' + str(x.score),True,(0,colour,0))
    textx_rect = textx.get_rect()
    texto = font.render('Player O: ' + str(o.score),True,(0,colour,0))
    texto_rect = texto.get_rect()
    textx_rect.center = screen.get_rect().center
    textx_rect.bottom = screen.get_rect().bottom
    texto_rect.center = screen.get_rect().center
    texto_rect.top = screen.get_rect().top
    screen.blit(textx,textx_rect)
    screen.blit(texto,texto_rect)

# Display the winner in the center of the screen
def draw_winner(screen,winner):
    font = pygame.font.SysFont(None, 50)
    text = font.render(str(f'Player {winner} has won the game!'), True, (0,128,0))
    text_rect = text.get_rect()
    text_rect.center = screen.get_rect().center
    screen.blit(text,text_rect)

def get_user_action(border_size):

    # Get the position of the mouse click
    pos = pygame.mouse.get_pos()
    # Convert the mouse position to an action
    col = (pos[0]-border_size) // SQ_SIZE
    row = (pos[1]-border_size) // SQ_SIZE

    return (row,col)
    
if __name__ == "__main__":
    main()