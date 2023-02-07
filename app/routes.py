from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

# Helper Functions
def validate_request_and_create_entry(cls, request_data):
    try:
        new_obj = cls.from_dict(request_data)
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}"}), 400))
    return new_obj

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message" : f" {cls.__name__} {model_id} invalid."}, 400))
    model = cls.query.get(model_id)
    if model:
        return model  
    abort(make_response({"message" : f" {cls.__name__} {model_id} not found."}, 404))


@boards_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    return make_response(jsonify(boards_response), 200)

@boards_bp.route("", methods=["POST"])
def create_one_board():
    request_body = request.get_json()
    new_board = validate_request_and_create_entry(Board, request_body)

    db.session.add(new_board)
    db.session.commit()

    return new_board.to_dict(), 201

# POST /board/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_new_card_to_board(board_id):
    board = validate_model(Board, board_id)
    
    card_data = request.get_json()
    card_data[board_id] = board.board_id
    new_card = Card.from_dict(card_data)
    
    db.session.add(new_card)
    db.session.commit()

    return make_response(new_card.to_dict(),200)

# GET /board/<board_id>/cards
@boards_bp.route("/<board_id>/cards", methods=["GET"])
def get_cards_by_board_id(board_id):
    board = validate_model(Board, board_id)
    
    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict())
    
    return make_response(jsonify(cards_response),200)

@boards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card_by_id(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(jsonify({"message": f"Card #{card.card_id} successfully deleted"}), 200)


