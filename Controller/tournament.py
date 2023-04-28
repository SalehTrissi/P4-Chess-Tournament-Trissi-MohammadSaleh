from datetime import datetime
from texttable import Texttable
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
