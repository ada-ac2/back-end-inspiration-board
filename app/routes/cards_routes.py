from app import db
from flask import Blueprint, abort, make_response, request
from app.models.card import Card
from app.models.board import Board


cards_bp = Blueprint("cards", __name__, url_prefix="/boards/<board_id>/cards")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} is an invalid ID"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} #{model_id} not found"}, 404))

    return model


@cards_bp.route("", methods=["POST"])
def create_card(board_id):
    board = validate_model(Board, board_id)
    request_body = request.get_json()

    # the only required attribute for the Card model is message
    if "message" not in request_body:
        abort(make_response({"message":"a message must be included to add a card"}, 400))

    new_card = Card.from_dict(request_body, board_id, board)
    db.session.add(new_card)
    db.session.commit()
    return make_response({"message":f"Card #{new_card.id} successfully added to {board.title} board"}, 201)


@cards_bp.route("/<card_id>", methods=["PATCH"])
def delete_card(board_id, card_id):
    board = validate_model(Board, board_id)
    card = validate_model(Card, card_id)
    card.status = False
    db.session.commit()
    return make_response(
        {"message":f"card #{card_id} has been successfully removed from the {board.title} board"}, 200
    )