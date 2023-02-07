from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.routes.helpers import validate_model, validate_request_body
from app.models.card import Card

# blueprint for Board
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

###########       Routes Function      ##########

@boards_bp.route("",methods = ["POST"])
def create_board():
    request_body = request.get_json()
    validate_request_body(request_body,["title","owner"])

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    response_obj = {
        "statuscode":201,
        "message": f"Board: {new_board.title} created successfully.",
        "data": new_board.to_dict()
    }
    #return response message or return the title by itself
    return make_response(jsonify(response_obj), 201)
    
#get list of all boards
@boards_bp.route("", methods = ["GET"])
def read_all_boards():

    board_query = Board.query
    boards = board_query.all()

    board_response = []
    for board in boards:
        board_response.append(board.to_dict())

    response_obj = {
        "statuscode": 200,
        "message": "All boards showing below.",
        "data": board_response
    }

    return make_response(jsonify(response_obj), 200)

#get one board by id and return cards 
@boards_bp.route("/<board_id>", methods = ["GET"])
def read_one_board_by_id(board_id):
    board = validate_model(Board, board_id)

    return (board.to_dict(), 200)

#delete board by id (optional:if we'd like to include this feature)
@boards_bp.route("/<board_id>", methods = ["DELETE"])
def delete_one_board_by_id(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    response_obj = {
        "statuscode": 200,
        "message": f"Board {board_id} has been deleted successfully."
    }
    return make_response(jsonify(response_obj), 200)

@boards_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_to_board(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json(silent=True)
    validate_request_body(request_body, ["message"])

    new_card = Card(message=request_body["message"])
    new_card.board = board

    db.session.add(new_card)
    db.session.commit()

    response_obj = {
        "statuscode": 201,
        "message": f"Created new card id: {new_card.id}",
        "data": new_card.to_dict()
    }
    return make_response(jsonify(response_obj),201)




