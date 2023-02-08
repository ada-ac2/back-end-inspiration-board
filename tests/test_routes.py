from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
from app.models.card import Card
import pytest

BOARD_TITLE = "Testing Board One"
BOARD_CREATOR = "InspoBoardCheerup"

CARD_MESSAGE = "Don't put off tomorrow what you can do today!"

##### tests on validate_model
def test_validate_model(two_saved_boards):
    # Act
    result_board = validate_model(Board, 2)

    # Assert
    assert result_board.id == 2
    assert result_board.title == "Testing Board Two"
    assert result_board.creator == "InspoBoardCheerUp New"
    

def test_validate_model_missing_id(two_saved_boards):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_board = validate_model(Board, "3")

def test_validate_model_invalid_id(two_saved_boards):
    # Act & Assert
    # Calling `validate_book` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_board = validate_model(Board, "helloworld")

##### tests on POST one board
def test_create_one_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "like the dog",
        "creator": "Zoro"       
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["title"] == "like the dog"
    assert response_body["creator"] == "Zoro" 
    assert response_body["cards"] == []

def test_create_one_board_missing_keyword_title(client):
    # Act
    response = client.post("/boards", json={
        "creator": "Zoro"       
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A title must be included to add a board"

def test_create_one_board_empty_title(client):
    # Act
    response = client.post("/boards", json={
        "title": "",
        "creator": "Zoro"       
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A title must be included to add a board"

def test_create_one_board_missing_keyword_creator(client):
    # Act
    response = client.post("/boards", json={
        "title": "like the dog"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A creator must be included to add a board"

def test_create_one_board_empty_creator(client):
    # Act
    response = client.post("/boards", json={
        "title": "like the dog",
        "creator": ""  
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A creator must be included to add a board"

##### tests on GET all boards
def test_get_boards_empty_db_returns_empty_list(client):
    # Act
    response = client.get("/boards")

    # Assert 
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_boards_optional_query_returns_seeded_boards(client, two_saved_boards):
    response = client.get("/boards")

    assert response.status_code == 200
    board_list = response.get_json()
    assert len(board_list) == 2
    assert board_list[0]["id"] == 1
    assert board_list[0]["title"] == "Testing Board One"
    assert board_list[0]["creator"] == "InspoBoardCheerup"
    
    assert board_list[1]["id"] == 2
    assert board_list[1]["title"] == "Testing Board Two"
    assert board_list[1]["creator"] == "InspoBoardCheerUp New"
    

def test_get_one_board_with_title_param_asc_sort(client, two_saved_boards):
    response = client.get("/boards?title=Testing Board One&sort=asc") 

    assert response.status_code == 200
    board_list = response.get_json()
    assert len(board_list) == 1
    assert board_list[0]["id"] == 1
    assert board_list[0]["title"] == "Testing Board One"
    assert board_list[0]["creator"] == "InspoBoardCheerup"

def test_get_one_board_with_title_param_desc_sort(client, two_saved_boards):
    response = client.get("/boards?title=Testing Board Two&sort=desc") 

    assert response.status_code == 200
    board_list = response.get_json()
    assert len(board_list) == 1
    
    assert board_list[0]["id"] == 2
    assert board_list[0]["title"] == "Testing Board Two"
    assert board_list[0]["creator"] == "InspoBoardCheerUp New"

##### tests on GET one board
def test_get_one_board_by_id(client, two_saved_boards):
    response = client.get("/boards/2") 

    assert response.status_code == 200
    board_list = response.get_json()

    assert len(board_list) == 4    
    assert board_list["id"] == 2
    assert board_list["title"] == "Testing Board Two"
    assert board_list["creator"] == "InspoBoardCheerUp New"

def test_get_board_with_id_empty_db_returns_404(client):
    # Act
    response = client.get("/boards/100")

    # Assert 
    assert response.status_code == 404
    assert response.get_json() == {"message":f"Board 100 not found"}

##### tests on DELETE one board

def test_delete_one_board(client, two_saved_boards):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 200
    assert response_body == "Board #1 successfully deleted"


def test_does_not_delete_board_with_invalid_id(client, two_saved_boards):
    # Act
    response = client.delete("/boards/helloworld")

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"message": f"Board helloworld invalid"}

def test_does_not_delete_board_with_nonexistent_id(client, two_saved_boards):
    # Act
    response = client.delete("/boards/100")

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {"message":f"Board 100 not found"}

##### tests on UPDATE one board
def test_does_not_update_one_board_with_invalid_id(client, two_saved_boards):
    # Act
    response = client.put("/boards/helloworld", json={
        "title": "Walk the Cat",
        "creator": "Tabby"
    })

    # Assert
    assert response.status_code == 400
    assert response.get_json() == {"message":f"Board helloworld invalid"}

def test_does_not_update_one_board_with_nonexistent_id(client, two_saved_boards):
    # Act
    response = client.put("/boards/300", json={
        "title": "Read one Book every Month",
        "creator": "Nandini"
    })

    # Assert
    assert response.status_code == 404
    assert response.get_json() == {"message":f"Board 300 not found"}

def test_update_one_board(client, two_saved_boards):
    # Act
    response = client.put("/boards/2", json={
        "title": "Blink Your Eyes",
        "creator": "Tanvi"
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 200
    assert response_body == "Board #2 successfully updated"

def test_update_board_with_extra_keys(client, two_saved_boards):
    # Arrange
    board_data = {
        "extra": "some stuff",
        "title": "Work Hard to succeed",
        "creator": "Federer"
    }

    # Act
    response = client.put("/boards/1", json=board_data)
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 200
    assert response_body == "Board #1 successfully updated"

##### tests on POST one card to one board
def test_create_one_card_to_board(client, two_saved_boards):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Happy!"  
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["message"] == "Happy!"
    assert response_body["likes_count"] == 0
    assert response_body["board_id"] == 1
    assert response_body["board_title"] == "Testing Board One"


def test_create_one_card_to_board_missing_keyword_message(client, two_saved_boards):
    # Act
    response = client.post("/boards/1/cards", json={
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A message must be included to add a card"



def test_create_one_card_to_board_empty_message(client, two_saved_boards):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": ""
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A message must be included to add a card"


def test_create_one_card_to_board_with_message_more_than_40_characters(client, two_saved_boards):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "Happy!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body["message"] == "A message must be less than or equal to 40 characters"

##### tests on GET all cards for the board with id
#@pytest.mark.skip()
def test_rentals_by_customer(client, one_posted_card):
    response = client.get("/boards/1/cards")

    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["message"] == CARD_MESSAGE


##### tests on DELETE one card from one board with ids
@pytest.mark.skip()
def test_delete_one_card_from_one_board(client, two_saved_boards, one_posted_card):
    # Act
    response = client.delete("/boards/1/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == "Card 1 in Board 1 successfully deleted"
    assert Card.query.get(1) == None

@pytest.mark.skip()
def test_does_not_delete_card_with_invalid_board_id(client, two_saved_boards, one_posted_card):
    # Act
    response = client.delete("/boards/helloworld/cards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": f"Board helloworld invalid"}

@pytest.mark.skip()
def test_does_not_delete_card_with_non_existent_board_id(client, two_saved_boards, one_posted_card):
    # Act
    response = client.delete("/boards/100/cards/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message":f"Board 100 not found"}

@pytest.mark.skip()
def test_does_not_delete_card_with_invalid_card_id(client, two_saved_boards, one_posted_card):
    # Act
    response = client.delete("/boards/1/cards/hi")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": f"Card hi invalid"}

@pytest.mark.skip()
def test_does_not_delete_card_with_non_existent_card_id(client, two_saved_boards, one_posted_card):
    # Act
    response = client.delete("/boards/1/cards/1000")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message":f"Card 1000 not found"}


# test on DELTETE one card
#@pytest.mark.skip()
def test_delete_one_card(client, one_card):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert
    assert response_body["message"] == "Card #1 successfully deleted"
    assert response.status_code == 200
    assert Card.query.get(1) == None