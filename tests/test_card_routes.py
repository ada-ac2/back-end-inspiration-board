from app.models.board import Board
from app.models.card import Card

CARD_MESSAGE = "My awesome new card"
OWNER = "Nad"
TITLE = "My test board"

#----------------------Tests for create card with board

def test_create_card_with_board_valid_request_body(client, one_board):
    request_body = {"message":CARD_MESSAGE}
    response = client.post("boards/1/cards",json=request_body)

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["statuscode"] == 201
    assert response_body["message"] == "Created new card id: 1"
    assert len(response_body["data"]) == 3
    assert response_body["data"]["id"] == 1
    assert response_body["data"]["message"] == CARD_MESSAGE
    assert response_body["data"]["likes"] == 0
    # assert len(response_body["data"]["board"]) == 3
    # assert response_body["data"]["board"]["id"] == 1
    # assert response_body["data"]["board"]["owner"] == OWNER
    # assert response_body["data"]["board"]["title"] == TITLE

def test_create_card_with_board_no_message_request_body(client, one_board):
    request_body = {"anotherAttribute":3}
    response = client.post("boards/1/cards",json=request_body)

    response_body = response.get_json()
    assert response.status_code == 400
    assert response_body["statuscode"] == 400
    assert response_body["message"] == "Invalid request. Request body must include message."

def test_create_card_with_board_empty_request_body(client, one_board):
    request_body = {}
    response = client.post("boards/1/cards",json=request_body)

    response_body = response.get_json()
    assert response.status_code == 400
    assert response_body["statuscode"] == 400
    assert response_body["message"] == "No request body: an empty or invalid json object was sent."

def test_create_card_with_board_extra_parameters_request_body(client, one_board):
    request_body = {"message":CARD_MESSAGE, "another": 3}
    response = client.post("boards/1/cards",json=request_body)

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["statuscode"] == 201
    assert response_body["message"] == "Created new card id: 1"
    assert len(response_body["data"]) == 3
    assert response_body["data"]["id"] == 1
    assert response_body["data"]["message"] == CARD_MESSAGE
    assert response_body["data"]["likes"] == 0
    # assert len(response_body["data"]["board"]) == 3
    # assert response_body["data"]["board"]["id"] == 1
    # assert response_body["data"]["board"]["owner"] == OWNER
    # assert response_body["data"]["board"]["title"] == TITLE

def test_create_card_with_board_non_numeric_board_id(client, one_board):
    request_body = {"message":CARD_MESSAGE}
    invalid_id = "board"
    response = client.post(f"boards/{invalid_id}/cards",json=request_body)

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["statuscode"] == 400
    assert response_body["message"] == f"Board id {invalid_id} is Invalid"

def test_create_card_with_board_inexistent_board_id(client, one_board):
    request_body = {"message":CARD_MESSAGE}
    invalid_id = "3"
    response = client.post(f"boards/{invalid_id}/cards",json=request_body)

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["statuscode"] == 404
    assert response_body["message"] == f"Board id {invalid_id} is Not Found"


#-------------- Test for add_likes_to_card

def test_add_likes_to_card_valid_id(client, one_card_to_board):
    response = client.patch("cards/1/add-likes")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["statuscode"] == 200
    assert response_body["message"] == "Increased likes for card id 1 to 1"
    assert len(response_body["data"]) == 3
    assert response_body["data"]["id"] == 1
    assert response_body["data"]["message"] == "Good message"
    assert response_body["data"]["likes"] == 1
    # assert len(response_body["data"]["board"]) == 3
    # assert response_body["data"]["board"]["id"] == 1
    # assert response_body["data"]["board"]["owner"] == OWNER
    # assert response_body["data"]["board"]["title"] == TITLE

def test_add_likes_to_card_non_numeric_id(client, one_card_to_board):
    invalid_id = "card"
    response = client.patch(f"cards/{invalid_id}/add-likes")

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["statuscode"] == 400
    assert response_body["message"] == f"Card id {invalid_id} is Invalid"

def test_add_likes_to_card_inexistent_id(client, one_card_to_board):
    invalid_id = "5"
    response = client.patch(f"cards/{invalid_id}/add-likes")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["statuscode"] == 404
    assert response_body["message"] == f"Card id {invalid_id} is Not Found"

#-----------------Delete card tests ------------------------------

def test_delete_card_valid_id(client, one_card_to_board):
    id = 1
    response = client.delete(f"cards/{id}")

    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["statuscode"] == 200
    assert response_body["message"] == f"Card with id: {id} successfully deleted"

def test_delete_card_non_numeric_id(client, one_card_to_board):
    id = "card"
    response = client.delete(f"cards/{id}")

    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body["statuscode"] == 400
    assert response_body["message"] == f"Card id {id} is Invalid" 

def test_delete_card_inexisten_id(client, one_card_to_board):
    id = "3"
    response = client.delete(f"cards/{id}")

    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body["statuscode"] == 404
    assert response_body["message"] == f"Card id {id} is Not Found"