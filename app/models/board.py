from app import db
# needed to establish one-to-many relationship
from sqlalchemy.orm import relationship


class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner,
            "cards": [card for card in self.cards]
        }

    @classmethod
    def from_dict(cls, request_data):
        new_board = Board(
            title = request_data["title"],
            owner = request_data["owner"]
        )
        return new_board