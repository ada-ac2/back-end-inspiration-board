from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    owner = db.Column(db.String(120), nullable=False)
    cards = db.relationship("Card", back_populates="board")

    def to_dict(self):
        board_as_dict = {}
        board_as_dict["id"] = self.id
        board_as_dict["title"] = self.title
        board_as_dict["owner"] = self.owner

        card_list = []
        for card in self.cards:
            card_list.append(card.message)
        board_as_dict["cards"] = card_list

        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        new_board = Board(title = board_data["title"],
                        owner = board_data["owner"],
                        )
        return new_board