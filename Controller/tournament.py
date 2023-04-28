import random
from datetime import datetime

from texttable import Texttable
from Model.round import Round
from Model.tournament import Tournament, TournamentDatabase
from View.menu import MenuView
from View.round import RoundViews


class MenuTournamentController:
    def __init__(self):
        self.round_view = RoundViews()
        self.timer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.menu_view = MenuView()

    @staticmethod
    def select_tournament(tournaments):
        """
        Display all tournaments for select one
        :return: list of tournament
        """
        table = Texttable()
        table.header(
            ["ID", "Name", "Location", "Description", "Start Date", "End Date",
             "Round"])

        for tournament in tournaments:
            row = [
                tournament['id'],
                tournament['name'],
                tournament['location'],
                tournament['description'],
                tournament['start_date'],
                tournament['end_date'],
                f"{tournament['nb_current_round'] - 1}/"
                f"{tournament['rounds_total']}"
            ]
            table.add_row(row)

        print(table.draw().center(100))

    def load_tournament(self):
        """Select an existing tournament to resume."""
        # Load the list of existing tournaments from the database
        tournament_list = TournamentDatabase().load_tournament_list()
        # Prompt the user to select a tournament
        self.select_tournament(tournament_list)

        # Loop until a valid tournament ID is entered
        while True:
            # Ask the user to enter the ID
            # of the tournament they want to resume
            tournament_id = input(
                "\n- Choose a tournament using the ID number: ")

            # Check if the input is a valid integer
            if not tournament_id.isdigit():
                # If not, print an error message and continue the loop
                print(f"\nInvalid input: {tournament_id}."
                      f" Please enter a valid integer ID.")
                continue

            # Loop through the list of tournaments
            # to find the one with the matching ID
            for tournament_data in tournament_list:
                if int(tournament_id) == tournament_data["id"]:

                    # If a matching tournament is found,
                    # create a Tournament object from its data
                    tournament = self.create_tournament_from_data(
                        tournament_data)
                    # Start the tournament
                    self.start_tournament(tournament)
                    # Return from the function
                    return

            # If no matching tournament is found,
            # print an error message and continue the loop
            print(f"\nInvalid input: {tournament_id}."
                  f" Please choose a valid tournament ID "
                  f"from the following options:")
            for tournament_data in tournament_list:
                # Print a list of all the available tournaments
                print(f"{tournament_data['id']} - {tournament_data['name']}"
                      f" ({tournament_data['location']})")

    @staticmethod
    def create_tournament_from_data(tournament_data):
        """Create a Tournament object from the given data dictionary."""
        return Tournament(
            tournament_data["id"],
            tournament_data["name"],
            tournament_data["location"],
            tournament_data["start_date"],
            tournament_data["end_date"],
            tournament_data["description"],
            tournament_data["nb_current_round"],
            tournament_data["list_players"],
            tournament_data["list_rounds"],
            tournament_data["rounds_total"]
        )
    