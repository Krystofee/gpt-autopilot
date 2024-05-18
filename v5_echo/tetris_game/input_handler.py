import pygame

class InputHandler:
    def __init__(self, tetris):
        """
        Initialize the input handler with a reference to the Tetris game.
        :param tetris: Instance of the Tetris game.
        """
        self.tetris = tetris

    def handle_input(self, event):
        """
        Handle the keyboard input and map it to game controls.
        :param event: Pygame event.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.tetris.move('left')
            elif event.key == pygame.K_d:
                self.tetris.move('right')
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                self.tetris.move('rotate')
