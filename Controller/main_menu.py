from Controller.controller import Controllers
from Controller.player import MenuPlayerController
from Controller.report import ReportController
from Controller.tournament import MenuTournamentController
from Model.player import PlayersDatabase
from View.menu import MenuView
from View.player import AddPlayerMenu
from View.tournament import CreateNewTournament


class MenuController:
    CREATE_NEW_PLAYER_OPTION = '1'
    EDIT_EXISTING_PLAYERS_OPTION = '2'
    SHOW_LIST_PLAYERS_OPTION = '3'
    CREATE_NEW_TOURNAMENT_OPTION = '4'
    LOAD_TOURNAMENT_OPTION = '5'
    REPORTS = '6'
    EXIT_OPTION = '7'

    def __init__(self):
        self.menu_view = MenuView()
        self.controllers = Controllers()
        self.menu_options = {
            self.CREATE_NEW_PLAYER_OPTION: self.create_new_player,
            self.EDIT_EXISTING_PLAYERS_OPTION:
                self.edit_or_delete_existing_player,
            self.SHOW_LIST_PLAYERS_OPTION: self.show_list_players,
            self.CREATE_NEW_TOURNAMENT_OPTION: self.create_new_tournament,
            self.LOAD_TOURNAMENT_OPTION: self.load_tournament,
            self.REPORTS: self.reports_menu,
            self.EXIT_OPTION: self.exit_program,
        }

    def main_menu(self):
        """Displays the main menu and handles user input"""
        self.menu_view.title_menu()
        self.menu_view.main_menu()
        self.menu_view.input_msg()
        user_input = input().lower()

        if user_input in self.menu_options:
            self.menu_options[user_input]()
        else:
            self.invalid_option()

    def create_new_player(self):
        """Handles creating a new player"""
        self.menu_view.title_create_new_player()
        # Call function to create a new player here
        AddPlayerMenu()
        self.controllers.return_or_exit()

    def show_list_players(self):
        """Displays a list of players"""
        self.menu_view.title_show_list_players()
        MenuPlayerController().table_list_players()
        self.controllers.return_or_exit()

    def create_new_tournament(self):
        """Create a new tournament"""
        self.menu_view.title_create_new_tournament()
        CreateNewTournament()
        self.controllers.return_or_exit()

    def edit_or_delete_existing_player(self):
        """Modify the existing player information."""
        while True:
            self.menu_view.titre_edit_existing_player()
            try:
                user_input = input()
                if user_input == '1':
                    PlayersDatabase().update_player()
                    self.controllers.return_or_exit()
                elif user_input == '2':
                    PlayersDatabase().delete_player()
                    self.controllers.return_or_exit()
                else:
                    raise ValueError("Invalid input.")
            except ValueError as e:
                print(f"Error: {e}. Please enter a valid input.")
                continue

    def load_tournament(self):
        """Handles in a progress option"""
        self.menu_view.load_a_tournament()
        MenuTournamentController().load_tournament()
        self.controllers.return_or_exit()

    def reports_menu(self):
        self.menu_view.main_menu_reports()
        ReportMenu().main_menu_reports()
        self.controllers.return_or_exit()

    def invalid_option(self):
        """Displays a message for invalid option"""
        self.menu_view.invalid_input()
        self.main_menu()

    def exit_program(self):
        """Handles quitting the program"""
        self.menu_view.msg_good_bay()
        self.menu_view.exit_program()


class ReportMenu:
    # Constants for menu options
    DISPLAY_ALL_PLAYERS = '1'
    DISPLAY_PLAYERS_IN_TOURNAMENT = '2'
    DISPLAY_ALL_TOURNAMENTS = '3'
    DISPLAY_ROUNDS_IN_TOURNAMENT = '4'
    DISPLAY_MATCHES_IN_TOURNAMENT = '5'
    EXIT_OPTION = '6'
    RETURN_TO_MENU = 'back' or 'Back'

    def __init__(self):
        # Initialize menu, menu Controller, and reports Controller
        self.menu_view = MenuView()
        self.menu_controller = MenuController()
        self.reports_controller = ReportController()
        # Initialize menu options dictionary with option 1
        # and its corresponding function call
        self.menu_options = {

            self.DISPLAY_ALL_PLAYERS: self.player_reports_sorting,

            self.DISPLAY_PLAYERS_IN_TOURNAMENT:
                self.display_players_in_tournament,

            self.DISPLAY_ALL_TOURNAMENTS:
                self.display_all_tournaments,

            self.DISPLAY_ROUNDS_IN_TOURNAMENT:
                self.display_rounds_in_tournament,

            self.DISPLAY_MATCHES_IN_TOURNAMENT:
                self.display_matches_in_tournament,

            self.EXIT_OPTION: self.menu_controller.exit_program,

            self.RETURN_TO_MENU: self.reports_controller.return_to_main_menu,
        }

    def main_menu_reports(self):
        """Displays the main menu and handles user input"""

        # Display the main menu and prompt for user input
        self.menu_view.input_msg()
        user_input = input().lower()

        # If user input matches a menu option,
        # execute the corresponding function
        if user_input in self.menu_options:
            self.menu_options[user_input]()
        else:
            # Otherwise, display an error message and return to the main menu
            self.menu_view.invalid_input()
            self.menu_view.main_menu_reports()
            self.main_menu_reports()

    def player_reports_sorting(self):
        # Call the reports_player_sorting() method
        # from the reports_controller object
        self.reports_controller.reports_player_sorting(
            PlayersDatabase().load_players_db())
        # Call the main_menu_reports() method
        self.main_menu_reports()

    def display_players_in_tournament(self):
        # Call the display_players_of_tournament() method
        # from the reports_controller object
        self.reports_controller.reports_player_sorting(
            self.reports_controller.display_players_of_tournament())
        self.main_menu_reports()

    def display_all_tournaments(self):
        # Call the all_tournaments() method from the reports_controller object
        self.reports_controller.all_tournaments()
        # Call the main_menu_reports() method
        self.main_menu_reports()

    def display_rounds_in_tournament(self):
        # Call the tournament_rounds() method
        # from the reports_controller object
        self.reports_controller.tournament_rounds()
        # Call the main_menu_reports() method
        self.main_menu_reports()

    def display_matches_in_tournament(self):
        # Call the display_tournament_matches() method
        # from the reports_controller object
        self.reports_controller.display_tournament_matches()
        # Call the main_menu_reports() method
        self.main_menu_reports()
