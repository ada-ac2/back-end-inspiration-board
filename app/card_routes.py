from app import db
from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.card import Card
from .routes_helper import validate_model


cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

# DELETE
@cards_bp.route("/<id>", methods=["DELETE"])
def delete_card(id):
    card = validate_model(Card, id)

    db.session.delete(card)
    db.session.commit()

    return make_response({"message": f"Card #{card.id} successfully deleted"})