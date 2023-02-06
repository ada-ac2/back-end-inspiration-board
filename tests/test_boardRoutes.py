import pytest
from werkzeug.exceptions import HTTPException
from app.routes.board_routes import validate_model
from app.models.board import Board


def test_get_all_planets_with_no_records_return_empty_array(client):
    response = client.get("/planets")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []