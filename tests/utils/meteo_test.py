import requests
import os
from app.utils.mappings import WEATHER_MAPPING
from app.utils.meteo import get_weather

VALID_CITY = "London"


def test_correct_response():
    """Test if the function returns correct weather information for a valid city."""
    response = get_weather(VALID_CITY)
    expected_conditions = set(sum(WEATHER_MAPPING.values(), []))
    assert any(item in expected_conditions for item in response), \
        "Response did not contain any expected weather conditions"
