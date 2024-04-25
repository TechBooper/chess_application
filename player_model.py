import json


class Player:
    def __init__(self, first_name, last_name, date_of_birth, chess_id):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "chess_id": self.chess_id,
        }


class PlayerModel:
    def __init__(self, file_path):
        self.file_path = file_path
        self.players = self.load_players()

    def load_players(self):
        """Loads players from the JSON file."""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_player_by_chess_id(self, chess_id):
        """Returns a player dictionary by chess_id or None if not found."""
        for player in self.players:
            if player["chess_id"] == chess_id:
                return player
        return None

    def save_players(self):
        """Saves the current list of players to the JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(self.players, file, indent=4)

    def add_player(self, player):
        """Adds a new player to the list and saves it."""
        self.players.append(player.to_dict())
        self.save_players()

    def get_all_players_sorted(self):
        with open(self.file_path, "r") as file:
            players = json.load(file)
        # Sort by first_name
        sorted_players = sorted(players, key=lambda x: x["first_name"])
        return sorted_players
