import pytest
from werkzeug.exceptions import HTTPException
from app.routes.board_routes import validate_model
from app.models.board import Board


def test_get_all_boards_with_no_records_return_empty_array(client):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []


def test_get_board_by_id_return_200_successful_code(client, saved_two_boards):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["title"] == "Hello,world!"
    assert response_body["owner"] == "Nad"
    assert response_body["cards"] == []

def test_get_board_by_not_exist_id_return_404(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404

def test_get_board_by_invalid_planet_id_return_400_bad_request_error(client, saved_two_boards):
    response = client.get("/boards/hello")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body[0]["message"] == "Board id hello is Invalid"

def test_get_all_boards_with_two_records_return_array_with_size_2(client, saved_two_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0]["id"] == 1
    assert response_body[0]["title"] == "Hello,world!"
    assert response_body[0]["owner"] == "Nad"
    assert response_body[0]["cards"] == []
    assert response_body[1]["id"] == 2
    assert response_body[1]["title"] == "Hello,friend!"
    assert response_body[1]["owner"] == "Jennifer"
    assert response_body[0]["cards"] == []

