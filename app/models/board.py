from app import db


class Board(db.Model):
    # primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # other columns
    title = db.Column(db.String(45), nullable=False)
    owner = db.Column(db.String(45), nullable=False)
    status = db.Column(db.Boolean, default=True)
    # foreign key associate to Card table
    cards = db.relationship("Card")

    def to_dict(self):
        board_as_dict = dict()
        board_as_dict["id"] = self.id
        board_as_dict["title"] = self.title
        board_as_dict["owner"] = self.owner
        board_as_dict["status"] = self.status
        return board_as_dict
    
    @classmethod
    def from_dict(cla, board_data):
        new_board = Board(
            title=board_data["title"],
            owner=board_data["owner"],
        )
        return new_board
