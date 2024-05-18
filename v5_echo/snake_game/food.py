import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_BLOCK_SIZE, RED

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.spawn()

    def spawn(self):
        self.position = (random.randint(0, (SCREEN_WIDTH // SNAKE_BLOCK_SIZE) - 1) * SNAKE_BLOCK_SIZE,
                         random.randint(0, (SCREEN_HEIGHT // SNAKE_BLOCK_SIZE) - 1) * SNAKE_BLOCK_SIZE)

    def render(self, surface):
        rect = pygame.Rect(self.position, (SNAKE_BLOCK_SIZE, SNAKE_BLOCK_SIZE))
        pygame.draw.rect(surface, RED, rect)
