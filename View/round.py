from prettytable import prettytable

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

    def display_matches(self, matches):
        """Display matches for the current round as table.

        Args:
            matches (list): A list of match tuples.
        """
        # Clear any existing data in the table.
        self.match_table.clear()

        # Set the field names to the values in ROUND_FIELD_NAMES.
        self.match_table.field_names = ROUND_FIELD_NAMES

        # Add each match to the table as a row.
        for i, match in enumerate(matches):
            # Convert the match tuple to a list.
            row = list(match)

            # Add the match number and "vs." to the row.
            row.insert(0, f"Match {i+1}")
            row.insert(4, "vs.")

            # Add the row to the table.
            self.match_table.add_row(row)

        # Print the table.
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

        print(header_1.center(70, " "))
        print(header_2.center(70, " "))
        print(header_3.center(70, " "))

    def display_results(self, tournament):
        """
        Display results at the end of the tournament

        Args:
            tournament (Tournament): current tournament object
        """
        # Reset the table and set the field names to be displayed
        self.match_table.reset()
        self.match_table.field_names = RESULTS_FIELD_NAMES

        # Add each player's information to the table
        for i in range(len(tournament.list_players)):
            self.match_table.add_row([
                i + 1,
                tournament.list_players[i]["last_name"] + ", " +
                tournament.list_players[i]["first_name"],
                tournament.list_players[i]["score"],
                tournament.list_players[i]["rank"]
            ])

        # Print the final scores and tournament details
        print("\n\n- FINAL SCORES -\n")
        print(f"{tournament.name.upper()}, {tournament.location.title()} | "
              f"Description : {tournament.description}")
        print(f"Start : {tournament.start_date} | "
              f"End : {tournament.end_date} \n")

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
