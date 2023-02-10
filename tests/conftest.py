import pytest
from app import create_app, db
from app.models.board import Board
from app.models.card import Card
from flask.signals import request_finished
#need to reinstall requirements.txt for the blinker

BOARD_TITLE = "Favorite Quotes"
BOARD_OWNER = "Talia"

CARD_MESSAGE = "Hello!"

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
def one_saved_board(app):
    new_board = Board(
        title=BOARD_TITLE,
        owner=BOARD_OWNER
    )
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_saved_card(app, one_saved_board):
    new_card = Card(
        message=CARD_MESSAGE
    )
    db.session.add(new_card)
    db.session.commit()

#--------------------------------------------
# for nesting routes
#--------------------------------------------
@pytest.fixture
def two_saved_boards(app):
    board_1 = Board(
        title= "Trips",
        owner="Tom"
    )
    board_2 = Board(
        title= "Holidays",
        owner= "Jun" 
    )
    db.session.add(board_1)
    db.session.add(board_2)
    db.session.commit()


@pytest.fixture
def add_one_card_to_id_2 (app, client, two_saved_boards):
    #Arrange
    response = client.post("/boards/2/cards", json = {
        "board_id": 2,
        "message": CARD_MESSAGE,
        "likes_count": 2
    })
    