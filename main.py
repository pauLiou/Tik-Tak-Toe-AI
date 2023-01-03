import pygame
import engine

WIDTH = HEIGHT = 512
DIMENSION = 3
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

def load_images():
    pieces = ['x','o']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('./Assests/' + piece + '.png'),(SQ_SIZE,SQ_SIZE))
def main():
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    clock = pygame.time.Clock()
    running = True
    sq_selected = ()
    player_clicks = []

    gs = engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    load_images()


    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running == False


        #mouse stuff
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row,col):
                    sq_selected = ()
                else:
                    sq_selected = (row,col)
                #if len(player_clicks) == 1:
                move = engine.Move(sq_selected,gs.board)
                    #if move in valid_moves:
                gs.make_move(move)
                move_made = True
                sq_selected = ()

        if move_made:
            move_made = False
        draw_game_state(screen,gs)
        clock.tick(MAX_FPS)
        pygame.display.flip()






def draw_game_state(screen,gs):
    draw_board(screen)
    draw_pieces(screen,gs.board)

def draw_board(screen):
    colours = [pygame.Color('white'),pygame.Color('light blue')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[((r+c)) % 2]
            pygame.draw.rect(screen,colour,pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def draw_pieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece == 'x':
                screen.blit(IMAGES[piece],pygame.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))

if __name__ == "__main__":
    main()