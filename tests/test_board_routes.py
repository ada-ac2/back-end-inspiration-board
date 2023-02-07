from operator import contains
from app.models.board import Board
from app.models.card import Card


def test_create_one_board_with_missing_title(client):
    # Act
    response = client.post("/boards", json={
        "owner": "owner_4"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Request body must include title."}

def test_create_one_board_with_missing_owner(client):
    # Act
    response = client.post("/boards", json={
        "title": "title_4"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Request body must include owner."}

def test_create_one_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "title_5",
        "owner": "owner_5"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body["title"] == "title_5"
    assert response_body["owner"] == "owner_5"

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_board(client, add_one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["title"] == "title_3"
    assert response_body[0]["owner"] == "owner_3"

def test_get_boards_two_saved_boards(client, add_two_boards):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["title"] == "title_1"
    assert response_body[0]["owner"] == "owner_1"
    assert response_body[1]["title"] == "title_2"
    assert response_body[1]["owner"] == "owner_2"

def test_read_one_board_does_not_exist(client, add_one_board):
    # Act
    response = client.get("/boards/6")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 6 was not found"}

def test_read_one_board_archived(client, add_one_board):
    # Act
    # how do I create Act here???
    pass
    # Assert

def test_read_one_board(client, add_two_boards):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body["title"] == "title_1"
    assert response_body["owner"] == "owner_1"

def test_update_one_board(client, add_one_board):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated TITLE",
        "owner": "Updated OWNER"
    })
    response_body = response.get_json()
    # Assert
    assert response.status == '200 OK' # why is this different from others?
    assert response_body["title"] == "Updated TITLE"
    assert response_body["owner"] == "Updated OWNER"

def test_update_one_board_with_missing_title(client, add_one_board):
    # Act
    response = client.put("/boards/1", json={
        "owner": "Updated OWNER"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Request body must include title."}

def test_update_one_board_with_missing_owner(client, add_one_board):
    # Act
    response = client.put("/boards/1", json={
        "title": "Updated TITLE"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Request body must include owner."}

def test_patch_one_board_title(client, add_one_board):
    # Act
    response = client.patch("/boards/1", json={
        "title": "Updated TITLE"
    })
    response_body = response.get_json()
    # Assert
    assert response.status == '200 OK' # why is this different from others?
    assert response_body["title"] == "Updated TITLE"
    assert response_body["owner"] == "owner_3"

def test_patch_one_board_owner(client, add_one_board):
    # Act
    response = client.patch("/boards/1", json={
        "owner": "Updated OWNER"
    })
    response_body = response.get_json()
    # Assert
    assert response.status == '200 OK' # why is this different from others?
    assert response_body["title"] == "title_3"
    assert response_body["owner"] == "Updated OWNER"

def test_delete_one_board(client, add_two_boards):
    # Act
    response = client.delete("/boards/2")
    response_body = response.get_json()
    #Assert
    assert response.status == "200 OK"
    assert response_body["status"] == False