import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card

BOARD_TITLE = "Testing Board One"
BOARD_CREATOR = "InspoBoardCheerup"

CARD_MESSAGE = "Don't put off tomorrow what you can do today!"

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
def one_board(app):
    new_board = Board(title=BOARD_TITLE,
                creator=BOARD_CREATOR)
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def two_saved_boards(app):
    # Arrange
    b1 = Board(title=BOARD_TITLE,
                creator=BOARD_CREATOR)
    b2 = Board(title="Testing Board Two",
                creator="InspoBoardCheerUp New")
    

    db.session.add_all([b1, b2])
    db.session.commit()

@pytest.fixture
def one_card(app):
    new_card = Card(
        message=CARD_MESSAGE
        )
    db.session.add(new_card)
    db.session.commit()


@pytest.fixture
def one_posted_card(app, client, one_board, one_card):
    response = client.post("boards/1/cards", json={
        "message": CARD_MESSAGE
    })