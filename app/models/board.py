from app import db

class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    owner = db.Column(db.String(120), nullable=False)
    cards = db.relationship("Card", back_populates="board")