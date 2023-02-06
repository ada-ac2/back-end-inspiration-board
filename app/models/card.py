
from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    message = db.Column(db.String, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    display_status = db.Column(db.Boolean, default=True)
    # make sure of the name of the "backpopulates" in the board model
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"))
    board = db.relationship("Board", back_populates="cards")
    
    