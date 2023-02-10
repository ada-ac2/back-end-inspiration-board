from app.models.board import Board
import pytest


def test_from_dict_with_valid_input():
    # Act
    test_data = {
        "title": "Test Title 12",
        "owner": "Test Owner 12"
    }
    result = Board.from_dict(test_data)
    # Assert
    assert result.title == "Test Title 12"
    assert result.owner == "Test Owner 12"

def test_from_dict_with_missing_attribute():
    # Act
    test_data = {
        "": "Test Title 12",
        "owner": "Test Owner 12"
    }
    # Assert
    with pytest.raises(KeyError, match="title"):
        Board.from_dict(test_data)

def test_to_dict_with_data():
    # Act
    test_data = {
        "title": "Test Title 12",
        "owner": "Test Owner 12"
    }
    result = Board.from_dict(test_data).to_dict()
    # Assert
    assert len(result) == 6
    assert result["id"] == None
    assert result["title"] == "Test Title 12"
    assert result["owner"] == "Test Owner 12"
    assert result["status"] == None
    assert result["selected"] == None
