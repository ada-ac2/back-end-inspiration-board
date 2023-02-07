from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer,nullable=False, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        card_dict = {
            "id": self.id,
            "message": self.message,
            "likes": self.likes
        }
        if self.board:
            card_dict["board"] = {
                "id": self.board.id,
                "title": self.board.title,
                "owner": self.board.owner
            }

        return card_dict