import datetime

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
                 round_total=4
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
        self.round_total = round_total
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
            "round_total": self.round_total,
            "list_players": self.list_players,
            "list_rounds": self.list_rounds,
        }
