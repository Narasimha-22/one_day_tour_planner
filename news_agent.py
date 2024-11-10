# File: news_agent.py

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class NewsAgent:
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')

    def get_local_events(self, city, date):
        # Return mock data if the API key is missing (useful for testing without an API key)
        if not self.api_key:
            return [
                {"title": "Food Festival", "location": "City Center", "time": "1:00 PM - 4:00 PM"},
                {"title": "Historical Walk", "location": "Old Town", "time": "11:00 AM - 1:00 PM"}
            ]
        
        # Correct URL for NewsAPI endpoint
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": city,
            "from": date,
            "sortBy": "relevance",
            "apiKey": self.api_key
        }
        
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])
            # Process articles as events with placeholder locations and publication times
            return [
                {"title": article["title"], "location": "Various Locations", "time": article["publishedAt"]}
                for article in articles
            ]
        else:
            return [{"title": "No events found", "location": "", "time": ""}]

