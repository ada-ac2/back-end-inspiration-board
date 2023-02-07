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