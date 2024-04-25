class PlayerView:
    def get_new_player_data(self):
        print("Please enter the new player's details:")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        date_of_birth = input("Date of Birth (YYYY-MM-DD): ")
        chess_id = input("Chess ID: ")

        return {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": date_of_birth,
            "chess_id": chess_id,
        }

    def display_player_details(self, player):
        print("\nPlayer Details:")
        print(f"Last Name: {player.last_name}")
        print(f"First Name: {player.first_name}")
        print(f"Date of Birth: {player.date_of_birth}")
        print(f"Chess ID: {player.chess_id}")

    def display_players(self, players_info):
        print("\nList of Players (Sorted by First Name):")
        for player in players_info:
            print(f"Name: {player['first_name']}, Chess ID: {player['chess_id']}")
