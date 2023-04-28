from tinydb import TinyDB
from texttable import Texttable


class MenuPlayerController:
    def __init__(self):
        self.db = TinyDB('./Database/players_db.json')

    def table_list_players(self):
        # Query the database for all players
        players_data = self.db.all()

        # print a message if the data is empty
        if not players_data:
            print('No players found. The table is empty')
            return

        # print the data in a table
        table_data = [
            ['ID', 'First name', 'Last name', 'Gender', 'Date of birth']
        ]
        for player in players_data:
            table_data.append([
                player['player_id'],
                player['first_name'],
                player['last_name'],
                player['gender'],
                player['date_of_birth']
            ])

        table = Texttable()
        table.add_rows(table_data)
        print(table.draw())
