import requests
import streamlit as st
from datetime import datetime

def get_weather_data(location, user_api):
    complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={user_api}"
    api_link = requests.get(complete_api_link)
    return api_link.json()

def display_weather_data():
    st.title("Weather Information Dashboard")
    user_api = st.text_input("Enter your OpenWeatherMap API Key:", type="password")
    location = st.text_input("Enter the city name:")

    st.markdown(
        """
        <style>
        .weather-card {
            background-color: #f0f8ff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
        }
        .weather-card h3 {
            margin-bottom: 15px;
            color: #007acc;
        }
        .weather-card p {
            font-size: 16px;
            color: #333;
        }
        .weather-card .highlight {
            font-weight: bold;
            color: #007acc;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if user_api and location:
        try:
            api_data = get_weather_data(location, user_api)

            if api_data.get("cod") != 200:
                st.error(f"Error fetching weather data: {api_data.get('message', 'Unknown error')}")
            else:
                temp_city = api_data['main']['temp'] - 273.15
                weather_desc = api_data['weather'][0]['description']
                hmdt = api_data['main']['humidity']
                wind_spd = api_data['wind']['speed']
                date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

                st.markdown(
                    f"""
                    <div class="weather-card">
                        <h3>Weather Stats for {location.upper()} || {date_time}</h3>
                        <p><span class="highlight">Current Temperature:</span> {temp_city:.2f} °C</p>
                        <p><span class="highlight">Weather Description:</span> {weather_desc.capitalize()}</p>
                        <p><span class="highlight">Humidity:</span> {hmdt} %</p>
                        <p><span class="highlight">Wind Speed:</span> {wind_spd} km/h</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please enter the required details to get the weather information.")
