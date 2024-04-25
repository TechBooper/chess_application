from datetime import datetime


class Round:
    def __init__(self, round_number, matches=None, start_time=None, end_time=None):
        self.round_number = round_number
        self.matches = matches if matches is not None else []
        self.start_time = (
            start_time
            if isinstance(start_time, datetime)
            else (datetime.fromisoformat(start_time) if start_time else None)
        )
        self.end_time = (
            end_time
            if isinstance(end_time, datetime)
            else (datetime.fromisoformat(end_time) if end_time else None)
        )

    def add_match(self, player1_chess_id, player2_chess_id):
        self.matches.append(([player1_chess_id, 0], [player2_chess_id, 0]))

    @classmethod
    def from_dict(cls, data):
        return cls(
            round_number=data["round_number"],
            matches=data.get("matches", []),
            start_time=data["start_time"],
            end_time=data["end_time"],
        )

    def to_dict(self):
        return {
            "round_number": self.round_number,
            "matches": [[list(match[0]), list(match[1])] for match in self.matches],
            "start_time": (
                self.start_time.isoformat()
                if isinstance(self.start_time, datetime)
                else self.start_time
            ),
            "end_time": (
                self.end_time.isoformat()
                if isinstance(self.end_time, datetime)
                else self.end_time
            ),
        }


class Tournament:
    def __init__(
        self,
        name,
        location,
        start_date,
        end_date,
        total_rounds,
        current_round,
        players=None,
        description="",
        rounds=None,
        scores=None,
        standings=None,
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.total_rounds = total_rounds
        self.current_round = current_round
        self.players = players if players is not None else []
        self.description = description
        self.rounds = rounds if rounds is not None else []
        self.scores = scores if scores is not None else {}
        self.standings = standings if standings is not None else []

    @classmethod
    def from_dict(cls, data):
        # Assuming 'data' is a dictionary with all necessary keys to initialize a Tournament instance
        return cls(
            name=data["name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            total_rounds=data["total_rounds"],
            current_round=data["current_round"],
            players=data.get("players", []),
            description=data.get("description", ""),
            rounds=[Round.from_dict(r_data) for r_data in data.get("rounds", [])],
            scores=data.get("scores", {}),
            standings=data.get("standings", []),
        )

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_rounds": self.total_rounds,
            "current_round": self.current_round,
            "players": self.players,
            "rounds": [
                round.to_dict() for round in self.rounds
            ],
            "scores": self.scores,
            "standings": self.standings,
        }

    def get_match_by_index_in_round(self, round_index, match_index):
        round_data = self.rounds[round_index]

        if "matches" in round_data:
            return round_data["matches"][match_index]

        raise ValueError(f"No 'matches' data found in round number: {round_index + 1}")

    def is_round_complete(self, round_number):
        if round_number > len(self.rounds) or round_number < 1:
            print("Invalid round number.")
            return False
        current_round = self.rounds[round_number - 1]
        return all(match.winner is not None for match in current_round.matches)

    def update_match_result(
        self, round_number, match_index, player1_score, player2_score
    ):
        # Validate round_number and match_index
        if round_number > len(self.rounds) or round_number < 1:
            print(f"Invalid round number: {round_number}.")
            return
        if match_index >= len(self.rounds[round_number - 1].matches) or match_index < 0:
            print(f"Invalid match index: {match_index}.")
            return

        # Update the specified match with new scores
        round_ = self.rounds[round_number - 1]
        match = round_.matches[match_index]
        updated_match = ([match[0][0], player1_score], [match[1][0], player2_score])
        round_.matches[match_index] = updated_match

        # Save changes to the tournament
        self.save_tournaments()  # Assumes implementation of persistence

    def calculate_standings(self):
        player_scores = {player: 0 for player in self.players}
        for round_ in self.rounds:
            for match in round_.matches:
                player1_id, player1_score = match[0]
                player2_id, player2_score = match[1]
                if player1_score > player2_score:
                    player_scores[player1_id] += 1
                elif player1_score < player2_score:
                    player_scores[player2_id] += 1
                else:
                    player_scores[player1_id] += 0.5
                    player_scores[player2_id] += 0.5
        # Sort and return the standings
        sorted_scores = sorted(
            player_scores.items(), key=lambda item: item[1], reverse=True
        )
        return sorted_scores

    def add_player(self, chess_id):
        # This method assumes 'players' is a list attribute of the Tournament class
        if not hasattr(self, "players"):
            self.players = []  # Initialize if not already present
        self.players.append(chess_id)

    def update_scores(self):
        # Reset scores to 0 for all players before recalculating
        self.scores = {player: 0 for player in self.players}

        # Iterate through each round and each match (now as tuples)
        for round_ in self.rounds:
            for match in round_.matches:
                # Unpack the player IDs and scores from the match tuple
                player1, player2 = match  # match is a tuple of two lists
                player1_id, player1_score = player1
                player2_id, player2_score = player2

                # Update scores based on match outcome
                self.scores[player1_id] += player1_score
                self.scores[player2_id] += player2_score

    def get_player_names(self):
        return self.players

    def remove_player(self, player):
        self.players.remove(player)
