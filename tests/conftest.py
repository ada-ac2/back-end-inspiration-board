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
def two_saved_boards(app):
    # Arrange
    b1 = Board(title="Testing Board One",
                creator="InspoBoardCheerup")
    b2 = Board(title="Testing Board Two",
                creator="InspoBoardCheerUp New")
    

    db.session.add_all([b1, b2])
    db.session.commit()