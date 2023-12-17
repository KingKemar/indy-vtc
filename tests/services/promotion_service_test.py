from app.models.promotion import PromoCode, DateRestriction
from unittest.mock import patch


def test_apply_promocode_success(client):

    promo = PromoCode(
        name="valid_promocode",
        avantage={"avantage_type": "percent", "value": 15},
        restrictions=[DateRestriction(after="2023-12-01", before="2023-12-31")]
    )
    promo.save()

    response = client.post('/apply_promocode', json={
        "promocode_name": "valid_promocode",
        "arguments": {"age": 25, "meteo": {"town": "Lyon"}}
    })

    assert response.status_code == 200
    assert response.json == {
        "promocode_name": "valid_promocode",
        "status": "accepted",
        "avantage": {"percent": 15}
    }


def test_apply_promocode_missing_data(client):
    response = client.post('/apply_promocode', json={
        "promocode_name": "",
        "arguments": {}
    })
    assert response.status_code == 400
    assert "error" in response.json


def test_apply_promocode_not_found(client):

    response = client.post('/apply_promocode', json={
        "promocode_name": "nonexistent_promocode",
        "arguments": {"age": 25}
    })

    assert response.status_code == 404
    assert "error" in response.json
