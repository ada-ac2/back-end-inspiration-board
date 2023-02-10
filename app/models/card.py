from app import db
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    board_id = db.Column(db.Integer,db.ForeignKey("board.id"))
    board = db.relationship("Board", back_populates="cards")

    def to_dict(self):

            return {
            "id" : self.id,
            "message" : self.message,
            "likes_count" : self.likes_count,
            "board_id" : self.board_id,
            "board_title" : self.board.title
            
        }
    
    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(
            message = card_data["message"]
        )
        return new_card