import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card

BOARD_TITLE_ONE = "First Board"
BOARD_TITLE_TWO = "Second Board"
BOARD_TITLE_THREE = "Third Board"

BOARD_OWNER_ONE = "First Owner"
BOARD_OWNER_TWO = "Second Owner"
BOARD_OWNER_THREE = "Third Owner"

CARD_ONE_MESSAGE = "Pickles are priceless"
CARD_TWO_MESSAGE = "Some Days are Fancy Free"
CARD_THREE_MESSAGE = "I like my dancing pants"
CARD_FOUR_MESSAGE = "Days are good Days are Bad Its okay to sometimes be sad"
CARD_FIVE_MESSAGE = "Its a good day"
CARD_SIX_MESSAGE = "I GOT THIS"

CARD_ONE_LIKES = 0
CARD_TWO_LIKES = 0
CARD_THREE_LIKES = 1
CARD_FOUR_LIKES = 2
CARD_FIVE_LIKES = 3
CARD_SIX_LIKES = 0

CARD_ONE_BOARD = 3
CARD_TWO_BOARD = 2
CARD_THREE_BOARD = 1
CARD_FOUR_BOARD= 3
CARD_FIVE_BOARD = 2
CARD_SIX_BOARD = 3




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
    new_board = Board()
