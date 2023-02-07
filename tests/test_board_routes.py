from operator import contains
from app.models.board import Board
from app.models.card import Card


def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_two_saved_board(client, add_two_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == "title_1"
    assert response_body[0]["owner"] == "ownder_1"
    assert response_body[1]["title"] == "title_2"
    assert response_body[1]["owner"] == "ownder_2"