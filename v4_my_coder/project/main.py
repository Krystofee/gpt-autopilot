
# main.py
import os

game_state = {
    "grid": [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]],
    "score": 0,
    "messages": []
}

def print_game_state():
    print("Game State:")
    for row in game_state["grid"]:
        print(" ".join(row))
    print(f"Score: {game_state['score']}")
    if game_state["messages"]:
        print("\nMessages:")
        for message in game_state["messages"]:
            print(message)

def main_menu():
    print("Welcome to My Game!")
    while True:
        print("\nMain Menu:")
        print("1. Start Game")
        print("2. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            # Call the main function
            start_game()
            break
        elif choice == "2":
            print("Goodbye!")
            exit()
        else:
            print("Invalid choice. Please enter 1 or 2.")

def start_game():
    while True:
        print("\nGame Start:")
        for i in range(3):
            for j in range(3):
                if game_state["grid"][i][j] == " ":
                    print(f"Enter a move (row {i+1}, column {j+1}): ")
                    row = int(input()) - 1
                    col = int(input()) - 1
                    if 0 <= row < 3 and 0 <= col < 3:
                        game_state["grid"][row][col] = "X"
                        print_game_state()
                    else:
                        print("Invalid move. Try again.")
        break

if __name__ == "__main__":
    main_menu()
