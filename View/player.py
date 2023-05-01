import datetime

from Model.player import PlayersDatabase, Players


class AddPlayerMenu:
    def __init__(self):
        self.new_player()

    @staticmethod
    # Function to validate the player's gender input
    def validate_gender_input():
        while True:
            gender = input("3- Enter player's gender (M/F): ").upper()
            if gender in ['M', 'F']:
                return gender
            else:
                print("*** [Error] : Invalid input. Please enter 'M' or 'F'.")

    @staticmethod
    # Function to validate the player's date of birth input
    def validate_date_of_birth_input():
        while True:
            date_of_birth = input(
                "4- Enter player date of birth (DD/MM/YYYY): "
            )
            try:
                return datetime.datetime.strptime(date_of_birth, '%d/%m/%Y')
            except ValueError:
                print("*** [Error] : "
                      "Enter a valid date in the format (DD/MM/YYYY).")

    @staticmethod
    # Function to get the next available player ID and rank
    def get_next_id_and_rank(database):
        if len(database.players_list) == 0:
            return 1, 1
        else:
            player_id = len(database.players_list) + 1
            rank = len(database.players_list) + 1
            return player_id, rank

    # Function to validate the input for a new player
    def validate_player_input(self):
        while True:
            try:
                first_name = input("1- Enter player first name: ")
                if not first_name or len(first_name) > 50:
                    raise ValueError("Invalid first name")

                last_name = input("2- Enter player last name: ")
                if not last_name or len(last_name) > 50:
                    raise ValueError("Invalid last name")

                gender = self.validate_gender_input()
                date_of_birth = self.validate_date_of_birth_input()

                return first_name, last_name, gender, date_of_birth

            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

    # Function to add a new player to the database
    def new_player(self):
        database = PlayersDatabase()
        while True:
            try:
                num_players = int(input(
                    "How many players do you want to add? "
                ))
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

        player_id, rank = self.get_next_id_and_rank(database)

        for i in range(num_players):
            print(f"\nAdding player {i + 1} of {num_players}")
            first_name, last_name, gender, date_of_birth = \
                self.validate_player_input()

            player = Players(
                player_id, first_name, last_name, gender, rank,
                date_of_birth.strftime('%d/%m/%Y')
            )
            database.add_player(player.to_dict())

            print("Player added successfully")

            player_id += 1
            rank += 1

        print(f"\n{num_players} players added to the database.")
