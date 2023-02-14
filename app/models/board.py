from app import db

class Board(db.Model):
    board_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        board_dict = {}
        board_dict["board_id"] = self.board_id
        board_dict["title"] = self.title
        board_dict["owner"] = self.owner
        cards_list = []
        for card in self.cards:
            cards_list.append(card.to_dict())
        board_dict["cards"] = cards_list
        #board_dict["cards"] = [card.to_dict() for card in self.cards]
        return board_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title=board_data["title"],
                        owner=board_data["owner"])
        return new_board

                    