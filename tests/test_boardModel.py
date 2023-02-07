import pytest
from app.models.board import Board
from app.routes.helpers import validate_model

def test_to_dict_no_miss_data():
    test_data = Board(id = 1,
                title = "Hello",
                owner = "World",)
    
    result = test_data.to_dict()

    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] == "Hello"
    assert result["owner"] == "World"
    assert result["cards"] == []


def test_to_dict_missing_title():
    test_data = Board(id = 1,
                owner = "World",)

    result = test_data.to_dict()

    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] is None
    assert result["owner"] == "World"
    assert result["cards"] == []


def test_from_dict_with_no_title():
    board_data = {
                "owner" : "World"
    }

    with pytest.raises(KeyError, match = 'title'):
        new_board = Board.from_dict(board_data)


def test_from_dict_with_no_owner():
    board_data = {
                "title" : "World"
    }

    with pytest.raises(KeyError, match = 'owner'):
        new_board = Board.from_dict(board_data)

def test_from_dict_with_extra_keys():
    board_data = {
        "title" : "World",
        "owner" : "Hello",
        "extra" : "very extra"
    }
    new_board = Board.from_dict(board_data)
        
    assert new_board.title == "World"
    assert new_board.owner== "Hello"
    assert new_board.cards == []
