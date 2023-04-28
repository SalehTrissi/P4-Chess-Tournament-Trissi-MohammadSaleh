from Controller.tournament import MenuTournamentController
from View.menu import MenuView


class Controllers:
    def __init__(self):
        self.menu_view = MenuView()
        self.controller_tournament = MenuTournamentController()

    def return_or_exit(self):
        # A loop that runs indefinitely until 'break' is called.
        while True:
            # Ask for user input and convert it to lowercase.
            user_input = input(
                "\nType 'back' to return to main menu, "
                "'exit' to exit the program: ").lower()
            # If user types 'back', return to the main menu.
            if user_input == 'back':
                # Return to the main menu
                self.controller_tournament.return_to_main_menu()
                # Exit the loop.
                break
            # If user types 'exit', exit the program.
            elif user_input == 'exit':
                # Exit program
                """Handles quitting the program"""
                # Display a goodbye message.
                self.menu_view.msg_good_bay()
                # Call a function to exit the program.
                self.menu_view.exit_program()
                # Exit the loop.
                break
            # If the user input is neither 'back' nor 'exit',
            # show an error message and ask for input again.
            else:
                # Show an error message and re-ask for input.
                print("Invalid input. Please type 'back' or 'exit'.")
