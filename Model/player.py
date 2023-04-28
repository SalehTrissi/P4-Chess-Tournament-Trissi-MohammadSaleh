import datetime
import json

import tinydb
from tinydb import TinyDB


# Define a class to represent a player.py
class Players:
    def __init__(self,
                 player_id: int,
                 first_name: str,
                 last_name: str,
                 gender: str,
                 rank: int,
                 date_of_birth: datetime,
                 ):
        """ Initialize the player. By's attributes"""
        self.player_id = player_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.rank = rank
        self.score = 0.0
        self.opponents = []
        self.date_of_birth = datetime.datetime.strptime(
            date_of_birth, '%d/%m/%Y').date()
        self.player_db = TinyDB('./Database/players.json')

    def to_dict(self):
        return {
            'player_id': self.player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.isoformat(),
            "rank": self.rank,
            "score": self.score,
            "opponents": self.opponents
        }


# Define a class to represent a player.py database
class PlayersDatabase:
    def __init__(self):
        # Initialize the list of players and
        # load player data from the JSON file
        self.players_list = []
        self.players_db = './Database/players_db.json'
        self.db = TinyDB(self.players_db)
        players_table = self.db.table('_default')
        self.players_list = players_table.all()

    # Add a player to the database
    def add_player(self, player):
        # Insert the player data to the player table
        self.db.insert(player)

    def load_players_db(self):
        # Load the player data from the database
        players_table = self.db.table('_default')
        players = players_table.all()
        return players

    def load_players_from_json(self):
        # Load the JSON file and parse it as a Python object
        with open(self.players_db, 'r') as f:
            players_list = json.load(f)
        return players_list

    def update_player(self):
        # Load the player data from the database
        players = self.load_players_db()
        # Print a list of all players for the user to choose from
        print("Select a player to update:")
        for player in players:
            print(f"\t[{player['player_id']}]: "
                  f"{player['first_name']} {player['last_name']}")
        selected_player_id = int(input(
            "\nEnter the player_id of the player to update: ")
        )

        # Find the player in the player table by player_id
        players_table = self.db.table('_default')
        player_query = tinydb.Query()
        player = players_table.get(
            player_query.player_id == selected_player_id
        )

        # Prompt the user for new information to update
        if player:
            new_player_data = {}
            print(f"Current information for player :")
            print(f"\t- First name: {player['first_name']}")
            print(f"\t- Last name: {player['last_name']}")
            print(f"\t- Gender: {player['gender']}")
            print(f"\t- Date of birth: {player['date_of_birth']}")
            new_player_data['first_name'] = input(
                "1- Enter new first name (press enter to keep current value): "
            )
            new_player_data['last_name'] = input(
                "2- Enter new last name (press enter to keep current value): "
            )
            new_player_data['gender'] = input(
                "3- Enter new gender [M/F] "
                "(press enter to keep current value): "
            )
            new_date_of_birth = input(
                "4- Enter new date of birth "
                "(DD/MM/YYYY format, press enter to keep current value): "
            )

            if new_date_of_birth:
                new_player_data['date_of_birth'] = \
                    datetime.datetime.strptime(
                        new_date_of_birth, '%d/%m/%Y').date().isoformat()

            # Update the player data
            players_table.update(
                new_player_data, player_query.player_id == selected_player_id
            )

            print(f"\t\nPlayer {player['player_id']} updated successfully!")
        else:
            print(
                f"Player with player_id "
                f"{selected_player_id} not found in the database"
            )
