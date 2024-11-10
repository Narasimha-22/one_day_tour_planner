# one_day_tour_planner
One-Day Tour Planning Application 

1. **Set Up Neo4j Database**
Install and start Neo4j.
Change the password for the default user (neo4j).

2.Create a .env file in the root directory with the following content:
Update your .env file with the Neo4j credentials.
**Set Up API Keys and Environment Variables**

NEO4J_URI=bolt://localhost:7687

NEO4J_USERNAME=<neo4j-username>

NEO4J_PASSWORD=<neo4j-password>

WEATHER_API_KEY=<your-openweather-api-key>

NEWS_API_KEY=<your-news-api-key>


3. Install Ollama
**Start the Llama2 Model Server**

ollama serve --model llama2 --port 11434




4. **Project Structure**
.
├── app.py                   # Main backend logic with FastAPI
├── frontend.py              # Streamlit frontend application
├── itinerary_generator.py   # Itinerary generator using Llama2 model
├── weather_agent.py         # Weather data retrieval
├── news_agent.py            # News and events retrieval
├── memory_agent.py          # Memory and preference storage with Neo4j
├── requirements.txt         # Required Python packages
├── .env                     # Environment variables (not in repo; create it)
└── README.md                # Project documentation




5. **Running the Application**

uvicorn app:app --reload

streamlit run frontend.py


6. **Usage**
a.Enter User ID: Start by entering your unique user ID.
b.Select City and Date: Choose the city you plan to visit and specify the date.
c.Enter Preferences: Provide details like your interests, budget, start time, and end time.
d.View Generated Itinerary: After entering all details, view your custom itinerary along with the weather forecast and any local events.
e.Save Memories and Preferences: User preferences and memories are stored in the Neo4j database for personalized future recommendations.


7. **Troubleshooting**
Neo4j Authentication Errors: Ensure that Neo4j is running, and the credentials in your .env file match those set in Neo4j.
Llama2 Model Errors: If the model fails to respond, make sure the Llama2 server is running on the correct port and accessible.
API Key Errors: Check that your API keys for the weather and news services are correct and active.


**Future Improvements
Real-Time Travel Mode Adjustment: Adjust itinerary paths based on real-time budget updates.
