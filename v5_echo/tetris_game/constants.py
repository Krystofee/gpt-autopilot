BOARD_WIDTH = 10
BOARD_HEIGHT = 20
TILE_SIZE = 30

# Define the colors for the tetris pieces
COLORS = [
    (0, 0, 0),        # Black for the background
    (0, 255, 255),    # Cyan for I
    (0, 0, 255),      # Blue for J
    (255, 165, 0),    # Orange for L
    (255, 255, 0),    # Yellow for O
    (0, 255, 0),      # Green for S
    (128, 0, 128),    # Purple for T
    (255, 0, 0)       # Red for Z
]

# Define the shapes of the tetris pieces
SHAPES = [
    [[1, 1, 1, 1]],                       # I
    [[2, 0, 0], [2, 2, 2]],               # J
    [[0, 0, 3], [3, 3, 3]],               # L
    [[4, 4], [4, 4]],                     # O
    [[0, 5, 5], [5, 5, 0]],               # S
    [[0, 6, 0], [6, 6, 6]],               # T
    [[7, 7, 0], [0, 7, 7]]                # Z
]