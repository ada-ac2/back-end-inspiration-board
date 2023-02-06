from operator import contains
from werkzeug.exceptions import HTTPException
from app.models.board import Board
from app.models.card import Card

BOARD_TITLE = "Favorite Quotes"
BOARD_OWNER = "Talia"

##############
# BOARD ROUTES #
##############

# CREATE
def test_create_one_board(client):
    # Act
    response = client.post("/boards", json={
        "title": BOARD_TITLE,
        "owner": BOARD_OWNER
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["title"] == BOARD_TITLE
    assert response_body["owner"] == BOARD_OWNER

    new_board = Board.query.get(1)

    assert new_board
    assert new_board.title == BOARD_TITLE
    assert new_board.owner == BOARD_OWNER

def test_create_board_must_contain_BOARD_TITLE(client):
    # Act
    response = client.post("/boards", json={
        "owner": BOARD_OWNER
    })
    response_body = response.get_json()

    # Assert
    assert "message" in response_body
    assert "Request body must include title" in response_body["message"]
    assert response.status_code == 400
    assert Board.query.all() == []

def test_create_board_must_contain_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": BOARD_TITLE,
    })
    response_body = response.get_json()

    # Assert
    assert "message" in response_body
    assert "Request body must include owner" in response_body["message"]
    assert response.status_code == 400
    assert Board.query.all() == []

# READ
def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, one_saved_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["board_id"] == 1
    assert response_body[0]["title"] == BOARD_TITLE
    assert response_body[0]["owner"] == BOARD_OWNER

##############
# CARD ROUTES #
##############

def test_get_all_cards_for_one_board():
    pass

def test_get_all_cards_no_cards():
    pass

def test_add_one_card():
    pass

def test_add_one_card_invalid_board_id():
    pass

def test_add_one_card_nonexistent_board_id():
    pass

def test_add_one_card_must_include_message():
    pass

def test_update_likes_on_card():
    pass

def test_delete_one_card(client, one_saved_card):
    # Act 
    response = client.delete("/boards/1/1")
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 200
    assert response["message"] == "Card #1 successfully deleted"
