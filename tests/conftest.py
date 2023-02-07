import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.board import Board
from app.models.card import Card

OWNER = "Nad"

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app(test_config=True)

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_board(app):
    new_board = Board(title="My test board", owner=OWNER)

    db.session.add(new_board)
    db.session.commit()
    db.session.refresh(new_board,["id"])

def second_board(app):
    new_board = Board(title="My test board2", owner="Nad")

    db.session.add(new_board)
    db.session.commit()
    db.session.refresh(new_board,["id"])

@pytest.fixture
def one_card_to_board(app,one_board):
    new_card = Card(message="Good message",board_id=1)

    db.session.add(new_card)
    db.session.commit()
    db.session.refresh(new_card,["id"])


