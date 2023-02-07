import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card


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
def add_two_boards(app):
    board_1 = Board(title="title_1", owner="owner_1")
    board_2 = Board(title="title_2", owner="owner_2")
    db.session.add_all([board_1, board_2])
    db.session.commit

    return [board_1, board_2]

@pytest.fixture
def add_one_board(app):
    board_3 = Board(title="title_3", owner="owner_3")
    db.session.add(board_3)
    db.session.commit

    return board_3

@pytest.fixture
def add_two_cards_to_board_one(app, add_two_boards):
    card_1 = Card(message="first sample card for board 1", board_id=1)
    card_2 = Card(message="second sample card for board 1", board_id=1)
    db.session.add_all([card_1, card_2])
    db.session.commit 

    return [card_1, card_2]

@pytest.fixture
def add_one_card_to_board_one_and_one_card_to_board_two(app, add_two_boards):
    card_1 = Card(message="first sample card for board 1", board_id=1)
    card_2 = Card(message="first sample card for board 2", board_id=2)
    db.session.add_all([card_1, card_2])
    db.session.commit 

    return [card_1, card_2]

@pytest.fixture
def archive_one_card(app, add_two_cards_to_board_one):
    card_one = Card.query.get(1)
    card_one.status = False
    db.session.commit