class Player:
    def __init__(self, first_name, last_name, date_of_birth, chess_id, score):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.chess_id = chess_id
        self.score = score

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth,
            "chess_id": self.chess_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            first_name=data["first_name"],
            last_name=data["last_name"],
            date_of_birth=data["date_of_birth"],
            chess_id=data["chess_id"],
            score=data.get("score", 0),  # Handle score with a default value
        )

    def __repr__(self):
        return f"{self.first_name} {self.last_name} (Score: {self.score})"
