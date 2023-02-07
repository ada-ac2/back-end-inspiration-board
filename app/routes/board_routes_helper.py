from flask import abort, make_response
from app.models.board import Board


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    class_obj = cls.query.get(model_id)
    if not class_obj:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return class_obj

def validate_board(request_body):
    title, owner = "title", "owner"
    if title not in request_body or not isinstance(request_body[title], str) or request_body[title] is None:
        abort(make_response({"details": f"Request body must include {title}."}, 400))
    if owner not in request_body or not isinstance(request_body[owner], str) or request_body[owner] is None:
        abort(make_response({"details": f"Request body must include {owner}."}, 400))

def validate_attribute(record, request_body):
    for key, value in request_body.items():
        try:
            getattr(record, key)
        except AttributeError:
            abort(make_response({"message": f"Attribute {key} does not exist."}, 400))
        setattr(record, key, value)
    return record