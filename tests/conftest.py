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
def add_two_boards(app):
    board_1 = Board(title="title_1", owner="ownder_1")
    board_2 = Board(title="title_2", owner="ownder_2")
    db.session.add_all([board_1, board_2])
    db.session.commit

    return [board_1, board_2]
