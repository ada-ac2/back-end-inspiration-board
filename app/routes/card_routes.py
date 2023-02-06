from flask import Blueprint, request, jsonify, make_response
from app.routes.helpers import validate_model, validate_request_body
from app.models.card import Card
from app import db

cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card_id)
    db.session.commit()

    response_obj = {
        "statuscode": 200,
        "message": f"Card with id: {card_id} successfully deleted"
    }
    return make_response(jsonify(response_obj),200)

cards_bp.route("/<card_id>/add-likes", methods=["PATCH"])
def add_likes_to_card(card_id):
    card = validate_model(Card,card_id)

    card.likes += 1

    db.session.commit()

    response_obj = {
        "statuscode": 200,
        "message": f"Increased likes for card id {card_id} to {card.likes}",
        "data": card.to_dict()
    }
    return make_response(jsonify(response_obj),200)

required_data = ["message"]

cards_bp.route("",methods=["POST"])
def create_card():
    request_body = request.get_json(silent=True)
    validate_request_body(request_body, required_data)

    new_card = Card(message=request_body["message"])

    db.session.add(new_card)
    db.session.commit()

    response_obj = {
        "statuscode": 201,
        "message": f"Created new card id: {new_card.id}",
        "data": new_card.to_dict()
    }
    return make_response(jsonify(response_obj),201)
