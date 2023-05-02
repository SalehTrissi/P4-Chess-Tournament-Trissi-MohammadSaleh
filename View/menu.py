class MenuView:
    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        print("\n --- MAIN MENU --- \n")
        print("[1] Create new player")
        print("[2] Edit or delete existing player")
        print("[3] Display list of players")
        print("[4] Create new tournament")
        print("[5] Load tournament")
        print("[6] Reports")
        print("[7] Exit program")

    @staticmethod
    def main_menu_reports():
        print("\n---------------------------")
        print("\t MENU OF REPORTS ")
        print("---------------------------\n")
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
        print(f"Enter {option} (type [back] for main menu) : ", end='')

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
        print("\n-----------------------------------")
        print(" Edit or delete a Player from database")
        print("-----------------------------------\n")
        print("You want edit or delete the player?\n")
        print("[1] Edit the player.")
        print("[2] Delete the player.")
        print("Chose [1] for Edit or [2] for delete: ", end="")

    @staticmethod
    def load_a_tournament():
        print("--------------------------".center(70))
        print(" Load a tournament".center(70))
        print("--------------------------".center(70))

    @staticmethod
    def sort_all_players_by_name(sorting):
        print("-----------------------------".center(70))
        print(f" All players ({sorting})".center(70))
        print("-----------------------------".center(70))

    @staticmethod
    def all_tournaments():
        print("-----------------------------".center(70))
        print(" All tournaments".center(70))
        print("-----------------------------".center(70))

    @staticmethod
    def display_all_players_matches(matches):
        print("-----------------------------".center(80))
        print(f"All played matches ({len(matches)} total)".center(80))
        print("-----------------------------".center(80))

    @staticmethod
    def msg_all_rounds():
        print("-----------------------".center(100))
        print(" All rounds".center(100))
        print("-----------------------\n".center(100))

    @staticmethod
    def header_final_scour(tournament):
        # Print the final scores and tournament details
        print("-----------------------------".center(50))
        print(" FINAL SCORES".center(50))
        print("-----------------------------".center(50))
        print(f"{tournament.name.upper()}, {tournament.location.title()} | "
              f"Description : {tournament.description}".center(50))
        print(f"Start : {tournament.start_date} | "
              f"End : {tournament.end_date} ".center(50))

    @staticmethod
    def reports_player_sorting():
        print("-----------------------".center(50))
        print(" Select a choix".center(50))
        print("-----------------------".center(50))
        print("Do you want to display the player’s name or rank?")
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

    @staticmethod
    def report_header(info):
        """Prints header for tournament reports

        Args:
            info (dict): Dictionary containing information about the tournament
                (name, location, description, start_date, end_date,
                nb_current_round, rounds_total)
        """
        print("\n\n")

        h_1 = f"{info['name'].upper()}, {info['location'].title()} | " \
              f"Description : {info['description']}"
        h_2 = \
            f"Start date : {info['start_date']} | " \
            f"End date : {info['end_date']} | " \
            f"Rounds played : {info['nb_current_round'] - 1}/" \
            f"{info['rounds_total']}"

        # Print the header
        print(h_1)
        print(h_2)
