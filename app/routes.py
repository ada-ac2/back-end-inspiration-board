from flask import Blueprint, request, jsonify,abort, make_response
from app import db
from app.models.board import Board 
from app.models.card import Card 

card_bp = Blueprint("card_bp", __name__, url_prefix="/cards")
board_bp = Blueprint("board_bp", __name__, url_prefix="/boards")

#  --------------------------------- Board routes ---------------------------------
# Add a board 
@board_bp.route("", methods = ["POST"])
def create_board():
    board_data = validate_board_input(request.get_json())
    new_board = Board.from_dict(board_data)

    db.session.add(new_board)
    db.session.commit()
    return make_response(
        jsonify({
                "title" : new_board.title,
                "owner" : new_board.owner,
                "cards": [] 
            }), 201)

# Add a card to a board by board id 
@board_bp.route("/<board_id>/cards", methods = ["POST"])
def add_card_to_board(board_id):
    board = validate_model(Board, board_id)
    card_data = validate_card_input(request.get_json())
    new_card = Card.from_dict(card_data, board_id)
    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(new_card.to_dict()), 201)

# Read a board by its id, display all cards underneath 
@board_bp.route("/<board_id>/cards", methods = ["GET"])
def get_cards_by_board_id(board_id): 
    board = validate_model(Board, board_id)
    cards = []
    for card in board.cards:
        cards.append(card.to_dict())
    return make_response(jsonify(cards), 200)


# Get all board names, id, owner 
@board_bp.route("", methods = ["GET"])
def get_all_boards():
    board_query = Board.query.all()
    board_response = []
    for board in board_query:
        board_response.append(board.to_dict())
    return jsonify(board_response)

# Delete a board by board id
@board_bp.route("/<board_id>", methods = ["DELETE"])
def delete_board(board_id):
    board = validate_model(Board, board_id)
    for card in board.cards:
        db.session.delete(card)
    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify(f"Board #{board.board_id} successfully deleted"))

# --------------------------------- Card routes --------------------------------- 

# Get all cards when no board is selected
@card_bp.route("", methods = ["GET"])
def get_all_cards():
    cards = Card.query.all()
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())
    return jsonify(cards_response)

# Get card by card id 
@card_bp.route("/<card_id>", methods = ["GET"])
def get_card_by_id(card_id):
    card = validate_model(Card, card_id)
    return make_response(jsonify(card.to_dict()), 200)

# Update a card by card id (like_count, message) 
@card_bp.route("/<card_id>", methods = ["PUT"])
def update_card_by_id(card_id):
    card = validate_model(Card, card_id)
    request_body = validate_card_input(request.get_json())
    card.message = request_body["message"]
    card.likes_count = request_body["likes_count"]
    card.board_id = request_body["board_id"]

    db.session.commit()
    message = f"Card {card_id} successfully updated"
    return make_response(jsonify(message), 200)

# # Delete a card 
@card_bp.route("/<card_id>", methods = ["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify(f"Card #{card.card_id} successfully deleted"))
    
# --------------------------------- helper functions --------------------------------- 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if model:
        return model
    abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

def validate_board_input(board_data):
    if "title" not in board_data \
        or board_data["title"] == "" \
        or "owner" not in board_data \
        or board_data["owner"] == "":
        return abort(make_response(jsonify("Invalid request"), 400))
    return board_data

def validate_card_input(card_data):
    if "message" not in card_data \
        or card_data["message"] == "":
        return abort(make_response(jsonify("invalid request"), 400))
    return card_data