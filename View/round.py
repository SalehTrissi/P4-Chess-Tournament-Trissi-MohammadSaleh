from prettytable import prettytable

from View.menu import MenuView

ROUND_FIELD_NAMES = [
    "Match #",
    "Full name P1",
    "Rank P1",
    "Score P1",
    "V.S",
    "Full name P2",
    "Rank P2",
    "Score P2"
]

RESULTS_FIELD_NAMES = [
    "Tournament ranking",
    "Name",
    "Final Score",
    "Global ranking"
]


class RoundViews:
    def __init__(self):
        self.match_table = prettytable.PrettyTable()
        self.menu_view = MenuView()

    def display_matches(self, matches):
        """display matches for current round as table

        @param matches: list of matches tuples
        """
        self.match_table.clear()
        self.match_table.field_names = ROUND_FIELD_NAMES

        # sort matches by descending score of player 1
        matches_sorted = sorted(
            matches, key=lambda players: players[5], reverse=True
        )

        for i in range(len(matches_sorted)):
            row = list(matches_sorted[i])
            row.insert(0, f"Match {i + 1}")
            row.insert(4, "vs.")
            self.match_table.add_row(row)

        print(self.match_table)

    @staticmethod
    def display_round_header(tournament, round_number, start_time):
        """Display tournament info as a round header

        @param tournament: The current tournament is
        @param round_number: the number of the current round
        @param start_time: the start time of the round (str)
        """
        print("\n\n")

        header_1 = f"{tournament.name.upper()}, " \
                   f"{tournament.location.title()} | " \
                   f"Description: {tournament.description}"
        header_2 = f"Start: {tournament.start_date} | " \
                   f"End: {tournament.end_date} \n"
        header_3 = f"- ROUND {round_number}/{tournament.rounds_total} | " \
                   f"{start_time} -\n"

        print(header_1.center(100, " "))
        print(header_2.center(100, " "))
        print(header_3.center(100, " "))

    def display_results(self, tournament):
        """
        Display results at the end of the tournament

        Args:
            tournament (Tournament): current tournament object
        """
        # Reset the table and set the field names to be displayed
        self.match_table.clear()
        self.match_table.field_names = ['Rank', 'Player', 'Score', 'Ranking']

        # Sort the players by score
        sorted_players = sorted(tournament.list_players,
                                key=lambda players: players["score"],
                                reverse=True)

        # Add each player's information to the table
        for i, player in enumerate(sorted_players):
            score_rounded = round(player["score"])
            self.match_table.add_row([
                i + 1,
                player["last_name"] + ", " + player["first_name"],
                score_rounded,
                player["rank"]
            ])

        self.menu_view.header_final_scour(tournament)
        # Print the table with player information
        print(self.match_table)

    @staticmethod
    def round_over():
        print("\n- Is this round over? [ok] ")
        print("- Return back main menu: [back] ")

    @staticmethod
    def score_options(match_number: int):
        """Displays the available score options for a given match.

        Args:
            match_number (int): The number of the match.

        Returns:
            None
        """
        # Display the available score options,
        # including the names of the players.
        print(f"\nMatch {match_number}:")
        print("[0] Draw")
        print("[1] Player 1 wins")
        print("[2] Player 2 wins")
        print("\n[back] Back to main menu")

    @staticmethod
    def score_input_prompt():
        print('\nEnter the match result please: ', end=' ')
