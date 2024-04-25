class TournamentView:

    def prompt_for_tournament_name(self):
        """Prompt the user for the tournament name and return it."""
        return input("Enter the name of the tournament: ").strip()

    def get_player_chess_id(self):
        """Prompt the user for a player's chess ID and return it."""
        return input("Enter the player's Chess ID: ").strip()

    def get_round_number(self):
        """Prompt the user for the round number and return it."""
        try:
            return int(input("Enter the round number: ").strip())
        except ValueError:
            print("Invalid input. Please enter a valid round number.")
            return None

    def get_winner_chess_id(self):
        """Prompt the user for the winner's chess ID and return it."""
        return input("Enter the winner's chess ID (or 'draw' for a tie): ").strip()

    def prompt_for_scores(self):
        print("Enter the scores for the match or type 'draw' for a draw.")
        player1_score = input("Player 1 score (or 'draw'): ")
        player2_score = input("Player 2 score (or 'draw'): ")
        return player1_score, player2_score

    def prompt_for_round_number(self):
        return int(input("Enter the round number: "))

    def display_success(self, message):
        print(f"Success: {message}")

    def display_message(self, message):
        print(f"Success: {message}")

    def prompt_for_match_index(self):
        """Prompt the user for the match index and return it."""
        try:
            return int(input("Enter the match index (starting from 0): ").strip())
        except ValueError:
            print("Invalid input. Please enter a valid match index.")
            return None

    def get_winner(self):
        return input("Enter the winner (Player 1 ID, Player 2 ID, or 'draw'): ")

    def get_new_tournament_data(self):
        print("\nCreate a New Tournament")
        name = input("Tournament name: ")
        location = input("Location: ")
        start_date = input("Start date (YYYY-MM-DD): ")
        end_date = input("End date (YYYY-MM-DD): ")
        rounds = input("Number of rounds (default is 4): ") or 4
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "rounds": int(rounds),
        }

    def display_matches(self, matches):
        print("\nMatches:")
        for match_id, match_data in matches.items():
            print(
                f"{match_id}: {match_data['player1'].name} vs {match_data['player2'].name}"
            )

    def display_tournament_players(self, tournament_name, players):
        if players:
            print(f"\nPlayers in Tournament '{tournament_name}':")
            for player in players:
                print(f"- {player}")
        else:
            print(f"No players found for tournament '{tournament_name}'.")

    def display_rounds(self, rounds):
        print("\nRounds:")
        for round_number, round_data in rounds.items():
            print(f"Round {round_number}:")
            for match_id, match_data in round_data["matches"].items():
                print(
                    f"{match_id}: {match_data['player1'].name} vs {match_data['player2'].name}"
                )

    def display_standings(self, standings):
        print("\nStandings:")
        if standings:
            for player_id, score in standings:
                print(f"{player_id}: {score} points")
        else:
            print("No standings available.")

    def display_pairs(self, pairs):
        print("\nPairs:")
        for pair in pairs:
            player1, player2 = pair
            print(f"{player1} vs {player2}")

    def display_all_tournaments(self, tournaments):
        if tournaments:
            print("\nList of All Tournaments:")
            for tournament in tournaments:
                print(
                    f"- {tournament.name}at{tournament.location}from{tournament.start_date}to{tournament.end_date}"
                )
        else:
            print("No tournaments available.")

    def display_tournament_rounds(self, tournament_name, rounds):
        print(f"\nTournament '{tournament_name}' Rounds and Matches:")
        for round_ in rounds:
            print(f"Round {round_.round_number}:")
            for match in round_.matches:
                player1, player2 = match[0][0], match[1][0]
                score1, score2 = match[0][1], match[1][1]
                print(f"  Match: {player1} ({score1}) vs {player2} ({score2})")

    def display_error(self, message):
        print(message)
