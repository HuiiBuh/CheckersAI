from Colors import COLOUR


def select_order(error: str = "") -> int:
    """
    Asks the user for the order
    :param error: The error message that will be displayed if th user makes a wrong input
    :return: The Order 1 for the computer first or 2 for the human first
    """
    if error != "":
        print(COLOUR.RED + error + COLOUR.END)

    player_order: str = input("Select if you (1) want to be first or your opponent (2): ")
    if not (player_order == "1" or player_order == "2"):
        error_message: str = f"You did not input '1' for opponent first or '2' for yourself first, but {player_order}"
        return int(select_order(error=error_message))

    return int(player_order)


def select_difficulty(error: str = "") -> int:
    """
    Asks the user to select a difficulty
    :param error: The error message that will be displayed if th user makes a wrong input
    :return: The difficulty
    """
    if error != "":
        print(COLOUR.RED + error + COLOUR.END)

    print("Select the difficulty 0: Random 1: Self learning KI")

    selected_difficulty: str = input("Difficulty: ")
    if not (selected_difficulty == "0" or selected_difficulty == "1"):
        return int(select_difficulty(error=f"You did not input 0 or 1 but {selected_difficulty}"))

    return int(selected_difficulty)
