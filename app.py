# File: app.py

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from memory_agent import MemoryAgent
from itinerary_generator import ItineraryGenerator
from weather_agent import WeatherAgent
from news_agent import NewsAgent
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Allow CORS for API interaction with frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
memory_agent = MemoryAgent()
itinerary_generator = ItineraryGenerator()
weather_agent = WeatherAgent()
news_agent = NewsAgent()

class UserRequest(BaseModel):
    city: str
    interests: list
    budget: int
    start_location: str
    start_time: str
    end_time: str

@app.post("/generate-itinerary/")
def generate_itinerary(request: UserRequest):
    itinerary = itinerary_generator.generate_itinerary(
        request.city,
        request.interests,
        request.start_time,
        request.end_time
    )
    optimized_itinerary = memory_agent.optimize_itinerary(
        itinerary, request.city, request.budget
    )
    weather_info = weather_agent.get_weather(request.city, request.start_time)
    local_events = news_agent.get_local_events(request.city, request.start_time)

    return {
        "itinerary": optimized_itinerary,
        "weather": weather_info,
        "local_events": local_events
    }
