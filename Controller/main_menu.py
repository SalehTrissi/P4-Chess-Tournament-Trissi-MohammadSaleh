from Controller.controller import Controllers
from Controller.player import MenuPlayerController
from Model.player import PlayersDatabase
from View.menu import MenuView
from View.player import AddPlayerMenu


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
            self.EDIT_EXISTING_PLAYERS_OPTION: self.edit_existing_player,
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
        AddTournamentMenu()
        self.controllers.return_or_exit()

    def edit_existing_player(self):
        """Modify the existing player information."""
        self.menu_view.titre_edit_existing_player()
        PlayersDatabase().update_player()
        self.controllers.return_or_exit()

    def load_tournament(self):
        """Handles in a progress option"""
        self.menu_view.your_welcome()
        MenuTournamentController().resume_tournament()
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
