import pytest

from app.models.promotion import PromoCode
from app.models.restriction import DateRestriction
from flask import json
from datetime import datetime, timedelta


def test_apply_promocode_success(client):
    today = datetime.now().date()

    seven_days_before = today - timedelta(days=7)
    seven_days_after = today + timedelta(days=7)
    promo = PromoCode(
        name="valid_promocode",
        avantage={"avantage_type": "percent", "value": 15},
        restrictions=[
            DateRestriction(
                after=seven_days_before.strftime("%Y-%m-%d"),
                before=seven_days_after.strftime("%Y-%m-%d"),
            )
        ],
    )
    promo.save()

    response = client.post(
        "/apply_promocode",
        json={
            "promocode_name": "valid_promocode",
            "arguments": {"age": 25, "meteo": {"town": "Lyon"}},
        },
    )

    assert response.status_code == 200
    assert response.json == {
        "promocode_name": "valid_promocode",
        "status": "accepted",
        "avantage": {"percent": 15},
    }


def test_apply_promocode_missing_data(client):
    response = client.post(
        "/apply_promocode", json={"promocode_name": "", "arguments": {}}
    )
    assert response.status_code == 400
    assert "error" in response.json


def test_apply_promocode_not_found(client):
    response = client.post(
        "/apply_promocode",
        json={"promocode_name": "nonexistent_promocode",
              "arguments": {"age": 25}},
    )

    assert response.status_code == 404
    assert "error" in response.json


@pytest.mark.parametrize(
    "promo_data, expected_status",
    [
        # Valid promo code
        (
            {
                "name": "ValidPromo",
                "avantage": {"percent": 20},
                "restrictions": [
                    {"@date": {"after": "2022-12-31", "before": "2024-01-01"}}
                ],
            },
            201,
        ),
        # Invalid promo code (e.g., missing fields, invalid data)
        (
            {
                "name": "InvalidPromo",
                "avantage": {"percent": 150},
                # Invalid date range
                "restrictions": [
                    {"@date": {"after": "2024-01-01", "before": "2022-12-31"}}
                ],
            },
            400,
        ),
        # Add more test cases as needed
    ],
)
def test_create_promotion(client, promo_data, expected_status):
    response = client.post(
        "/create_promocode",
        data=json.dumps(promo_data),
        content_type="application/json",
    )
    assert response.status_code == expected_status
