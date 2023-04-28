import datetime
import json

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
        self.player_db = TinyDB('./database/players.json')

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
