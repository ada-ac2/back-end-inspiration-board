from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board


boards_bp = Blueprint("boards", __name__, url_prefix="/boards")

def validate_request_and_create_entry(cls, request_data):
    try:
        new_obj = cls.from_dict(request_data)
    except KeyError as e:
        key = str(e).strip("\'")
        abort(make_response(jsonify({"message": f"Request body must include {key}"}), 400))
    return new_obj


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