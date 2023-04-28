from Controller.tournament import MenuTournamentController
from Model.tournament import TournamentDatabase
from View.menu import MenuView
from View.report import Reports


class ReportController:
    def __init__(self):
        self.menu_view = MenuView()
        self.reports_view = Reports()
        self.menu_tournament = MenuTournamentController()

    def reports_player_sorting(self, players):
        """
                    This method prompts the user to select a sorting option
                    for players (name or rank),
                    displays the sorted player report, and asks the user
                    if they would like to view another report.
                    """
        # Display sorting options to the user
        self.menu_view.reports_player_sorting()
        self.menu_view.msg_input_prompt("player reports sorting")

        # Create a dictionary with user input options
        # as keys and corresponding function calls as values
        options = {
            "1": lambda: self.display_players_by_name(players),
            "2": lambda: self.display_players_by_rank(players),
            "back": self.return_to_main_menu,
        }

        # Loop until user chooses to exit
        while True:
            # Get user input and execute corresponding function
            # call from dictionary
            user_input = input("Enter an option: ")
            if user_input in options:
                options[user_input]()  # Call function corresponding
                # to user input
                # Ask if user wants to view another report
                self.get_another_report_choice()
                break
            else:
                # Display an error message for invalid input
                # and show sorting options again
                self.menu_view.invalid_input()
                self.menu_view.reports_player_sorting()
                self.menu_view.msg_input_prompt("player reports sorting")

        # If code execution reaches here, user has chosen
        # to view another report
        # Return to reports menu
        # self.menu_view.main_menu_reports()

    def get_another_report_choice(self):
        """
        This method prompts the user for a choice to view another report
        and handles the input.
        """
        while True:
            print('\nTo return to the main menu press [back] '
                  'or [exit] to exit the programme,')
            another_report = input(
                "Would you like to view another report? [y/n]: ").lower()
            if another_report == "y":
                # Exit loop to display another report
                break
            elif another_report == "n" or another_report == "exit":
                # Exit program
                self.menu_view.msg_good_bay()
                self.menu_view.exit_program()
            elif another_report == "back":
                # Return to the main menu
                self.menu_tournament.return_to_main_menu()
            else:
                # Display an error message for invalid input
                self.menu_view.invalid_input()

        # If code execution reaches here,
        # user has chosen to view another report
        # Return to the report menu
        self.menu_view.main_menu_reports()

    def display_players_by_name(self, players: list) -> None:
        """Display player report sorted by last name.

        Args:
            players (list): List of player dictionaries.
        """
        # Sort players by last name
        players = sorted(players, key=lambda x: x.get('last_name'))
        # Display players report
        self.reports_view.display_players(players, "by name")

    def display_players_by_rank(self, players):
        """Display player report sorted by rank.

        Args:
            players (list): List of player dictionaries.
        """
        # Sort players by rank
        players = sorted(players, key=lambda x: x.get('rank'))
        # Display players report
        self.reports_view.display_players(players, "by rank")

    def display_players_of_tournament(self):
        """Display players in a tournament report. Select a tournament
        to display players.

        Returns:
            list: List of player dictionaries for the selected tournament.
        """
        # Get a list of tournaments
        user_input, tournaments = self.get_selected_tournament()

        # Find the selected tournament by ID and return its players
        for i in range(len(tournaments)):
            if user_input == str(tournaments[i]['id']):
                return tournaments[i]["list_players"]

    def all_tournaments(self):
        """Display all tournament reports."""
        # Get a list of tournaments from the database and display the report
        self.reports_view.display_tournaments_report(
            TournamentDatabase().load_tournament_list())
        # Ask if user wants to view another report
        self.get_another_report_choice()

    def tournament_rounds(self):
        """Display all rounds from a selected tournament"""
        # Prompt the user to select a tournament
        user_input, tournaments = self.get_selected_tournament()

        # Get the selected tournament
        selected_tournament = tournaments[int(user_input) - 1]

        # Display the tournament header
        self.menu_view.report_header(selected_tournament)

        # Display the round report for the selected tournament
        self.reports_view.display_rounds_report(
            selected_tournament["list_rounds"]
        )

        # Ask if user wants to view another report
        self.get_another_report_choice()

    def display_tournament_matches(self):
        """
        Displays all matches from a tournament
        """
        # Prompt the user to select a tournament
        user_input, tournaments = self.get_selected_tournament()

        # Display the header for the selected tournament
        self.menu_view.report_header(tournaments[int(user_input) - 1])

        # Get all rounds from the selected tournament
        rounds = tournaments[int(user_input) - 1]["list_rounds"]

        # Get all matches from each round
        matches = []
        for round in rounds:
            for match in round[3]:
                matches.append(match)

        # Display the matches report
        self.reports_view.display_matches_report(matches)

        # Ask if user wants to view another report
        self.get_another_report_choice()

    def get_selected_tournament(self):
        """load all tournaments for selection

        @return: user selection, list of all tournaments
        """
        self.menu_view.all_tournaments()
        tournaments = TournamentDatabase().load_tournament_list()
        self.menu_tournament.select_tournament(tournaments)
        self.menu_view.msg_input_prompt("select tournament")
        user_input = input()
        if user_input == "back":
            self.return_to_main_menu()

        elif not user_input.isdigit() or int(user_input) < 1 \
                or int(user_input) > len(tournaments):
            print("Invalid input. Please enter a valid tournament ID.")
            print('test1')
            self.get_selected_tournament()

        else:
            return user_input, tournaments

    @staticmethod
    def return_to_main_menu():
        """Go back to the main menu"""
        from Controller.main_menu import MenuController
        MenuController().main_menu()
