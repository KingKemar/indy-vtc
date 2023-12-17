import requests
import os
from app.utils.mappings import WEATHER_MAPPING

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(town):
    api_key = os.environ.get('METEO_API_KEY')
    if not api_key:
        raise ValueError("METEO_API_KEY environment variable not set")

    params = {
        'q': town,
        'appid': api_key,
        'units': 'metric'
    }

    response = requests.get(WEATHER_API_URL, params=params)

    if response.status_code != 200:
        return f"Error: Unable to fetch weather data, status code: {response.status_code}"

    weather_data = response.json()
    weather_description = weather_data['weather'][0]['main']
    town_temp = weather_data['main']['temp']

    return town_temp, WEATHER_MAPPING.get(weather_description, ["varied"])
