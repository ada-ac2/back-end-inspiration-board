from app.models.board import Board
from app.models.card import Card

CARD_MESSAGE = "My awesome new card"
OWNER = "Nad"
TITLE = "My test board"

def test_create_card_with_board_valid_request_body(client, one_board):
    request_body = {"message":CARD_MESSAGE}
    response = client.post("boards/1/cards",json=request_body)

    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body["statuscode"] == 201
    assert response_body["message"] == "Created new card id: 1"
    assert len(response_body["data"]) == 4
    assert response_body["data"]["id"] == 1
    assert response_body["data"]["message"] == CARD_MESSAGE
    assert response_body["data"]["likes"] == 0
    assert len(response_body["data"]["board"]) == 3
    assert response_body["data"]["board"]["id"] == 1
    assert response_body["data"]["board"]["owner"] == OWNER
    assert response_body["data"]["board"]["title"] == TITLE

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
    assert len(response_body["data"]) == 4
    assert response_body["data"]["id"] == 1
    assert response_body["data"]["message"] == CARD_MESSAGE
    assert response_body["data"]["likes"] == 0
    assert len(response_body["data"]["board"]) == 3
    assert response_body["data"]["board"]["id"] == 1
    assert response_body["data"]["board"]["owner"] == OWNER
    assert response_body["data"]["board"]["title"] == TITLE

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
