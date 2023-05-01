import datetime
import json

from tinydb import TinyDB


class Tournament:
    def __init__(self,
                 tournament_id: int,
                 name: str,
                 location: str,
                 start_date: datetime,
                 end_date: datetime,
                 description: str,
                 nb_current_round: int,
                 list_players: list,
                 list_rounds: list,
                 rounds_total=4
                 ):
        self.tournament_id = tournament_id
        self.name = name
        self.location = location
        self.start_date = datetime.datetime.strptime(
            start_date, '%d/%m/%Y').date()
        self.end_date = datetime.datetime.strptime(
            end_date, '%d/%m/%Y').date()
        self.description = description
        self.nb_current_round = nb_current_round
        self.list_players = list_players
        self.list_rounds = list_rounds
        self.rounds_total = rounds_total
        self.tournament_db = TinyDB('./Database/tournament_db.json')

    def to_dict_(self):
        return {
            "id": self.tournament_id,
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime('%d/%m/%Y'),
            "end_date": self.end_date.strftime('%d/%m/%Y'),
            "description": self.description,
            "nb_current_round": self.nb_current_round,
            "rounds_total": self.rounds_total,
            "list_players": self.list_players,
            "list_rounds": self.list_rounds,
        }

    def sort_players_by_rank(self):
        """
        Sorts a list of players by their rank in ascending order.

        Args: - players (list): A list of player dictionaries,
        where each dictionary contains a 'name' and 'rank'
        key-value pair.

        Returns:
        - A new list of player dictionaries sorted
        by their rank in ascending order.
        """

        # Use the built-in `sorted` function
        # to sort the list of players by their rank
        sorted_players = sorted(self.list_players,
                                key=lambda player: player['rank'])

        return sorted_players

    def sort_players_by_score(self):
        """
        Sorts a list of players by their score in descending order.

        Args: - players (list): A list of player dictionaries,
         where each dictionary contains a 'name' and 'score'
        key-value pair.

        Returns:
        - A new list of player dictionaries sorted
        by their score in descending order.
        """

        # Use the built-in `sorted` function to sort the list
        # of players by their score in descending order
        sorted_players = sorted(self.list_players,
                                key=lambda player: (player["score"],
                                                    -player["rank"]),
                                reverse=True)

        return sorted_players

    def update_tournament_db(self):
        """
        Updates tournament information (after each round) in the database.
        """

        tournament_table = self.tournament_db
        tournament_info = {
            'list_rounds': self.list_rounds,
            'list_players': self.list_players,
            'nb_current_round': self.nb_current_round
        }
        tournament_table.update(tournament_info, doc_ids=[self.tournament_id])

    def update_timer(self, timer: str, info: str):
        """
        Update the start or end timer of the tournament.
        """
        db = self.tournament_db
        db.update({info: timer}, doc_ids=[self.tournament_id])


# Define a class to represent a player database
class TournamentDatabase:
    def __init__(self):
        # Initialize the list of tournament
        # and load tournament data from JSON file
        self.tournament_list = []
        self.filename = './Database/tournament_db.json'
        self.db = TinyDB(self.filename)
        tournament_table = self.db.table('_default')
        self.tournament_list = tournament_table.all()

    # ADD a tournament to the database
    def add_new_tournament(self, tournament):
        # Insert the tournament data to the list of tournament
        self.db.insert(tournament)

    def load_tournament_list(self):
        # Load the JSON file and parse it as a Python object
        tournament_table = self.db.table('_default')
        tournament = tournament_table.all()
        return tournament

    def load_tournament_from_JSON(self):
        # Load the JSON file and parse it as a tournament object
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return data
