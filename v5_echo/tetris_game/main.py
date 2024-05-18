import pygame
import sys
from tetris import Tetris
from input_handler import InputHandler
from score import Score
from constants import BOARD_WIDTH, BOARD_HEIGHT, TILE_SIZE

# Initialize Pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode((BOARD_WIDTH * TILE_SIZE, BOARD_HEIGHT * TILE_SIZE))
pygame.display.set_caption('Tetris')

# Instantiate game components
score = Score()
tetris = Tetris(score)
input_handler = InputHandler(tetris)

# Run until the user asks to quit
running = True
clock = pygame.time.Clock()

while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            input_handler.handle_input(event)

    # Update game state
    tetris.update()

    # Check for game over
    if tetris.game_over:
        print('Game Over! Final Score:', score.score)
        running = False
        continue

    # Fill the background with black
    screen.fill((0, 0, 0))

    # Draw game elements
    tetris.draw(screen)
    
    # Display score
    score.display_score(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate at 2 frames per second
    clock.tick(2)

# Done! Time to quit.
pygame.quit()
sys.exit()
