import streamlit as st
from itinerary_generator import ItineraryGenerator
from weather_agent import WeatherAgent
from news_agent import NewsAgent
from memory_agent import MemoryAgent
import datetime

# Initialize agents
generator = ItineraryGenerator()
weather_agent = WeatherAgent()
news_agent = NewsAgent()
memory_agent = MemoryAgent()

# Streamlit app setup
st.set_page_config(page_title="Interactive One-Day Trip Planner", layout="wide")
st.title("Welcome to One-Day Trip Planner!")

# Conversation flow
if 'conversation_stage' not in st.session_state:
    st.session_state['conversation_stage'] = 0

if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {}

# Conversation logic
if st.session_state['conversation_stage'] == 0:
    st.write("Hello! Please enter your User ID to proceed.")
    user_id = st.text_input("Enter your User ID:")
    if user_id:
        st.session_state['user_data']['user_id'] = user_id
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 1:
    st.write("Great! I can help you plan a one-day trip. Please tell me the name of the city you want to visit.")
    city = st.text_input("Enter the city name:")
    if city:
        st.session_state['user_data']['city'] = city
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 2:
    st.write(f"You want to visit {st.session_state['user_data']['city']}. What day are you planning for?")
    date = st.date_input("Select the date:", min_value=datetime.date.today())
    if date:
        st.session_state['user_data']['date'] = date
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 3:
    st.write("What time do you want to start your day?")
    start_time = st.time_input("Start time:", datetime.time(9, 0))
    if start_time:
        st.session_state['user_data']['start_time'] = start_time
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 4:
    st.write("What time do you want to end your day?")
    end_time = st.time_input("End time:", datetime.time(19, 0))
    if end_time:
        st.session_state['user_data']['end_time'] = end_time
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 5:
    st.write("What are your interests? You can select multiple.")
    interests = st.multiselect("Select your interests:", ["Historical Sites", "Beaches", "Shopping", "Food Experiences", "Nature", "Art Galleries"])
    if interests:
        st.session_state['user_data']['interests'] = interests
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 6:
    st.write("What's your budget for the day (in Euros)?")
    budget = st.number_input("Enter your budget:", min_value=0, value=100)
    if budget:
        st.session_state['user_data']['budget'] = budget
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 7:
    st.write("Where would you like to start your day? (e.g., hotel name or a specific location)")
    start_location = st.text_input("Enter the starting location:")
    if start_location:
        st.session_state['user_data']['start_location'] = start_location
        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 8:
    st.write("Thank you for providing all the details! Generating your itinerary now...")
    user_data = st.session_state['user_data']
    with st.spinner("Generating your itinerary..."):
        itinerary = generator.generate_itinerary(user_data['city'], user_data['interests'], user_data['start_time'].strftime("%I:%M %p"), user_data['end_time'].strftime("%I:%M %p"))
        st.success("Itinerary generated!")
        st.text_area("Generated Itinerary", itinerary, height=200)

        # Store the itinerary as a memory for the user
        memory_agent.add_memory(user_data['user_id'], f"Generated itinerary for {user_data['city']} on {user_data['date']}")

        # Provide weather information
        with st.spinner("Fetching weather information..."):
            weather_info = weather_agent.get_weather(user_data['city'], user_data['date'].strftime("%Y-%m-%d"))
            st.subheader("Weather Forecast:")
            st.write(weather_info)

        # Provide local events information
        with st.spinner("Fetching local events..."):
            local_events = news_agent.get_local_events(user_data['city'], user_data['date'].strftime("%Y-%m-%d"))
            st.subheader("Local Events:")
            if local_events:
                for event in local_events:
                    st.write(f"**Event**: {event['title']} at {event['location']} from {event['time']}")
            else:
                st.write("No events found for this date.")

        # Store preferences for the user
        for interest in user_data['interests']:
            memory_agent.add_user_preference(user_data['user_id'], interest)

        st.session_state['conversation_stage'] += 1

elif st.session_state['conversation_stage'] == 9:
    st.write("Thank you for using the One-Day Trip Planner! Here are your saved preferences and memories:")
    user_id = st.session_state['user_data']['user_id']
    memories = memory_agent.retrieve_memories(user_id)
    preferences = memory_agent.get_user_preferences(user_id)

    st.subheader("Your Memories:")
    if memories:
        for memory in memories:
            st.write(f"- {memory}")
    else:
        st.write("No memories found.")

    st.subheader("Your Preferences:")
    if preferences:
        for preference in preferences:
            st.write(f"- {preference}")
    else:
        st.write("No preferences found.")

    st.write("Have a great trip!")

# Close the memory agent connection
memory_agent.close()
