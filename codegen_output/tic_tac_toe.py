
# Initialize the board
board = [[' ' for _ in range(3)] for _ in range(3)]

def print_board():
    for row in board:
        print(' | '.join(row))
        print('---------')

def check_win(player):
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False

def play_game():
    current_player = 'X'
    while True:
        print_board()
        move = input(f"Player {current_player}, enter your move (1;2 or 2;3 or 3;1): ")
        x, y = int(move.split(';')[0]), int(move.split(';')[1])
        if board[x-1][y-1] != ' ':
            print("Invalid move, try again.")
            continue
        board[x-1][y-1] = current_player
        if check_win(current_player):
            print_board()
            print(f"Player {current_player} wins!")
            play_again = input("Do you want to play again? (Y/N): ")
            if play_again.lower() == 'q':
                break
            else:
                board = [[' ' for _ in range(3)] for _ in range(3)]
                current_player = 'X'
        elif all(cell != ' ' for row in board for cell in row):
            print_board()
            print("It's a draw!")
            play_again = input("Do you want to play again? (Y/N): ")
            if play_again.lower() == 'q':
                break
            else:
                board = [[' ' for _ in range(3)] for _ in range(3)]
                current_player = 'X'
        else:
            current_player = 'O'

play_game()
