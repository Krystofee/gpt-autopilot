import pygame
from constants import SCREEN_SIZE, SNAKE_BLOCK_SIZE, SNAKE_SPEED, BLACK
from snake import Snake
from food import Food
from score import Score

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.snake = Snake()
        self.food = Food()
        self.score = Score()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.snake.handle_keys(event)

            self.snake.move()

            if self.snake.get_head_position() == self.food.position:
                self.snake.grow_snake()
                self.food.spawn()
                self.score.increment()

            self.screen.fill(BLACK)
            self.snake.render(self.screen)
            self.food.render(self.screen)
            self.score.render(self.screen)
            pygame.display.update()

            if self.snake.check_collision():
                print(f'Game Over! Your score was: {self.score.score}')
                self.running = False

            self.clock.tick(SNAKE_SPEED)

        pygame.quit()
