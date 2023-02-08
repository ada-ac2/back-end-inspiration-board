from werkzeug.exceptions import HTTPException
from app.board_routes import validate_model
from app.models.board import Board
import pytest

def test_get_boards_empty_db_returns_empty_list(client):
    # Act
    response = client.get("/boards")

    # Assert 
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_board_with_id_empty_db_returns_404(client):
    # Act
    response = client.get("/boards/100")

    # Assert 
    assert response.status_code == 404
    assert response.get_json() == {"message":f"Board 100 not found"}

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

def test_get_one_board_by_id(client, two_saved_boards):
    response = client.get("/boards/2") 

    assert response.status_code == 200
    board_list = response.get_json()

    assert len(board_list) == 4    
    assert board_list["id"] == 2
    assert board_list["title"] == "Testing Board Two"
    assert board_list["creator"] == "InspoBoardCheerUp New"

def test_create_one_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "like the dog",
        "creator": "Zoro"       
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 201
    assert response_body == "Board like the dog successfully created"


def test_create_one_board_missing_keyword_title(client):
    # Act
    response = client.post("/boards", json={
        "creator": "Zoro"       
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 400
    assert response_body == "{\"message\":\"A title must be included to add a board\"}\n"

def test_create_one_board_empty_title(client):
    # Act
    response = client.post("/boards", json={
        "title": "",
        "creator": "Zoro"       
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 400
    assert response_body == "{\"message\":\"A title must be included to add a board\"}\n"

def test_create_one_board_missing_keyword_creator(client):
    # Act
    response = client.post("/boards", json={
        "title": "like the dog"
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 400
    assert response_body == "{\"message\":\"A creator must be included to add a board\"}\n"

def test_create_one_board_empty_creator(client):
    # Act
    response = client.post("/boards", json={
        "title": "like the dog",
        "creator": ""  
    })
    response_body = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 400
    assert response_body == "{\"message\":\"A creator must be included to add a board\"}\n"

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

#####
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

