from app.models.board import Board
import pytest


def test_from_dict_with_valid_input(client, add_two_boards):
    pass


"""def test_from_dict_with_valid_input(client, add_two_boards):
    test_data = {
        "message" : "Enjoy coding everyone!"
    }

    result = Card.from_dict(test_data, 1)

    assert result.message == "Enjoy coding everyone!"
    assert result.board_id == 1

def test_from_dict_without_message_input_raises_error(client, add_two_boards):
    test_data = {
        "messageS" : "Enjoy coding everyone!"
    }

    with pytest.raises(KeyError, match="message"):
        Card.from_dict(test_data, 1)"""