import pytest
from app.models.card import Card


# tests for GET
def test_get_all_cards_for_one_board_with_empty_card_table_returns_empty_list(client, add_two_boards):
    response = client.get("/boards/1/cards")

    assert response.get_json() == []
    assert response.status_code == 200


def test_get_all_cards_for_one_board_with_2_cards_in_table(client, add_two_cards_to_board_one):
    response = client.get("/boards/1/cards")

    assert response.status_code == 200
    assert len(response.get_json()) == 2
    assert response.get_json()[0]["id"] == 1
    assert response.get_json()[1]["id"] == 2
    assert response.get_json()[0]["message"] == "first sample card for board 1"
    assert response.get_json()[1]["message"] == "second sample card for board 1"


def test_get_all_cards_for_one_board_with_1_card_while_other_boards_are_populated(client, add_one_card_to_board_one_and_one_card_to_board_two):
    response = client.get("/boards/1/cards")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["id"] == 1
    assert response.get_json()[0]["message"] == "first sample card for board 1"
    assert response.get_json()[0]["likes_count"] == 0
    assert response.get_json()[0]["status"] == True
    assert response.get_json()[0]["board_id"] == 1


def test_get_all_cards_for_one_board_while_one_card_archived(client, archive_one_card):
    response = client.get("/boards/1/cards")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["id"] == 2
    assert response.get_json()[0]["message"] == "second sample card for board 1"

# tests for POST
def test_create_new_card_for_board_one_successfully(client, add_two_boards):
    new_card_data = {"message":"this is a test card!"}

    response = client.post("/boards/1/cards", json=new_card_data)

    assert response.status_code == 201
    assert response.get_json() == {"message":"Card #1 successfully added to title_1 board"}


def test_create_new_card_for_board_one_without_message_returns_400(client, add_two_boards):
    new_card_data = {"messageS":"this is a test card!"}

    response = client.post("/boards/1/cards", json=new_card_data)

    assert response.status_code == 400
    assert response.get_json() == {"message":"a message must be included to add a card"}


# tests for validate_model helper function
def test_create_new_card_for_invalid_board_id_returns_400(client, add_two_boards):
    new_card_data = {"message":"this is a test card!"}

    response = client.post("/boards/one/cards", json=new_card_data)

    assert response.status_code == 400
    assert response.get_json() == {"message":"Board one is an invalid ID"}


def test_create_new_card_for_nonexistant_board_id_returns_404(client, add_two_boards):
    new_card_data = {"message":"this is a test card!"}

    response = client.post("/boards/3/cards", json=new_card_data)

    assert response.status_code == 404
    assert response.get_json() == {"message":"Board #3 not found"}


# tests for PATCH "/like/<card_id>"
def test_like_card_increases_likes_count(client, add_two_cards_to_board_one):
    response = client.patch("/boards/1/cards/like/1")

    assert response.status_code == 200
    assert response.get_json() == {"message":f"card #1 has been liked. It has 1 likes now"}


# tests for PATCH "archive/<card_id>"
def test_delete_card_changes_status_to_false(client, add_two_cards_to_board_one):
    response = client.patch("/boards/1/cards/archive/1")

    assert response.status_code == 200
    assert response.get_json() == {"message":f"card #1 has been successfully removed from the title_1 board"}