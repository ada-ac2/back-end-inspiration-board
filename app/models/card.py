from app import db
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer,db.ForeignKey("board.id"))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):
        card_dict = {}
        card_dict["id"] = self.id
        card_dict["message"] = self.message
        card_dict["likes_count"] = self.likes_count
        
        return card_dict
    
    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(
            message = card_data["message"],
            likes_count = card_data["likes_count"]
        )
        return new_card