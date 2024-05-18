import pygame
from constants import WHITE, FONT_NAME, FONT_SIZE

class Score:
    def __init__(self):
        pygame.font.init()
        self.score = 0
        self.font = pygame.font.Font(FONT_NAME, FONT_SIZE)

    def increment(self):
        self.score += 1

    def render(self, surface):
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        surface.blit(score_text, (10, 10))
