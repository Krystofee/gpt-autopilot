
import os
import random
import time

# Initialize the game variables
snake = [(0, 0), (1, 0), (2, 0)]  # initial snake position and direction
apple = None
direction = 'right'
score = 0
game_over = False

# Set the terminal size
os.system('cls' if os.name == 'nt' else 'clear')
print("Welcome to Snake Game!")
print("Use WASD keys to control the snake.")
print("Press Enter to start.")

input()

while True:
    # Draw the game board
    os.system('cls' if os.name == 'nt' else 'clear')
    for y in range(20):
        for x in range(20):
            if (x, y) in snake:
                print('*', end=' ')
            elif (x, y) == apple:
                print('A', end=' ')
            else:
                print(' ', end=' ')
        print()
    print(f"Score: {score}")

    # Get the user input
    while True:
        try:
            direction = input()
            if direction in ['w', 'a', 's', 'd']:
                break
        except KeyboardInterrupt:
            game_over = True

    # Move the snake
    head = snake[0]
    new_head = (head[0], head[1])
    if direction == 'w':
        new_head = (new_head[0] - 1, new_head[1])
    elif direction == 's':
        new_head = (new_head[0] + 1, new_head[1])
    elif direction == 'a':
        new_head = (new_head[0], new_head[1] - 1)
    elif direction == 'd':
        new_head = (new_head[0], new_head[1] + 1)

    snake.insert(0, new_head)

    # Check for collision with wall or itself
    if (new_head[0] < 0 or new_head[0] >= 20 or
            new_head[1] < 0 or new_head[1] >= 20 or
            new_head in snake[1:]):
        game_over = True

    # Check for apple
    if new_head == apple:
        score += 1
        apple = None
    else:
        snake.pop()

    # Generate a new apple if there is none
    while not apple:
        apple = (random.randint(0, 19), random.randint(0, 19))

    time.sleep(0.5)

    if game_over:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Game Over! Your score is", score)
        break
