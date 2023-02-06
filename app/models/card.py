from app import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    message = db.Column(db.String, nullable=False)
    likes = db.Column(db.Integer,nullable=False, default=0)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    board = db.relationship("Board", back_populates="cards")