import pytest
from app import create_app, db
<<<<<<< HEAD
from app.models import Board, Card

BOARD_TITLE = "Favorite Quotes"
BOARD_OWNER = "Talia"

CARD_MESSAGE = "Hello!"
=======
from app.models.board import Board

BOARD_TITLE = "Favorite Quotes"
BOARD_OWNER = "Talia"
>>>>>>> 53526e89163453fd91d892e706aa6c31332bb514

@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

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
def one_saved_board(app):
    new_board = Board(
        title=BOARD_TITLE,
        owner=BOARD_OWNER
    )
    db.session.add(new_board)
    db.session.commit()
<<<<<<< HEAD

@pytest.fixture
def one_saved_card(app, one_saved_board):
    new_card = Card(
        message=CARD_MESSAGE
    )
    db.session.add(new_card)
    db.session.commit()
=======
>>>>>>> 53526e89163453fd91d892e706aa6c31332bb514
