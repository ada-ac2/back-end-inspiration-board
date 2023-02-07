import pytest
from app import create_app
from app import db
from app.models.board import Board


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
def saved_two_boards(app):
    board1 = Board(title="Hello,world!",
                owner="Nad",
                cards = []
                )

    board2 = Board(title="Hello,friend!",
                owner="Jennifer",
                cards = []
                )

    db.session.add_all([board1, board2])
    db.session.commit()
    db.session.refresh(board1, ["id"])
    db.session.refresh(board2, ["id"])