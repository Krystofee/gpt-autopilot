import pygame
from constants import TILE_SIZE, COLORS

class Tile:
    def __init__(self, shape, color_index):
        self.shape = shape
        self.color = COLORS[color_index]

    def draw(self, screen, x, y):
        for row_index, row in enumerate(self.shape):
            for col_index, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, self.color, pygame.Rect(
                        (x + col_index) * TILE_SIZE, (y + row_index) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def rotate(self):
        """ Rotate the shape of the tile clockwise. """
        self.shape = [list(reversed(col)) for col in zip(*self.shape)]