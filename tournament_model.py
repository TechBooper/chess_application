from datetime import datetime
import json
import os
from tournament import Tournament
from tournament import Round


class TournamentModel:
    def __init__(self, file_path, player_model):
        self.file_path = file_path
        self.tournaments = []
        self.load_tournaments()
        self.player_model = player_model

    def find_tournament_by_name(self, tournament_name):
        for tournament in self.tournaments:
            if tournament.name == tournament_name:
                return tournament
        return None

    def add_player(self, chess_id):
        if not hasattr(self, "players"):
            self.players = []
        self.players.append(chess_id)

    def get_all_tournaments(self):
        return self.tournaments

    def get_latest_round_pairs(self, tournament_name):
        tournament = self.find_tournament_by_name(tournament_name)
        if tournament and tournament.rounds:
            latest_round = tournament.rounds[-1]
            return [(match[0][0], match[1][0]) for match in latest_round.matches]
        return []

    def ensure_data_directory_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    def load_tournaments(self):
        self.ensure_data_directory_exists()
        try:
            with open(self.file_path, "r") as file:
                tournaments_data = json.load(file)
                self.tournaments = [
                    Tournament.from_dict(t_data) for t_data in tournaments_data
                ]
        except FileNotFoundError:
            self.tournaments = []
            self.save_tournaments()
        except json.JSONDecodeError:
            print("Error decoding JSON from the tournament file.")
            self.tournaments = []
            self.save_tournaments()

    def add_player_to_tournament(self, tournament_name, chess_id):
        found = False
        for tournament in self.tournaments:
            if tournament.name == tournament_name:
                found = True
                if chess_id not in tournament.players:
                    tournament.players.append(chess_id)

                    if tournament.scores is None:
                        tournament.scores = {}
                    tournament.scores[chess_id] = tournament.scores.get(chess_id, 0)
                    self.save_tournaments()
                    print(f"Player {chess_id} added to tournament '{tournament_name}'.")
                    return True
                else:
                    print(
                        f"Player {chess_id} is already in tournament '{tournament_name}'."
                    )
                    return False
        if not found:
            print(f"Tournament '{tournament_name}' not found.")
            return False

    def generate_pairs_for_tournament(self, tournament_name):
        tournament = self.find_tournament_by_name(tournament_name)
        if not tournament:
            return False

        if tournament.current_round >= tournament.total_rounds:
            print("All rounds have been completed.")
            return False

        # Set end time for the previous round
        if tournament.current_round > 0:
            previous_round = tournament.rounds[tournament.current_round - 1]
            if previous_round.end_time is None:
                previous_round.end_time = datetime.now()

        players = tournament.players
        if len(players) % 2 != 0:
            raise ValueError("Number of players is not even.")

        past_matchups = set()
        for round_ in tournament.rounds:
            for match in round_.matches:
                past_matchups.add(frozenset([match[0][0], match[1][0]]))

        sorted_players = sorted(
            players, key=lambda x: tournament.scores.get(x, 0), reverse=True
        )
        new_pairs = []

        # Attempt to pair players without repeating matchups, if all matchups are exhausted, pair by scores
        paired = set()
        for i in range(len(sorted_players)):
            if sorted_players[i] in paired:
                continue
            for j in range(i + 1, len(sorted_players)):
                if sorted_players[j] in paired:
                    continue
                if frozenset(
                    [sorted_players[i], sorted_players[j]]
                ) not in past_matchups or len(past_matchups) == (
                    len(players) * (len(players) - 1) / 2
                ):
                    new_pairs.append((sorted_players[i], sorted_players[j]))
                    paired.add(sorted_players[i])
                    paired.add(sorted_players[j])
                    break

        # Create matches for the new round
        matches = [([p1, 0], [p2, 0]) for p1, p2 in new_pairs]
        new_round = Round(
            round_number=len(tournament.rounds) + 1,
            matches=matches,
            start_time=datetime.now(),
            end_time=None,
        )
        tournament.rounds.append(new_round)
        tournament.current_round += 1

        self.save_tournaments()
        print(
            f"New round {new_round.round_number} started with matches at {new_round.start_time}."
        )
        return True

    def start_tournament(self, tournament_name):
        tournament = self.find_tournament_by_name(tournament_name)
        if not tournament:
            print("Tournament not found.")
            return False

        success = self.generate_pairs_for_tournament(tournament_name)
        if not success:
            print(f"Failed to generate pairs and start tournament '{tournament_name}'.")
            return False

        self.save_tournaments()

        print(
            f"Tournament '{tournament_name}' successfully started with the first round of matches."
        )
        return True

    def save_tournaments(self):
        try:
            serialized_tournaments = [
                tournament.to_dict() for tournament in self.tournaments
            ]
            with open(self.file_path, "w") as file:
                json.dump(serialized_tournaments, file, indent=4)
        except Exception as e:
            print(f"Failed to save tournaments: {e}")

    def create_tournament(self, **tournament_data):

        scores = tournament_data.get(
            "scores", {player: 0 for player in tournament_data.get("players", [])}
        )
        initial_rounds = tournament_data.get("rounds", [])
        standings = tournament_data.get("standings", [])

        new_tournament = Tournament(
            name=tournament_data["name"],
            location=tournament_data["location"],
            start_date=tournament_data["start_date"],
            end_date=tournament_data["end_date"],
            total_rounds=tournament_data["total_rounds"],
            current_round=tournament_data["current_round"],
            players=tournament_data.get("players", []),
            description=tournament_data.get("description", ""),
            rounds=initial_rounds,
            scores=scores,
            standings=standings,
        )

        self.tournaments.append(new_tournament)
        self.save_tournaments()

    def get_player_ids_for_match(self, tournament_name, round_number, match_index):
        tournament = self.find_tournament_by_name(tournament_name)
        if not tournament:
            raise ValueError("Tournament not found.")

        round_ = tournament.rounds[round_number - 1]
        match = round_.matches[match_index]
        return match[0][0], match[1][0]

    def update_scores(
        self, tournament_name, round_number, match_index, player1_score, player2_score
    ):
        tournament = self.find_tournament_by_name(tournament_name)
        if not tournament:
            print(f"Tournament {tournament_name} not found.")
            return False

        try:
            match = tournament.rounds[round_number - 1].matches[match_index]
            player1_id, player2_id = match[0][0], match[1][0]

            match[0][1] = player1_score
            match[1][1] = player2_score

            tournament.scores[player1_id] = (
                tournament.scores.get(player1_id, 0) + player1_score
            )
            tournament.scores[player2_id] = (
                tournament.scores.get(player2_id, 0) + player2_score
            )

            if all(
                m[0][1] is not None and m[1][1] is not None
                for m in tournament.rounds[round_number - 1].matches
            ):
                tournament.rounds[round_number - 1].end_time = datetime.now()

            self.save_tournaments()
            return True
        except IndexError:
            print("Invalid round number or match index.")
            return False

    def get_current_standings(self, tournament_name: str):
        tournament = self.find_tournament_by_name(tournament_name)
        if not tournament:
            raise ValueError(f"Tournament '{tournament_name}' not found.")

        sorted_scores = sorted(
            tournament.scores.items(), key=lambda item: item[1], reverse=True
        )

        self.save_tournaments()
        return sorted_scores
