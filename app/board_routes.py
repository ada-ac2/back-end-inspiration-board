from app import db
from app.models.board import Board
from flask import Blueprint, jsonify, abort, make_response, request 
from app.models.card import Card


boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")