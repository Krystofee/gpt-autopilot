import pygame
from constants import BOARD_WIDTH, BOARD_HEIGHT, TILE_SIZE, COLORS, SHAPES
import random

class Tetris:
    def __init__(self, score):
        self.board = [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
        self.game_over = False
        self.current_piece = self.get_new_piece()
        self.next_piece = self.get_new_piece()
        self.piece_x = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        self.score = score

    def get_new_piece(self):
        return random.choice(SHAPES)

    def check_collision(self, piece, offset_x, offset_y):
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    px = x + offset_x
                    py = y + offset_y
                    if px < 0 or px >= BOARD_WIDTH or py >= BOARD_HEIGHT:
                        return True
                    if py >= 0 and self.board[py][px]:
                        return True
        return False

    def lock_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y + self.piece_y][x + self.piece_x] = cell
        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = self.get_new_piece()
        self.piece_x = BOARD_WIDTH // 2 - len(self.current_piece[0]) // 2
        self.piece_y = 0
        if self.check_collision(self.current_piece, self.piece_x, self.piece_y):
            self.game_over = True

    def clear_lines(self):
        lines_cleared = 0
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = BOARD_HEIGHT - len(new_board)
        self.board = [[0] * BOARD_WIDTH for _ in range(lines_cleared)] + new_board
        self.score.update_score(lines_cleared)

    def rotate_piece(self):
        return [list(reversed(col)) for col in zip(*self.current_piece)]

    def move(self, direction):
        if direction == 'left':
            if not self.check_collision(self.current_piece, self.piece_x - 1, self.piece_y):
                self.piece_x -= 1
        elif direction == 'right':
            if not self.check_collision(self.current_piece, self.piece_x + 1, self.piece_y):
                self.piece_x += 1
        elif direction == 'down':
            if not self.check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
                self.piece_y += 1
            else:
                self.lock_piece()
        elif direction == 'rotate':
            rotated = self.rotate_piece()
            if not self.check_collision(rotated, self.piece_x, self.piece_y):
                self.current_piece = rotated

    def drop(self):
        while not self.check_collision(self.current_piece, self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        self.lock_piece()

    def update(self):
        self.move('down')

    def draw_board(self, screen):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[cell], pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_piece(self, screen):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[cell], pygame.Rect((self.piece_x + x) * TILE_SIZE, (self.piece_y + y) * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw(self, screen):
        self.draw_board(screen)
        self.draw_piece(screen)
