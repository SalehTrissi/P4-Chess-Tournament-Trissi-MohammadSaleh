from tinydb import TinyDB
from texttable import Texttable


class MenuPlayerController:
    def __init__(self):
        self.db = TinyDB('./Database/players_db.json')
        self.players_table = self.db.table('_default')

    def select_players(self, num_players):
        # Load player data from TinyDB
        player_data = self.players_table.all()

        # Check if the 'players' key is present in the player_data dictionary
        if not player_data:
            raise ValueError(
                "The 'players' table is empty in the players_db database.")

        # Create a dictionary of players by ID
        players_dict = {player['player_id']: player for player in player_data}
        selected_players = []
        for i in range(num_players):
            # Print current list of available players
            print('\nChoose 8 players from them id to start the tournament')
            print("List of available players:")
            for player_id, player in players_dict.items():
                print(f"[{player_id}]. "
                      f"{player['first_name']} || "
                      f"{player['last_name']} || "
                      f"{player['gender']} || "
                      f"{player['date_of_birth']}")

            # Get user input for player selection
            while True:
                try:
                    player_id = int(input(f"Enter ID of player {i + 1}: "))
                    if player_id not in players_dict:
                        raise ValueError
                    break
                except ValueError:
                    print("\nInvalid input. Please enter a valid player ID.")

            # Add selected player to list and remove from dictionary
            selected_player = players_dict.pop(player_id)
            selected_players.append(selected_player)

        return selected_players
    
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
