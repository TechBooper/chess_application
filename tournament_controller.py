class TournamentController:
    def __init__(self, tournament_model, player_model, tournament_view):
        self.tournament_model = tournament_model
        self.player_model = player_model
        self.tournament_view = tournament_view

    def start_new_round(self):

        tournament_name = self.tournament_view.get_tournament_name()

        tournament = self.tournament_model.find_tournament_by_name(tournament_name)
        if tournament is None:
            self.tournament_view.display_error(
                f"Tournament '{tournament_name}' not found."
            )
            return

        if tournament.current_round >= tournament.total_rounds:
            self.tournament_view.display_error(
                f"Cannot start a new round. Tournament '{tournament_name}' has reached its total rounds limit."
            )
            return

        if len(tournament.players) < 2:
            self.tournament_view.display_error(
                "Not enough players to start a new round."
            )
            return

        success = self.tournament_model.generate_pairs_for_tournament(tournament_name)
        if success:
            self.tournament_view.display_success(
                f"New round started for tournament '{tournament_name}'."
            )
        else:
            self.tournament_view.display_error("Failed to start a new round.")

    def add_player_to_tournament(self):
        tournament_name = self.tournament_view.prompt_for_tournament_name()
        chess_id = self.tournament_view.get_player_chess_id()
        self.tournament_model.add_player_to_tournament(tournament_name, chess_id)

    def get_latest_round_pairs(self, tournament_name):
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament and tournament.rounds:
            latest_round = tournament.rounds[-1]
            return [
                (match.player1_chess_id, match.player2_chess_id)
                for match in latest_round.matches
            ]
        return []

    def display_latest_round_pairs(self, tournament_name):
        pairs = self.tournament_model.get_latest_round_pairs(tournament_name)
        if pairs:
            self.tournament_view.display_pairs(pairs)
        else:
            print(f"No pairs found for the latest round of '{tournament_name}'.")

    def add_tournament(self):
        tournament_data = {
            "name": input("Enter tournament name: "),
            "location": input("Enter location: "),
            "start_date": input("Enter start date (YYYY-MM-DD): "),
            "end_date": input("Enter end date (YYYY-MM-DD): "),
            "total_rounds": int(input("Enter number of rounds (default is 4): ") or 4),
            "current_round": 0,
            "players": [],
            "description": input("Enter tournament description (optional): ") or "",
            "rounds": [],
            "scores": {},
        }

        self.tournament_model.create_tournament(**tournament_data)
        print("Tournament created successfully!")

    def start_tournament(self, tournament_name):
        if self.tournament_model.start_tournament(tournament_name):
            self.display_first_round_matches(tournament_name)
        else:

            self.tournament_view.display_error(
                f"Failed to start tournament '{tournament_name}'."
            )

    def display_first_round_matches(self, tournament_name):
        pairs = self.tournament_model.get_latest_round_pairs(tournament_name)
        if pairs:
            self.tournament_view.display_pairs(pairs)
        else:
            self.tournament_view.display_error("No matches found for the first round.")

    def input_match_results(self):
        tournament_name = self.tournament_view.prompt_for_tournament_name()
        round_number = self.tournament_view.prompt_for_round_number()
        match_index = self.tournament_view.prompt_for_match_index()
        player1_score_input, player2_score_input = (
            self.tournament_view.prompt_for_scores()
        )

        if player1_score_input == "draw" and player2_score_input == "draw":
            player1_score = player2_score = 0.5
            player1_id, player2_id = self.tournament_model.get_player_ids_for_match(
                tournament_name, round_number, match_index
            )
            self.tournament_model.update_scores(tournament_name, player1_id, draw=True)
            self.tournament_model.update_scores(tournament_name, player2_id, draw=True)
            self.tournament_view.display_message(
                "The match ended in a draw. Everyone gets 0.5 points."
            )
        else:
            try:
                player1_score = float(player1_score_input)
                player2_score = float(player2_score_input)
                if player1_score > player2_score:
                    winner_id, loser_id = (
                        self.tournament_model.get_player_ids_for_match(
                            tournament_name, round_number, match_index
                        )
                    )
                    self.tournament_model.update_scores(
                        tournament_name, winner_id, win=True
                    )
                    self.tournament_model.update_scores(
                        tournament_name, loser_id, win=False
                    )
                    self.tournament_view.display_message(f"Winner is {winner_id}.")
                elif player2_score > player1_score:
                    loser_id, winner_id = (
                        self.tournament_model.get_player_ids_for_match(
                            tournament_name, round_number, match_index
                        )
                    )
                    self.tournament_model.update_scores(
                        tournament_name, winner_id, win=True
                    )
                    self.tournament_model.update_scores(
                        tournament_name, loser_id, win=False
                    )
                    self.tournament_view.display_message(f"Winner is {winner_id}.")
            except ValueError:
                self.tournament_view.display_error(
                    "Invalid input for scores. Please enter numeric values or 'draw'."
                )

        self.tournament_model.save_tournaments()
        self.tournament_view.display_success("Match result updated successfully.")

    def view_current_standings(self, tournament_name: str):
        standings = self.tournament_model.get_current_standings(tournament_name)
        self.tournament_view.display_standings(standings)

    def view_tournament_players(self):
        tournament_name = self.tournament_view.prompt_for_tournament_name()

        tournament = self.tournament_model.find_tournament_by_name(tournament_name)
        if tournament:

            self.tournament_view.display_tournament_players(
                tournament_name, tournament.players
            )
        else:
            self.tournament_view.display_error(
                f"Tournament '{tournament_name}' not found."
            )

    def list_all_tournaments(self):
        tournaments = self.tournament_model.get_all_tournaments()
        self.tournament_view.display_all_tournaments(tournaments)

    def view_tournament_details(self, tournament_name):
        tournament = self.tournament_model.find_tournament_by_name(tournament_name)
        if not tournament:
            self.tournament_view.display_error(
                f"Tournament '{tournament_name}' not found."
            )
            return

        rounds = tournament.rounds
        if rounds:
            self.tournament_view.display_tournament_rounds(tournament_name, rounds)
        else:
            self.tournament_view.display_message("No rounds found for this tournament.")

    def advance_to_next_round(self):
        tournament_name = self.tournament_view.prompt_for_tournament_name()

        success = self.tournament_model.generate_pairs_for_tournament(tournament_name)

        if success:
            self.tournament_view.display_success(
                f"Advanced to round {self.tournament_model.find_tournament_by_name(tournament_name).current_round}."
            )
        else:
            self.tournament_view.display_error(
                "Failed to advance to the next round or generate new pairs."
            )
