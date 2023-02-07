from app import db
# needed to establish one-to-many relationship
from sqlalchemy.orm import relationship

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String(40), nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey("board.board_id"))
    board = db.relationship("Board", back_populates="cards")
    

    def to_dict(self):
        card_dict = {
            "card_id": self.card_id,
            "board_id": self.board_id,
            "message": self.message,
            "likes_count": self.likes_count
        }
<<<<<<< HEAD
        return card_dict

=======
        
        return card_dict


>>>>>>> b33461c3a3f7305938657545733d86e16ca91b54
    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(
                    board_id = card_data["board_id"],
                    message = card_data["message"],
                    likes_count = card_data["likes_count"]
                    )
        return new_card