from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board


# blueprint for Board
boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

#########        Helper Function        ######
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} is invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

def validate_request_body(request_body):
    if "title" not in request_body or "owner" not in request_body:
        abort(make_response("Invalid Request", 400))



###########       Routes Function      ##########


@boards_bp.route("",methods = ["POST"])
def create_board():
    request_body = request.get_json()
    validate_request_body(request_body)

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    #return response message or return the title by itself
    return make_response(jsonify(f"Board: {new_board.title} created successfully."), 201)
    
#get list of all boards
@boards_bp.route("", methods = ["GET"])
def read_all_boards():

    board_query = Board.query
    boards = board_query.all()

    board_response = []
    for board in boards:
        board_response.append(board.to_dict())

    return make_response(jsonify(board_response), 200)

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

    return make_response(jsonify(f"Board {board_id} has been deleted successfully."), 200)