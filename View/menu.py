class MenuView:
    def __init__(self):
        pass

    @staticmethod
    def title_menu():
        print("\n** Your Welcome in CHESS TOURNAMENTS **")

    @staticmethod
    def main_menu():
        print("--- MAIN MENU --- \n")
        print("[1] Create new player")
        print("[2] Edit existing player")
        print("[3] Display list of players")
        print("[4] Create new tournament")
        print("[5] Load tournament")
        print("[6] Reports")
        print("[7] Exit program")

    @staticmethod
    def main_menu_reports():
        print("\n --- MENU OF REPORTS --- \n")
        print("[1] Display all players")
        print("[2] Display players in a tournament")
        print("[3] Display all tournament")
        print("[4] Display the rounds in a tournament")
        print("[5] Display matches in a tournament")
        print("[6] Exit program")
        print("\n[back] Return to main menu")

    @staticmethod
    def input_msg():
        print("\nEnter the option, then press Enter: ", end='')

    @staticmethod
    def msg_input_prompt(option):
        print(f"\nEnter {option} (type [back] for main menu) : ", end='')

    @staticmethod
    def title_create_new_player():
        print("\t\n --- Create new player ---\n")

    @staticmethod
    def title_show_list_players():
        print("\t\n --- Table of all players ---")

    @staticmethod
    def title_create_new_tournament():
        print("\t\n --- Create new tournament ---\n")

    @staticmethod
    def titre_edit_existing_player():
        print("\t --- Modify the player information ---\n")

    @staticmethod
    def reports_player_sorting():
        print("\nDo you want to display the player’s name or rank?")
        print("[1] Sort by name")
        print("[2] Sort by rank")
        print("\n[back] Back to main menu")

    @staticmethod
    def msg_good_bay():
        print("\n\t --- Good-bye! ---")

    @staticmethod
    def exit_program():
        print("Thank you for using our program.")
        return exit()

    @staticmethod
    def invalid_input():
        """Print error message for invalid user input"""
        print("\n*** [Error] Invalid input. Please try again ***")

    @staticmethod
    def your_welcome():
        print("--- Your welcome ---\n".center(100))

    @staticmethod
    def msg_return_main_menu():
        print("\nIf you want to go back to the main menu,"
              " type 'back' or 'return': ")

    @staticmethod
    def rank_update_header(player):
        print(f"\nUpdating {player.last_name}, {player.first_name}")
