
from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    status = db.Column(db.Boolean, default=True)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    board = db.relationship("Board", back_populates="cards")
    
    @classmethod
    def from_dict(cls, card_dict, board_id):
        return Card(
            message=card_dict["message"],
            board_id=board_id,
        )

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "likes_count": self.likes_count,
            "display_status": self.display_status,
            "board_id": self.board_id
        }