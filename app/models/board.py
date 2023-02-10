from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    creator = db.Column(db.String)
    cards = db.relationship("Card",back_populates="board")

    def to_dict(self):
        board_dict = {}
        board_dict["id"] = self.id
        board_dict["title"] = self.title
        board_dict["creator"] = self.creator
        cards = []
        for card in self.cards:
            cards.append(card.id)
        board_dict["cards"] = cards
        return board_dict
    
    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"],
                    creator=board_data["creator"],                                   
                    )
        return new_board


