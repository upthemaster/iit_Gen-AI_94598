import streamlit as st
import os 
import requests
import dotenv
from dotenv import load_dotenv

load_dotenv()

# SESSION STATE 
if "page" not in st.session_state:
    st.session_state.page = "login"

# LOGIN PAGE 
if st.session_state.page == "login":
    st.title("Login Form")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == password and username != "":
            st.session_state.page = "weather"
            st.rerun()
        else:
            st.error("Invalid credentials")

# WEATHER PAGE 
elif st.session_state.page == "weather":
    st.title("Weather Page")

    api_key = os.getenv("OPENWEATHER_API_KEY").strip()
    city = st.text_input("Enter City Name")

    if st.button("Get Weather"):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Weather in {city}")
                st.write("Temperature:", data["main"]["temp"], "°C")
                st.write("Humidity:", data["main"]["humidity"], "%")
                st.write("Wind Speed:", data["wind"]["speed"], "m/s")
            else:
                st.error("City not found")
        else:
            st.warning("Please enter city name")

    if st.button("Logout"):
        st.session_state.page = "thanks"
        st.rerun()

elif st.session_state.page == "thanks":
    st.title("Thank You")
    st.success("You have successfully logged out.")
