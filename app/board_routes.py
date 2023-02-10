from app import db
from app.models.board import Board
from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.card import Card
from .routes_helper import validate_model

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.route("", methods=["POST"])
def create_Board():
    request_body = request.get_json()

    if "title" not in request_body or len(request_body["title"]) == 0:
        abort(make_response({"message":"A title must be included to add a board"}, 400))

    if "creator" not in request_body or len(request_body["creator"]) == 0:
        abort(make_response({"message":"A creator must be included to add a board"}, 400))


    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return new_board.to_dict(), 201

@boards_bp.route("", methods=["GET"])
def read_all_boards():
    board_query = Board.query
    title_query = request.args.get("title")
    if title_query:
        board_query = board_query.filter(Board.title.ilike(f"%{title_query}%"))
        
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "desc":
            board_query = board_query.order_by(Board.title.desc())
        else:
            board_query = board_query.order_by(Board.title.asc())

    boards = board_query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    return jsonify(boards_response)

@boards_bp.route("/<id>", methods=["GET"])
def read_one_board(id):
    board = validate_model(Board, id)
    return board.to_dict()

@boards_bp.route("/<id>", methods=["PUT"])
def update_board(id):
    board = validate_model(Board, id)

    request_body = request.get_json()
    board.title = request_body["title"]
    board.creator = request_body["creator"]
    

    db.session.commit()
    
    return make_response(f"Board #{id} successfully updated")

@boards_bp.route("/<id>", methods=["DELETE"])
def delete_board(id):
    board = validate_model(Board, id)

    db.session.delete(board)
    db.session.commit()

    return make_response(f"Board #{id} successfully deleted")

# Create a new Card for the board with id 

@boards_bp.route("/<id>/cards", methods=["POST"])
def add_new_card_to_board(id):
    board = validate_model(Board, id)

    request_body = request.get_json()

    if "message" not in request_body or len(request_body["message"]) == 0:
        abort(make_response({"message":"A message must be included to add a card"}, 400))
    
    if len(request_body["message"]) > 40:
        abort(make_response({"message":"A message must be less than or equal to 40 characters"}, 400))

    new_card = Card.from_dict(request_body)
    new_card.board = board

    db.session.add(new_card)
    db.session.commit()

    
    return new_card.to_dict(), 201

# GET all cards for the board with id
@boards_bp.route("/<id>/cards", methods=["GET"])
def get_all_cards_for_board(id):
    board = validate_model(Board, id)

    cards_response = []
    for card in board.cards:
        cards_response.append(card.to_dict())

    return jsonify(cards_response)


# DELETE a card from a board with ids 
@boards_bp.route("/<board_id>/cards/<card_id>", methods=["DELETE"])
def delete_card(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()

    return make_response(f"Card #{card_id} in Board #{board_id} successfully deleted")

