# File: weather_agent.py

import requests
import os

class WeatherAgent:
    def __init__(self):
        self.api_key = os.getenv('WEATHER_API_KEY')

    def get_weather(self, city, date):
        url = f"https://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={city}&dt={date}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast = data["forecast"]["forecastday"][0]
            condition = forecast["day"]["condition"]["text"]
            temp = forecast["day"]["avgtemp_c"]
            return f"Weather on {date} in {city}: {condition}, Avg Temp: {temp}°C"
        return "Weather data unavailable."
