import pytest
from app import create_app
from app import db
from app.models.board import Board
from app.models.card import Card
from flask.signals import request_finished

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

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
    
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
    new_board = Board(
        title = BOARD_TITLE_ONE,
        owner = BOARD_OWNER_ONE
    )
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def two_board(app):
    new_board = Board(
        title = BOARD_TITLE_TWO,
        owner = BOARD_OWNER_TWO
    )
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def three_board(app):
    new_board = Board(
        title = BOARD_TITLE_THREE,
        owner = BOARD_OWNER_THREE
    )
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def list_three_boards_without_cards(app):
    first_board = Board(
        title = BOARD_TITLE_ONE,
        owner = BOARD_OWNER_ONE,
        cards = []
    )
    second_board = Board(
        title = BOARD_TITLE_TWO,
        owner = BOARD_OWNER_TWO,
        cards = []
    )
    third_board = Board(
        title = BOARD_TITLE_THREE,
        owner = BOARD_OWNER_THREE,
        cards = []
    )
    db.session.add_all([first_board, second_board, third_board])
    db.session.commit()

@pytest.fixture
def list_three_boards_with_cards(app):
    first_card = Card(
        message = CARD_ONE_MESSAGE,
        likes_count = CARD_ONE_LIKES,
        board_id = CARD_ONE_BOARD)
    
    second_card = Card(
        message = CARD_TWO_MESSAGE,
        likes_count = CARD_TWO_LIKES,
        board_id = CARD_TWO_BOARD)

    third_card = Card(
        message = CARD_THREE_MESSAGE,
        likes_count = CARD_THREE_LIKES,
        board_id = CARD_THREE_BOARD)
    
    fourth_card = Card(
        message = CARD_FOUR_MESSAGE,
        likes_count = CARD_FOUR_LIKES,
        board_id = CARD_THREE_BOARD)    
    
    first_board = Board(
        title = BOARD_TITLE_ONE,
        owner = BOARD_OWNER_ONE,
        cards = [first_card, second_card]
    )
    second_board = Board(
        title = BOARD_TITLE_TWO,
        owner = BOARD_OWNER_TWO,
        cards = [third_card]
    )
    third_board = Board(
        title = BOARD_TITLE_THREE,
        owner = BOARD_OWNER_THREE,
        cards = [fourth_card]
    )

    db.session.add_all([first_board, second_board, third_board])
    db.session.commit()

@pytest.fixture
def one_board_with_one_card(app):
    first_card = Card(
        message = CARD_ONE_MESSAGE,
        likes_count = CARD_ONE_LIKES,
        board_id = CARD_ONE_BOARD)
    
    first_board = Board(
        title = BOARD_TITLE_ONE,
        owner = BOARD_OWNER_ONE,
        cards = [first_card]
    )
    db.session.add(first_board)
    db.session.commit()

@pytest.fixture()
def one_card(app):
    new_card = Card(
        message = CARD_ONE_MESSAGE,
        likes_count = CARD_ONE_LIKES,
        board_id = CARD_ONE_BOARD )
    db.session.add(new_card)
    db.session.commit()


@pytest.fixture()
def two_card(app):
    new_card = Card(
        message = CARD_TWO_MESSAGE,
        likes_count = CARD_TWO_LIKES,
        board_id = CARD_TWO_BOARD )
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture()
def three_card(app):
    new_card = Card(
        message = CARD_THREE_MESSAGE,
        likes_count = CARD_THREE_LIKES,
        board_id = CARD_THREE_BOARD )
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture()
def four_card(app):
    new_card = Card(
        message = CARD_FOUR_MESSAGE,
        likes_count = CARD_FOUR_LIKES,
        board_id = CARD_FOUR_BOARD )
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture()
def five_card(app):
    new_card = Card(
        message = CARD_FIVE_MESSAGE,
        likes_count = CARD_FIVE_LIKES,
        board_id = CARD_FIVE_BOARD )
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture()
def six_card(app):
    new_card = Card(
        message = CARD_SIX_MESSAGE,
        likes_count = CARD_SIX_LIKES,
        board_id = CARD_SIX_BOARD )
    db.session.add(new_card)
    db.session.commit()
