
import curses
import snake
from snake import Snake

class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.snake_position = [(100, 100)]
        self.snake_direction = 'right'
        self.score = 0

    def update_game_state(self):
        # Update snake position based on direction
        if self.snake_direction == 'right':
            self.snake_position.append((self.snake_position[-1][0] + 10, self.snake_position[-1][1]))
        elif self.snake_direction == 'left':
            self.snake_position.append((self.snake_position[-1][0] - 10, self.snake_position[-1][1]))
        elif self.snake_direction == 'up':
            self.snake_position.append((self.snake_position[-1][0], self.snake_position[-1][1] - 10))
        elif self.snake_direction == 'down':
            self.snake_position.append((self.snake_position[-1][0], self.snake_position[-1][1] + 10))

    def handle_user_input(self, input_key):
        if input_key == curses.KEY_RIGHT and self.snake_direction != 'left':
            self.snake_direction = 'right'
        elif input_key == curses.KEY_LEFT and self.snake_direction != 'right':
            self.snake_direction = 'left'
        elif input_key == curses.KEY_UP and self.snake_direction != 'down':
            self.snake_direction = 'up'
        elif input_key == curses.KEY_DOWN and self.snake_direction != 'up':
            self.snake_direction = 'down'

    def render_game_screen(self, screen):
        # Clear the screen
        screen.clear()

        # Draw snake
        for pos in self.snake_position:
            screen.addstr(pos[1], pos[0], '*')

        # Update score
        screen.addstr(0, 0, f'Score: {self.score}')

    def main_loop(self):
        while True:
            input_key = curses.getch()
            self.handle_user_input(input_key)
            self.update_game_state()

            # Render game screen
            self.render_game_screen(curses.initscr())

            # Check for game over condition (e.g. snake collides with itself or boundary)
            if any(pos in self.snake_position[:-1] for pos in self.snake_position[1:]):
                break

        curses.endwin()



import curses
from snake import Snake

class Game:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.snake_position = [(100, 100)]
        self.snake_direction = 'right'
        self.score = 0

    def update_game_state(self):
        if self.snake_direction == 'right':
            self.snake_position.append((self.snake_position[-1][0] + 10, self.snake_position[-1][1]))
        elif self.snake_direction == 'left':
            self.snake_position.append((self.snake_position[-1][0] - 10, self.snake_position[-1][1]))
        elif self.snake_direction == 'up':
            self.snake_position.append((self.snake_position[-1][0], self.snake_position[-1][1] - 10))
        elif self.snake_direction == 'down':
            self.snake_position.append((self.snake_position[-1][0], self.snake_position[-1][1] + 10))

    def handle_user_input(self, input_key):
        if input_key == curses.KEY_RIGHT and self.snake_direction != 'left':
            self.snake_direction = 'right'
        elif input_key == curses.KEY_LEFT and self.snake_direction != 'right':
            self.snake_direction = 'left'
        elif input_key == curses.KEY_UP and self.snake_direction != 'down':
            self.snake_direction = 'up'
        elif input_key == curses.KEY_DOWN and self.snake_direction != 'up':
            self.snake_direction = 'down'

    def main_loop(self):
        while True:
            input_key = curses.getch()
            self.handle_user_input(input_key)
            self.update_game_state()
            # Render game screen
            #self.render_game_screen(curses.initscr())
            # Check for game over condition (e.g. snake collides with itself or boundary)
            if any(pos in self.snake_position[:-1] for pos in self.snake_position[1:]):
                break
        curses.endwin()


