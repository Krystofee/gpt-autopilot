
import os
import random

class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.snake_position = [(100, 100)]
        self.snake_direction = 'right'
        self.score = 0


