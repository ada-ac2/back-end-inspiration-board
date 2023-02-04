from app import db
from app.models.board import Board
from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.card import Card


cards_bp = Blueprint("cards_bp", __name__, url_prefix="/cards")