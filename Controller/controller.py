from Controller.tournament import MenuTournamentController
from View.menu import MenuView


class Controllers:
    def __init__(self):
        self.menu_view = MenuView()
        self.controller_tournament = MenuTournamentController()

    def return_or_exit(self):
        while True:
            user_input = input(
                "\nType 'back' to return to main menu, "
                "'exit' to exit the program: ").lower()
            if user_input == 'back':
                # Return to the main menu
                self.controller_tournament.return_to_main_menu()
                break
            elif user_input == 'exit':
                # Exit program
                """Handles quitting the program"""
                self.menu_view.msg_good_bay()
                self.menu_view.exit_program()
                break
            else:
                # Show an error message and re-ask for input
                print("Invalid input. Please type 'back' or 'exit'.")
