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

    def start_tournament(self, tournament):
        """
        Starts a tournament or resumes it if it was already started.
        Sets start and end timers and save to a database.
        """
        # If the tournament has not started yet, start it from the first round
        if tournament.nb_current_round == 1:
            tournament.start_date = datetime.now().strftime('%d/%m/%Y')
            tournament.update_timer(tournament.start_date, 'start_date')
            random.shuffle(tournament.list_players)  # Shuffle players randomly
            self.first_round(tournament)
            tournament.nb_current_round += 1
            tournament.update_tournament_db()

        elif 1 < tournament.nb_current_round <= tournament.rounds_total:
            # Resume the tournament from the current round
            for round_num in range(tournament.nb_current_round,
                                   tournament.rounds_total + 1):
                self.create_next_rounds(tournament)
                tournament.nb_current_round += 1
                tournament.update_tournament_db()

            # End the tournament
            tournament.end_date = datetime.now().strftime('%d/%m/%Y')
            tournament.update_timer(tournament.end_date, 'end_date')
            self.tournament_end(tournament)

        else:
            self.tournament_end(tournament)

        # Play all the remaining rounds
        while tournament.nb_current_round <= tournament.rounds_total:
            self.create_next_rounds(tournament)
            tournament.nb_current_round += 1
            tournament.update_tournament_db()

        # End the tournament
        tournament.end_date = self.timer
        tournament.update_timer(tournament.end_date, 'end_date')
        self.tournament_end(tournament)

    def first_round(self, tournament):
        """
        Plays the first round of a tournament by pairing random players
        with each other. Saves the results to the database.
        """

        # Create a new round with the name "Round 1", the current timer value,
        # and the end data to be determined
        round_obj = Round("Round 1", self.timer, "TBD")

        # Sort the list of players in the tournament by rank
        tournament.sort_players_by_rank()

        # Shuffle the list of players in the tournament randomly
        random.shuffle(tournament.list_players)

        # Set the start_datetime value if it is not set
        if not round_obj.start_datetime:
            round_obj.start_datetime = \
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Display the round header and print the round object
        self.round_view.display_round_header(
            tournament, 1, round_obj.start_datetime)
        # Play each match in the round and update the players' opponents
        for i in range(0, len(tournament.list_players), 2):
            round_obj.get_match_pairing(tournament.list_players[i],
                                        tournament.list_players[i + 1])
            tournament.list_players[i], tournament.list_players[i + 1] = \
                self.update_opponents(
                    tournament.list_players[i], tournament.list_players[i + 1])
        # Display the matches and ask the user to input scores
        self.enter_scores_and_update_round(tournament, round_obj)

    def enter_scores_and_update_round(self, tournament, round_obj):
        # Display the matches and ask the user to input scores
        self.round_view.display_matches(round_obj.matches)
        self.round_view.round_over()

        while True:
            self.menu_view.input_msg()
            user_input = input("'ok' to proceed, 'back' to go back: ").lower()
            scores_list = []

            if user_input == 'ok':
                # Enter the matches if the user entered 'ok'

                # Set the end datetime of the current round to the timer
                round_obj.end_datetime = datetime.now().strftime('%d/%m/%Y')

                # Add the updated round to the tournament's list of rounds
                tournament.list_rounds.append(round_obj.set_round())
                # Enter the results of the matches using the provided scores
                # list
                self.enter_results_of_matches(scores_list, tournament)
                break

            elif user_input == 'back':
                # return to the main menu if the user entered 'back'
                return self.return_to_main_menu()

            else:
                print("Error: invalid input. Please enter 'ok' to proceed "
                      "or 'back' to go back.")

    # Define a static method to update opponents for two players
    @staticmethod
    def update_opponents(player_1, player_2):
        """
        Updates the opponent list for two players.
        :param player_1: A dictionary representing the first player.
        :param player_2: A dictionary representing the second player.
        :return: A tuple of two dictionaries representing
        the updated players.
        """
        if player_2["player_id"] not in player_1["opponents"]:
            player_1["opponents"].append(player_2["player_id"])
        if player_1["player_id"] not in player_2["opponents"]:
            player_2["opponents"].append(player_1["player_id"])
        return player_1, player_2

    def create_next_rounds(self, tournament):
        """Set possible pairings """

        # Create a new round object
        round_number = tournament.nb_current_round
        round_name = f"Round {round_number}"
        round_obj = Round(round_name, self.timer, "TBD")

        # Sort players by score
        tournament.sort_players_by_score()

        # Display round header
        self.round_view.display_round_header(
            tournament, round_number, round_obj.start_datetime)

        # Set up variables for pairing algorithm
        available_players = tournament.list_players.copy()
        players_added = []
        rounds_total = tournament.rounds_total

        for k in range(rounds_total):

            if available_players[1]["player_id"] \
                    in available_players[0]["opponents"]:
                try:
                    available_list, players_added = self.match_other_option(
                        available_players, players_added, round_obj
                    )
                    tournament.list_players = players_added
                except IndexError:
                    available_list, players_added = self.match_first_option(
                        available_players, players_added, round_obj
                    )
                    tournament.list_players = players_added
            else:
                available_list, players_added = self.match_first_option(
                    available_players, players_added, round_obj
                )
                tournament.list_players = players_added

        # Display the matches and ask the user to input scores
        self.enter_scores_and_update_round(tournament, round_obj)

    def match_first_option(self, available_list, players_added, round_obj):
        """main pairing option

        @param available_list: list of players not set in match
         for a current round
        @param players_added: list of players already in match
        @param round_obj: current round
        @return: updated lists
        """
        round_obj.get_match_pairing(available_list[0], available_list[1])
        available_list[0], available_list[1] = \
            self.update_opponents(available_list[0], available_list[1])

        available_list, players_added = self.update_player_lists(
            available_list[0],
            available_list[1],
            available_list,
            players_added
        )

        return available_list, players_added

    def match_other_option(self, available_list, players_added, round_obj):
        """alternative pairing option

        @param available_list: list of players not set in match
        for a current round
        @param players_added: list of players already in match for
        @param round_obj: current round
        @return: updated lists
        """
        player1, player2 = None, None
        for i in range(len(available_list)):
            for j in range(i + 1, len(available_list)):
                if (available_list[i]["player_id"] not in available_list[j][
                    "opponents"]
                        and available_list[j]["player_id"] not in
                        available_list[i]["opponents"]):
                    player1, player2 = available_list[i], available_list[j]
                    break
            if player1 is not None:
                break

        if player1 is None:
            # fallback option if no unique pair can be found
            player1, player2 = available_list[0], available_list[1]

        round_obj.get_match_pairing(player1, player2)
        player1, player2 = self.update_opponents(player1, player2)

        available_list, players_added = self.update_player_lists(
            player1,
            player2,
            available_list,
            players_added
        )

        return available_list, players_added

    @staticmethod
    def update_player_lists(player_1, player_2, available_list, players_added):
        """update player lists:
        Add unavailable player to the respective list
        Remove available player from the respective list

        @param player_1: player 1 (dict)
        @param player_2: player 2 (dict)
        @param available_list: list of players
        not set in match for a current round
        @param players_added: list of players already
        in match for a current round
        @return: updated list of available players,
        updated list of unavailable players
        """
        players_added.extend([player_1, player_2])
        available_list.remove(player_1)
        available_list.remove(player_2)

        return available_list, players_added

    def enter_results_of_matches(self, scores_list: list, tournament):
        """updates the scores of the players at the end of a round.

        args:
            scores_list (list): A list of scores for each player.
            tournament (Tournament): The current tournament.

        returns:
            list: A list of players with their scores updated.
        """
        # Iterate over the rounds in the tournament.
        for i in range(tournament.rounds_total):
            # Display the score options to the user.
            self.round_view.score_options(i + 1)

            # Ask the user to input scores.
            response = self.input_scores()

            # Update the score list with the user's input.
            scores_list = self.get_score(response, scores_list)

        # Update the scores of the players in the tournament.
        tournament.list_players = self.update_scores(
            tournament.list_players, scores_list)

        return tournament.list_players

    def input_scores(self):
        """
        Prompts the user to input scores and returns the response.

        Returns:
        int -- the user's response
        """
        while True:
            self.round_view.score_input_prompt()
            response = input().strip()
            if response == 'back':
                print("Returning to main menu...")
                return self.return_to_main_menu()
            elif response.isdigit() and int(response) in range(3):
                return int(response)
            else:
                print("Invalid input. Please enter '0', '1', '2', or 'back'.")

    def get_score(self, response, scores_list: list):
        """input scores for each match in the current round

        @param response: user input (int)
        @param scores_list: list of scores
        @return: updated list of scores
        """
        if response == 0:
            scores_list.extend([0.5, 0.5])
        elif response == 1:
            scores_list.extend([1.0, 0.0])
        elif response == 2:
            scores_list.extend([0.0, 1.0])
        elif response == "back":
            return self.return_to_main_menu()
        else:
            self.menu_view.invalid_input()
            return self.get_score(self.input_scores(), scores_list)

        # Commit the score input to the database
        try:
            # code to commit the score input to the database
            print("Score input committed to database.")
        except Exception as e:
            print(f"Error committing score input to database: {e}")

        return scores_list

    @staticmethod
    def update_scores(players, scores_list: list):
        """update player scores

        @param players: list of the players
        @param scores_list: list of a score
        @return: list of players with updated scores
        """
        for i in range(len(players)):
            players[i]["score"] += scores_list[i]

        # Commit the updated scores to the database
        try:
            # code to commit the updated scores to the database
            print("Updated scores committed to database.")
        except Exception as e:
            print(f"Error committing updated scores to database: {e}")

        return players

    def tournament_end(self, tournament):
        """End of tournament: display final results and offer user to update
        ranks.

        @param tournament: Current tournament object
        """

        # Sort players by rank
        tournament.sort_players_by_rank()

        # Display the final results of the tournament
        self.round_view.display_results(tournament)

        self.menu_view.msg_return_main_menu()
        print("Or press any other key to exit: ", end="")
        user_input = input().lower()

        if user_input in ["back", "return"]:
            # If the user chooses to return to the main menu,
            # go back to the main menu
            self.return_to_main_menu()
        else:
            # If the user enters something else, display an error message
            # and re-ask the question
            self.menu_view.invalid_input()
            # Call the function recursively until a valid input is given
            self.tournament_end(tournament)

    @staticmethod
    def return_to_main_menu():
        from Controller.main_menu import MenuController
        MenuController().main_menu()
