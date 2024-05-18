from colorama import Fore, Style, init

# Initialize colorama
init()

def print_colored_text(heading, text, color):
    color_dict = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
    }

    if color not in color_dict:
        print(f"Color '{color}' not recognized. Defaulting to white.")
        color = 'white'

    color_code = color_dict[color]

    print(f"\n{Style.BRIGHT}{color_code}{heading}{Style.RESET_ALL}")
    print(f"{color_code}{text}{Style.RESET_ALL}\n")

