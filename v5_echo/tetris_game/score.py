import pygame

class Score:
    def __init__(self):
        self.score = 0

    def update_score(self, lines_cleared):
        """Update the score based on the number of lines cleared."""
        self.score += lines_cleared * 100

    def display_score(self, screen):
        """Render the score at the top left of the screen."""
        font = pygame.font.SysFont('arial', 25)
        score_text = font.render(f'Score: {self.score}', True, (255, 255, 255))
        screen.blit(score_text, (5, 5))