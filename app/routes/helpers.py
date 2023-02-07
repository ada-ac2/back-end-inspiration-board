from flask import abort, make_response, jsonify

def validate_model(cls, model_id):
    response_obj = {}
    try:
        model_id = int(model_id)
    except:
        response_obj["statuscode"] = 400
        response_obj["message"] = f"{cls.__name__} id {model_id} is Invalid"
        abort(make_response(jsonify(response_obj,400)))

    model = cls.query.get(model_id)    

    if model:
        return model
 
    response_obj["statuscode"] = 404
    response_obj["message"] = f"{cls.__name__} id {model_id} is Not Found"
    abort(make_response(jsonify(response_obj),404))