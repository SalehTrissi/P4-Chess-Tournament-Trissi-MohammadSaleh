class MenuView:
    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        print("\n --- MAIN MENU --- \n")
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
    def title_menu():
        print("\n-----------------------------------")
        print(" Your Welcome in CHESS TOURNAMENTS")
        print("-----------------------------------")

    @staticmethod
    def input_msg():
        print("\nEnter the option, then press Enter: ", end='')

    @staticmethod
    def msg_input_prompt(option):
        print(f"\nEnter {option} (type [back] for main menu) : ", end='')

    @staticmethod
    def title_create_new_player():
        print("\n-----------------------------")
        print("\t Create new player ")
        print("-----------------------------\n")

    @staticmethod
    def title_show_list_players():
        print("\t\t\t--------------------------")
        print("\t\t\t   Table of all players")
        print("\t\t\t--------------------------")

    @staticmethod
    def title_create_new_tournament():
        print("\n------------------------")
        print(" Create new tournament")
        print("------------------------\n")

    @staticmethod
    def titre_edit_existing_player():
        print("\n--------------------------")
        print(" Edit Player Information")
        print("--------------------------\n")

    @staticmethod
    def load_a_tournament():
        print("--------------------------".center(70))
        print(" Load a tournament".center(70))
        print("--------------------------".center(70))

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
    def update_rank_msg():
        print("\nUpdate ranks ? [y/n] ", end='')

    @staticmethod
    def msg_return_main_menu():
        print("\nIf you want to go back to the main menu,"
              " type 'back' or 'return': ")

    @staticmethod
    def rank_update_header(player):
        print(f"\nUpdating {player.last_name}, {player.first_name}")

    @staticmethod
    def review_tournament(info, players):
        print("\n\nNew tournament created with successfully")
        print(f"Name : {info[1]}, Location :{info[2]}", end=" | ")
        print(f"Description : {info[2]}", end=' | ')
        print("Rounds : 4", end=' | ')
        print(f"Time control : {info[3]}")
        print("\nPlayers (2 total) :\n")

        for item in players:
            print(f"Player {players.index(item) + 1} : ", end='')
            print(f"{item['id']}", end=' | ')
            print(f"{item['last_name']}, {item['first_name']}", end=' | ')
            print(f"{item['date_of_birth']}", end=' | ')
