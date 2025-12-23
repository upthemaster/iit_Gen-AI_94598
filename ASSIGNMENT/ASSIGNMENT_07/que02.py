import streamlit as st
import time
from langchain.chat_models import init_chat_model
import os
import requests

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )
    response = requests.get(url)

    if response.status_code != 200:
        return None

    return response.json()

st.title("Weather Explanation Assistant")

city = st.text_input("Enter city name")

if st.button("Get Weather Explanation") and city:

    data = get_weather(city)
    if data is None:
        st.error("City not found!")
    else:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        desc = data["weather"][0]["description"]

        llm_input = f"""
        City: {city}
        Temperature : {temp} in Celsius
        Humidity : {humidity} %
        Wind Speed : {wind} m/s
        Description : {desc}

        Instruction: Give explanation in simple English in 7 sentences.
        """

        st.subheader("AI Explanation")

        output_box = st.empty()
        final_text = ""

        for chunk in llm.stream(llm_input):
            final_text += chunk.content
            output_box.write(final_text)
            time.sleep(0.05)
