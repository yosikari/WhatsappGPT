import os
import requests
from datetime import datetime

API_KEY = os.getenv('OPEN_WEATHER_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"


def get_weather(city="Tel-aviv"):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city.capitalize()
    response = requests.get(url).json()

    # Temps:
    temp_kelvin = response['main']['temp']
    temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
    # Feels like temps:
    feels_like_kelvin = response['main']['feels_like']
    feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(
        feels_like_kelvin)
    # Humidity:
    humidity = response['main']['humidity']
    # Description:
    description = response['weather'][0]['description']
    # Sunrise time:
    sunrise_time = datetime.fromtimestamp(
        response['sys']['sunrise'] + response['timezone'])
    # Sunset time:
    sunset_time = datetime.fromtimestamp(
        response['sys']['sunset'] + response['timezone'])
    # Wind speed:
    wind_speed = round(response['wind']['speed']*3600/1000, 3)

    return ("*The weather in {}:* \n {}, {}°C  ({}°F), \n *Feels like:* {}°C ({}°F), \n *Humidity:* {}%, \n *Sunrise time:* {}, \n *Sunset time:* {}, \n *Wind speed:* {} km/h.".format(city, description, temp_celsius, temp_fahrenheit, feels_like_celsius, feels_like_fahrenheit, humidity, sunrise_time, sunset_time, wind_speed))


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9/5) + 32
    return round(celsius, 2), round(fahrenheit, 2)
