from .player import Player


class PlayerController:
    def __init__(self, player_model, player_view):
        self.player_model = player_model
        self.player_view = player_view

    def validate_player_data(self, player_data):
        essential_fields = ["first_name", "last_name", "date_of_birth", "chess_id"]
        return all(
            field in player_data and player_data[field] for field in essential_fields
        )

    def list_players_sorted(self):
        players_info = self.player_model.get_all_players_sorted()
        self.player_view.display_players(players_info)

    def add_player(self):
        player_data = self.player_view.get_new_player_data()
        new_player = Player(**player_data)
        self.player_model.add_player(new_player)
        print(f"Added new player: {new_player.first_name} {new_player.last_name}")

    def get_player_by_name(self, name):
        return self.player_model.get_player_by_name(name)

    def get_all_players(self):
        return self.player_model.get_all_players()
