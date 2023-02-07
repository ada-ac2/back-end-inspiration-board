from flask import abort, make_response, jsonify

def validate_model(cls, model_id):
    response_obj = {}
    try:
        model_id = int(model_id)
    except:
        response_obj["statuscode"] = 400
        response_obj["message"] = f"{cls.__name__} id {model_id} is Invalid"
        abort(make_response(jsonify(response_obj),400))

    model = cls.query.get(model_id)    

    if model:
        return model
    response_obj["statuscode"] = 404
    response_obj["message"] = f"{cls.__name__} id {model_id} is Not Found"
    abort(make_response(jsonify(response_obj),404))

#required data is a list of attributes the request body must have to be valid
def validate_request_body(request_body,required_data):
    response_obj= {}
    if not request_body:
        response_obj["message"] = "No request body: an empty or invalid json object was sent."
        response_obj["statuscode"] = 400
        abort(make_response(jsonify(response_obj),400))
    
    for data in required_data:
        if data not in request_body: 
            response_obj["message"] = f"Invalid request. Request body must include {data}."
            response_obj["statuscode"] = 400
            abort(make_response(jsonify(response_obj),400))

    return request_body