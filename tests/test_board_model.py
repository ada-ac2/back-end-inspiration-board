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
    assert result.id == 1
    assert result.status == True
    assert result.selected == False
    assert result.title == "Test Title 12"
    assert result.owner == "Test Owner 12"