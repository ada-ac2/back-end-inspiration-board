from app import db
from app.models.board import Board
from app.models.card import Card
from flask import Blueprint, jsonify, make_response, request, abort


board_bp = Blueprint("boards", __name__, url_prefix="/boards")


@board_bp.route("", methods=["POST"])
def create_board():
    request_body = 