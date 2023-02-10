from app.board_routes import Board
import pytest

def test_to_dict_no_missing_data():
    # Arrange
    test_data = Board(id = 1,
                title="Testing Board One",
                creator="InspoBoardCheerup")
    
    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] == "Testing Board One"
    assert result["creator"] == "InspoBoardCheerup"
    


def test_to_dict_missing_id():
    # Arrange
    test_data = Board(
                title="Testing Board One",
                creator="InspoBoardCheerup")
    
    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] is None
    assert result["title"] == "Testing Board One"
    assert result["creator"] == "InspoBoardCheerup"
    
def test_to_dict_missing_title():
    # Arrange
    test_data = Board(id = 1,
                creator="InspoBoardCheerup")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] is None
    assert result["creator"] == "InspoBoardCheerup"

def test_to_dict_missing_creator():
    # Arrange
    test_data = Board(id = 1,
                title="Testing Board One")
    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result) == 4
    assert result["id"] == 1
    assert result["title"] == "Testing Board One"
    assert result["creator"] is None

# from_dict tests

def test_from_dict_returns_board():
    # Arrange
    board_data = {
                "title":"Testing Board Two",
                "creator":"InspoBoardCheerUp New"
    }
    
    # Act
    result = Board.from_dict(board_data)

    # Assert
    assert result.title == "Testing Board Two"
    assert result.creator == "InspoBoardCheerUp New"
    

def test_from_dict_with_no_title():
    # Arrange
    board_data = {
                
                "creator":"InspoBoardCheerUp New"
    }
    

    # Act & Assert
    with pytest.raises(KeyError, match = "title"):
        result = Board.from_dict(board_data)


def test_from_dict_with_no_creator():
    # Arrange
    board_data = {
                "title":"Testing Board Two"
    }
    
    

    # Act & Assert
    with pytest.raises(KeyError, match = "creator"):
        result = Board.from_dict(board_data)

def test_from_dict_with_extra_keys():
    # Arrange
    board_data = {
                "title":"Testing Board Two",
                "creator": "InspoBoardCheerUp New",
                "extra": "New Stuff"}
    
    # Act
    result = Board.from_dict(board_data)

    # Assert
    assert result.title == "Testing Board Two"
    assert result.creator == "InspoBoardCheerUp New"
    
