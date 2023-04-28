from prettytable import prettytable


# Initialize the Report class and set the required field names
# for each report type
class Reports:
    def __init__(self):
        # Create a PrettyTable object for each report type
        self.table = prettytable.PrettyTable()

        # Set the required field names for a player report
        self.player_report_filed_names = [
            "ID",
            "Last name",
            "First name",
            "Gender",
            "Date of birth",
            "Rank"
        ]

        # Set the required field names for a tournament report
        self.tournament_report_field_names = [
            "ID",
            "Name",
            "Location",
            "Description",
            "Start date",
            "End date",
            "Last round played",
            "Players (ID : Name)",
        ]

        # Set the required field names for matches report
        self.matches_report_field_names = [
            "Name P1",
            "Rank P1",
            "Score P1",
            " ",
            "Name P2",
            "Rank P2",
            "Score P2"
        ]

        # Set the required field names for a round report
        self.rounds_report_field_names = [
            "Round #",
            "Started at",
            "Ended at",
            "Matches"
        ]

    def display_players(self, players, sorting):
        """Display player report (all sorting types)

        Args:
            players (list): List of player dictionaries
            sorting (str): Sorting type (by ID, rank, or last name)
        """
        self.table.clear()
        self.table.field_names = self.player_report_filed_names
        self.table.align = "l"

        for i in range(len(players)):
            self.table.add_row([
                players[i]["player_id"],
                players[i]["last_name"],
                players[i]["first_name"],
                players[i]["gender"],
                players[i]["date_of_birth"],
                players[i]["rank"]
            ])

        print(f"\n\n\n- All players ({sorting}) -\n")
        print(self.table)

    def display_tournaments_report(self, tournaments):
        """Display tournament reports"""

        # Reset any previous data from the table
        self.table.clear()

        # Set the field names for the tournament report
        self.table.field_names = self.tournament_report_field_names

        # Align the data to the left for better readability
        self.table.align = "l"

        # Iterate over each tournament and add the required data to the table
        for tournament in tournaments:
            participants = []
            players = tournament["list_players"]

            # Add the ID and last name of each player in the tournament
            # to the participant list
            for player in players:
                participants.append(
                    "Id [" + str(player["player_id"]) + "] : " +
                    player["last_name"] + " " + player["first_name"]
                )

            # Add the tournament data to the table row by row
            self.table.add_row([
                tournament["id"],
                tournament["name"],
                tournament["location"],
                tournament["description"],
                tournament["start_date"],
                tournament["end_date"],
                str(tournament["nb_current_round"] - 1) + "/" +
                str(tournament["rounds_total"]),
                participants
            ])

        # Print the table with tournament data
        print("\n\n\n- All tournaments -\n")
        print(self.table)

    def display_rounds_report(self, rounds):
        """Display rounds in a tournament report"""

        # Reset any previous data from the table
        self.table.clear()

        # Set the field names for the round report
        self.table.field_names = self.rounds_report_field_names

        # Align the data to the left for better readability
        self.table.align = "l"

        for round_data in rounds:
            for i, match_data in enumerate(round_data[3]):
                # Add the match data to the table,
                # with additional space in the first row for better readability
                if i == 0:
                    self.table.add_row([
                        round_data[0],  # Round #
                        round_data[1],  # Started at
                        round_data[2],  # Ended at
                        match_data  # Match data
                    ])
                else:
                    self.table.add_row([
                        '',  # Empty space to align the data
                        '',  # Empty space to align the data
                        '',  # Empty space to align the data
                        match_data  # Match data
                    ])

        # Print the table with rounds data
        print("\n\n- All rounds -\n")
        print(self.table)

    def display_matches_report(self, matches):
        """
        Displays a report of all matches in a tournament
        """
        # Reset the table and set the field names and alignment
        self.table.clear()
        self.table.field_names = self.matches_report_field_names
        self.table.align = "l"

        # Add the "vs." string to the middle of each match
        #  and add it to the table
        for match in matches:
            match.insert(3, "vs.")
            self.table.add_row(match)

        # Display the matches report
        print(f"\n\n- All played matches ({len(matches)} total) -\n")
        print(self.table)

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
