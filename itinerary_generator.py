# itinerary_generator.py

from ollama import Client
from datetime import datetime, timedelta
import logging

class ItineraryGenerator:
    def __init__(self):
        self.client = Client(host="http://localhost:11434")
        logging.info("ItineraryGenerator initialized with Llama2 model.")

    def generate_itinerary(self, city, interests, start_time, end_time):
        # Prepare a prompt with time slots and user interests
        prompt = (
            f"Plan a one-day trip in {city} starting from {start_time} to {end_time}. "
            f"The user is interested in: {', '.join(interests)}. "
            "Provide an itinerary with hourly activities, covering each interest, check transporatation availability, and balancing exploration, meals, and relaxation."
        )
        logging.info(f"Prompt sent to Llama2: {prompt}")
        
        try:
            response = self.client.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
            logging.info(f"Llama2 Response: {response}")  # Log the full response for debugging

            if isinstance(response, dict):
                generated_text = response.get("message", {}).get("content", "Unable to generate itinerary.")
                
                # Parse the response into an hour-by-hour itinerary
                itinerary = self.parse_hour_by_hour(generated_text, start_time, end_time)
                return itinerary

            return "Unexpected response format."
        
        except Exception as e:
            logging.error(f"An error occurred while generating itinerary: {str(e)}")
            return f"An error occurred: {str(e)}"

    def parse_hour_by_hour(self, generated_text, start_time, end_time):
        """Custom parser to create an hour-by-hour itinerary from generated text."""
        logging.info("Parsing itinerary text into hour-by-hour format.")
        
        # Split generated text into lines
        generated_lines = generated_text.strip().split("\n")
        itinerary = []
        current_time = datetime.strptime(start_time, "%I:%M %p")
        end_time_dt = datetime.strptime(end_time, "%I:%M %p")
        
        # Iterate over lines and assign each line as an activity per hour
        for line in generated_lines:
            line = line.strip()
            if line and "**" not in line:  # Skip empty and non-activity lines
                # Format current time and add activity
                time_str = current_time.strftime("%I:%M %p")
                itinerary.append(f"{time_str}: {line}")
                
                # Increment time by one hour
                current_time += timedelta(hours=1)
                if current_time >= end_time_dt:
                    break  # Stop if the end time is reached

        parsed_itinerary = "\n".join(itinerary)
        logging.info(f"Parsed Itinerary: {parsed_itinerary}")
        return parsed_itinerary

