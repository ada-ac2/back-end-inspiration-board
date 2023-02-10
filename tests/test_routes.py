from app.models.board import Board
from app.models.card import Card

BOARD_TITLE_ONE = "First Board"
BOARD_TITLE_TWO = "Second Board"
BOARD_TITLE_THREE = "Third Board"
BOARD_OWNER_ONE = "First Owner"
BOARD_OWNER_TWO = "Second Owner"
BOARD_OWNER_THREE = "Third Owner"
BOARD_ONE_ID = 1
BOARD_TWO_ID = 2
BOARD_THREE_ID = 3

BOARD_ONE_CARD_COUNT = 1
BOARD_TWO_CARD_COUNT = 2
BOARD_THREE_CARD_COUNT = 3


CARD_ONE_MESSAGE = "Pickles are priceless"
CARD_TWO_MESSAGE = "Some Days are Fancy Free"
CARD_THREE_MESSAGE = "I like my dancing pants"
CARD_FOUR_MESSAGE = "Days are good Days are Bad Its okay to sometimes be sad"
CARD_FIVE_MESSAGE = "Its a good day"
CARD_SIX_MESSAGE = "I GOT THIS"

CARD_ONE_LIKES = 0
CARD_TWO_LIKES = 0
CARD_THREE_LIKES = 1
CARD_FOUR_LIKES = 2
CARD_FIVE_LIKES = 3
CARD_SIX_LIKES = 0

CARD_ONE_BOARD = 3
CARD_TWO_BOARD = 2
CARD_THREE_BOARD = 1
CARD_FOUR_BOARD= 3
CARD_FIVE_BOARD = 2
CARD_SIX_BOARD = 3

CARD_ONE_ID = 1
CARD_TWO_ID = 2
CARD_THREE_ID = 3
CARD_FOUR_ID = 4
CARD_FIVE_ID = 5
CARD_SIX_ID = 6

# Tests for Board routes
# POST / create Board
def test_create_board_valid_input(client):
    response = client.post("/boards", json = {
        "title":"Happy thoughts!",
        "owner":"Dreamer",
        "cards":[]
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 201
    assert response_body == {
        "title":"Happy thoughts!",
        "owner":"Dreamer",
        "cards":[]
    }

def test_create_board_invalid_input(client):
    response = client.post("/boards", json = {
        "title":"",
        "owner":"",
        "cards":[]
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 400

# GET all boards
def test_get_all_boards_with_no_boards_returns_empty_list(client):
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []

def test_get_all_boards_with_no_cards_returns_boards_info(client, list_three_boards_without_cards):
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "board_id": 1,
            "title": "First Board",
            "owner": "First Owner",
            "cards": []
        },
        {
            "board_id": 2,
            "title": "Second Board",
            "owner": "Second Owner",
            "cards": []
        },
        {
            "board_id": 3,
            "title": "Third Board",
            "owner": "Third Owner",
            "cards": []
        }
    ]

def test_get_all_boards_with_cards_returns_boards_info(client, list_three_boards_with_cards):
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "board_id": 1,
            "title": "First Board",
            "owner": "First Owner",
            "cards": [
                {
                "board_id": 1,
                "card_id": 1,
                "message" : "Pickles are priceless",
                "likes_count": 0},
                {
                "board_id": 1,
                "card_id": 2,
                "message" : "Some Days are Fancy Free",
                "likes_count": 0}]
        },
        {
            "board_id": 2,
            "title": "Second Board",
            "owner": "Second Owner",
            "cards": [
                {
                "board_id": 2,
                "card_id": 3,
                "message" : "I like my dancing pants",
                "likes_count": 1}]
        },
        {
            "board_id": 3,
            "title": "Third Board",
            "owner": "Third Owner",
            "cards": [
                {
                "board_id": 3,
                "card_id": 4,
                "message" : "Days are good Days are Bad Its okay to sometimes be sad",
                "likes_count": 2}]
        }
    ]

# Tests for Card inside Board routes
# GET cards by Board id
def test_get_all_cards_by_id_no_cards(client, one_board):
    response = client.get("/boards/1/cards")
    response_body = response.get_json()
    print(response_body)

    assert response.status_code==200
    assert len(response_body) == 0
    assert response_body == []

def test_get_all_cards_from_board_with_cards(client,one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card):
    response = client.get("/boards/3/cards")
    response_body = response.get_json()

    new_one = Card.query.get(1)
    new_four = Card.query.get(4)
    new_six = Card.query.get(6)


    assert response.status_code == 200
    assert len(response_body) == 3
    assert  new_one.to_dict() in response_body
    assert new_four.to_dict() in response_body
    assert new_six.to_dict() in response_body

def test_get_all_cards_by_no_board_returns_error(client):
    response = client.get("/boards/1/cards")
    
    assert response.status_code == 404

# POST card to the board by board_id
def test_add_card_to_board_with_valid_board_id_valid_input_201(client, one_board_without_cards):
    board_id = 1
    response = client.post(f"/boards/{board_id}/cards", json = {
        "message": "Smile! :)",
        "likes_count": 0,
        "board_id": 1
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 201
    assert response_body == {
        "card_id": 1,
        "board_id": 1,
        "message": "Smile! :)",
        "likes_count": 0
    }

def test_add_card_to_board_with_valid_board_id_invalid_input_400(client, one_board_without_cards):
    board_id = 1
    response = client.post(f"/boards/{board_id}/cards", json = {
        "message": "",
        "likes_count": 0,
        "board_id": 1
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 400

def test_add_card_to_board_with_invalid_board_id_return_400(client, one_board_without_cards):
    board_id = "hello"
    response = client.post(f"/boards/{board_id}/cards", json = {
        "message": "Smile! :)",
        "likes_count": 0,
        "board_id": 3
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 400

def test_add_card_to_board_with_not_existing_board_id_return_404(client, one_board_without_cards):
    board_id = 3
    response = client.post(f"/boards/{board_id}/cards", json = {
        "message": "Smile! :)",
        "likes_count": 0,
        "board_id": 3
    })
    response_body = response.get_json()
    #Assert
    assert response.status_code == 404

# DELETE a board
def test_delete_existing_board(client, one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card ):
    # Act 
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert 
    assert response.status_code  == 200
    assert response_body == "Board #1 successfully deleted"
    
def test_delete_missing_board(client, one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card ):
    # Act 
    response = client.delete("/boards/9")
    response_body = response.get_json()

    # Assert 
    assert response.status_code  == 404
    assert response_body == {"message": "Board 9 not found"}

def test_delete_board_invalid_id(client, one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card):
    # Act
    response = client.delete("/boards/invalid")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "invalid invalid"}

# GET card by id
def test_get_one_card_by_id(client,one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card):
    response_one = client.get('/cards/1')
    response_body = response_one.get_json()
    new_card = Card.query.get(1)
    print(response_body)

    assert response_one.status_code == 200
    assert response_body == new_card.to_dict()
    assert response_body['card_id'] == CARD_ONE_ID
    assert response_body["message"] == CARD_ONE_MESSAGE
    assert response_body["board_id"] == CARD_ONE_BOARD
    assert response_body["likes_count"] == CARD_ONE_LIKES

def test_no_such_card_returns_error(client):
    response_one = client.get('/cards/1')
    assert response_one.status_code == 404

# UPDATE card by id
def test_update_card_by_existed_id_returns_card_info(client, one_board_with_one_card):
    card_id = 1
    response = client.put(f"/cards/{card_id}", json = {
        "message": "Great Achievements Begin With Small Steps",
        "likes_count": 2,
        "board_id": 1
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert response_body == f"Card {card_id} successfully updated"

def test_update_card_by_invalid_id_returns_400(client, one_board_with_one_card):
    response = client.put(f"/cards/hello", json = {
        "message": "Great Achievements Begin With Small Steps",
        "likes_count": 2,
        "board_id": 1
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "hello invalid"}

def test_update_card_by_invalid_id_returns_404(client, one_board_with_one_card):
    response = client.put(f"/cards/5", json = {
        "message": "Great Achievements Begin With Small Steps",
        "likes_count": 2,
        "board_id": 1
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Card 5 not found"}

# DELETE a card
def test_delete_existing_card(client, one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card ):
    # Act 
    response = client.delete("/cards/1")
    response_body = response.get_json()

    # Assert 
    assert response.status_code  == 200
    assert response_body == "Card #1 successfully deleted"
    
def test_delete_missing_card(client, one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card ):
    # Act 
    response = client.delete("/cards/9")
    response_body = response.get_json()

    # Assert 
    assert response.status_code  == 404
    assert response_body == {"message": "Card 9 not found"}

def test_delete_card_invalid_id(client, one_board,two_board, three_board, one_card,two_card, three_card,four_card,five_card, six_card):
    # Act
    response = client.delete("/cards/invalid")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "invalid invalid"}