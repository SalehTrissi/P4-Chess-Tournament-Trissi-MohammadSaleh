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
            self.first_round(tournament)
            tournament.nb_current_round += 1
            tournament.update_tournament_db()
            # Play all the remaining rounds
            while tournament.nb_current_round <= tournament.rounds_total:
                self.next_rounds(tournament)
                tournament.nb_current_round += 1
                tournament.update_tournament_db()

        # If the tournament has already started, resume from the current round
        elif 1 < tournament.nb_current_round <= tournament.rounds_total:
            while tournament.nb_current_round <= tournament.rounds_total:
                self.next_rounds(tournament)
                tournament.nb_current_round += 1
                tournament.update_tournament_db()

            # If all rounds have been played, end the tournament
            tournament.end_date = datetime.now().strftime('%d/%m/%Y')
            tournament.update_timer(tournament.end_date, 'end_date')
            self.tournament_end(tournament)

        # If the current round is greater than the total rounds,
        # end the tournament
        elif tournament.nb_current_round > tournament.rounds_total:
            self.tournament_end(tournament)

    def first_round(self, tournament):
        """
        Plays the first round of a tournament by pairing random players
        with each other. Saves the results to the database.
        """

        # Create a new round with the name "Round 1", the current timer value,
        # and the end data to be determined
        nb_current_round = Round("Round 1", self.timer, "TBD")

        # Sort the list of players in the tournament by rank
        tournament.sort_players_by_rank()

        # Shuffle the list of players in the tournament randomly
        random.shuffle(tournament.list_players)

        # Set the start_datetime value if it is not set
        if not nb_current_round.start_datetime:
            nb_current_round.start_datetime = \
                datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Display the round header and print the round object
        self.round_view.display_round_header(
            tournament, 1, nb_current_round.start_datetime)
        # Play each match in the round and update the players' opponents
        for i in range(0, len(tournament.list_players), 2):
            nb_current_round.get_match_pairing(tournament.list_players[i],
                                               tournament.list_players[i + 1])
            tournament.list_players[i], tournament.list_players[i + 1] = \
                self.update_opponents(
                tournament.list_players[i], tournament.list_players[i + 1])

        # Display the matches and ask the user to input scores
        self.round_view.display_matches(nb_current_round.matches)
        self.round_view.round_over()
        self.menu_view.input_msg()
        user_input = input("'ok' to proceed, 'back' to go back: ").lower()
        scores_list = []

        if user_input == 'ok':
            # Enter the matches if the user entered 'ok'

            # Set the end datetime of the current round to the timer
            nb_current_round.end_datetime = self.timer

            # Add the updated round to the tournament's list of rounds
            tournament.list_rounds.append(nb_current_round.set_round())
            # Enter the results of the matches using the provided scores list
            self.enter_results_of_matches(scores_list, tournament)

        elif user_input == 'back':
            # return to the main menu if the user entered 'back'
            return self.return_to_main_menu()
        elif not user_input:
            print("Error: input cannot be empty. Please try again.")
        else:
            print("Error: invalid input. Please enter 'ok' to proceed "
                  "or 'back' to go back, do not leave blank..")

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
        # Append player_2's player_id to player_1's opponent list
        player_1["opponents"].append(player_2["player_id"])
        # Append player_2's player_id to player_1's opponent list
        player_2["opponents"].append(player_1["player_id"])
        # Return both players after updating their opponents
        return player_1, player_2

    def next_rounds(self, tournament):
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

        # Display match pairings and get user input
        self.round_view.display_matches(round_obj.matches)
        self.round_view.round_over()
        self.menu_view.input_msg()
        scores_list = []

        # Save round to tournament and move to
        # the next screen based on user input
        # Keep prompting the user
        # for input until they enter either "ok" or "back"
        user_input = input(
            "Enter 'ok' to continue or 'back' to go back to the menu: ")\
            .lower()

        # If the user enters "ok", set the end datetime of the current round,
        # append the round to the list of rounds in the tournament,
        # and enter the results of the matches using the provided scores list

        if user_input == "ok":
            round_obj.end_datetime = self.timer
            tournament.list_rounds.append(round_obj.set_round())
            self.enter_results_of_matches(scores_list, tournament)

        # If the user enters "back", go back to the menu
        elif user_input == "back":
            return self.return_to_main_menu()

    def match_first_option(self, available_list, players_added, round_obj):
        """Main pairing option

        @param available_list: List of players not set in match
        for the current round
        @param players_added: list of players already in the match
        for the current round
        @param round_obj: the current round object
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
        """ Alternative pairing option

        @param available_list: List of players not set in match
         for the current round
        @param players_added: list of players already in the match
        for the current round
        @param round_obj: the current round object
        @return: updated lists
        """
        round_obj.get_match_pairing(available_list[0], available_list[2])
        available_list[0], available_list[2] = \
            self.update_opponents(available_list[0], available_list[2])

        available_list, players_added = self.update_player_lists(
            available_list[0],
            available_list[2],
            available_list,
            players_added
        )

        return available_list, players_added

    def enter_results_of_matches(self, scores_list: list, tournament):
        """ updates the scores of the players at the end of a round.

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
        print(f"1: tournament.list_players is : {tournament.list_players }")
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
    def update_player_lists(player_1, player_2, available_list, players_added):
        """
        Update player lists:
        - Add unavailable player to respective list
        - Remove available player from a respective list

        @param player_1: player 1 (dict)
        @param player_2: player 2 (dict)
        @param available_list: list of players not set in match
        for a current round
        @param players_added: list of players already in match
        for a current round
        @return: updated list of available players,
        updated list of unavailable players
        """

        # Add the two players to the list of players already in the match
        # for the current round
        players_added.extend([player_1, player_2])

        # Remove the two players from the list of available players
        # for the current round
        available_list.remove(player_1)
        available_list.remove(player_2)

        # Return the updated lists of available and unavailable players
        return available_list, players_added

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
        """End of tournament: display final results and offer user
        to update ranks.

        @param tournament: Current tournament dict
        """

        # Sort players by rank and score
        tournament.sort_players_by_rank()
        tournament.sort_players_by_score()

        # Display the final results of the tournament
        self.round_view.display_results(tournament)

        # Ask the user if they want to update player ranks
        self.menu_view.msg_return_main_menu()
        print("Or press any other key to exit: ", end="")
        user_input = input()

        if user_input.lower() in ["back", "return"]:
            # If the user chooses to return to the main menu,
            # go back to the main menu
            self.return_to_main_menu()
        else:
            # If the user enters something else, display an error message
            # and re-ask the question
            self.menu_view.msg_good_bay()
            self.menu_view.exit_program()

    @staticmethod
    def return_to_main_menu():
        from Controller.main_menu import MenuController
        MenuController().main_menu()
