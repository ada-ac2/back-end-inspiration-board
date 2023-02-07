import pytest
from app.models.card import Card


def test_get_all_cards_for_one_board_with_empty_card_table_returns_empty_list(client, add_two_boards):
    response = client.get("/boards/1/cards")

    assert response.get_json() == []
    assert response.status_code == 200

def test_get_all_cards_for_one_board_with_2_cards_in_table(client, add_two_boards, add_two_cards_to_board_one):
    response = client.get("/boards/1/cards")

    assert response.status_code == 200
    assert len(response.get_json()) == 2
    assert response.get_json()[0]["id"] == 1
    assert response.get_json()[1]["id"] == 2
    assert response.get_json()[0]["message"] == "first sample card for board 1"
    assert response.get_json()[1]["message"] == "second sample card for board 1"

def test_get_all_cards_for_one_board_with_1_card_while_other_board_are_populated(client, add_two_boards, add_one_card_to_board_one_and_one_card_to_board_two):
    response = client.get("/boards/1/cards")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["id"] == 1
    assert response.get_json()[0]["message"] == "first sample card for board 1"


