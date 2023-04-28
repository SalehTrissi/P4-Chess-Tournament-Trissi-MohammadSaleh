import datetime

from Controller.tournament import MenuTournamentController
from Model.tournament import TournamentDatabase, Tournament


class CreateNewTournament:
    def __init__(self):
        self.new_tournament_menu()

    @staticmethod
    def get_next_tournament_id(database):
        if not database.tournament_list:
            return 1
        return len(database.tournament_list) + 1

    @staticmethod
    def validate_input(prompt):
        """
        Validate the user input.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The user's input.
        """
        while True:
            user_input = input(prompt)
            if user_input.strip() == "":
                print("[Error]: Input cannot be blank.")
            else:
                return user_input

    @staticmethod
    def validate_date(prompt, start_date=None):
        """
        validate the input date.

        Args:
            prompt (str): The prompt to display to the user.
            start_date (str): The start date of the tournament.

        returns:
            str: The formatted input date.
        """
        while True:
            try:
                input_date = input(prompt)
                date = datetime.datetime.strptime(input_date,
                                                  '%d/%m/%Y').date()
                today = datetime.date.today()
                if start_date and date < datetime.datetime.strptime(
                        start_date, '%d/%m/%Y').date():
                    print("[Error]: End date cannot be before start date.")
                elif date < today:
                    print("[Error]: Date cannot be in the past.")
                else:
                    return input_date
            except ValueError:
                print(
                    "[Error]: Enter a valid date in the format (DD/MM/YYYY).")

    def new_tournament_menu(self):
        """
        Add a new tournament to the tournament database.
        """
        try:
            database = TournamentDatabase()

            tournament_id = self.get_next_tournament_id(database)

            tournament_name = self.validate_input(
                "1- Enter the name of tournament: "
            )

            tournament_location = self.validate_input(
                "2- Enter the location of tournament: "
            )

            tournament_start_date = self.validate_date(
                "3- Enter the start date of the tournament (DD/MM/YYYY): "
            )

            tournament_end_date = self.validate_date(
                "4- Enter the end date of the tournament (DD/MM/YYYY): ",
                start_date=tournament_start_date,
            )

            tournament_description = self.validate_input(
                "5- Enter the description of the tournament: "
            )

            tournament_players = MenuTournamentController().select_players(8)

            tournament = Tournament(
                tournament_id,
                tournament_name,
                tournament_location,
                tournament_start_date,
                tournament_end_date,
                tournament_description,
                nb_current_round=1,
                list_players=tournament_players,
                list_rounds=[],
            )

            database.add_new_tournament(tournament.to_dict_())

            print("The tournament has been successfully added.")

        except Exception as e:
            print(f"Error occurred: {e}")
