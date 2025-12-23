import time
from langchain.chat_models import init_chat_model
import os
import requests

llm = init_chat_model(
    model= "llama-3.3-70b-versatile",
    model_provider="openai",
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY")

)

def get_weather(city):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return None
    
    return response.json()

while True:
    city = input("Enter city: ")
    if city == "Exit":
        break

    data = get_weather(city)
    if data is None:
        print("City not Found!")
        continue

    temp = data["main"]["temp"]
    humidity = data ["main"]["humidity"]
    wind = data["wind"]["speed"]
    desc = data["weather"][0]["description"]


    llm_input = f"""
        City: {city}
        Temperature : {temp} in Celsius
        Humidity : {humidity} %
        Wind Speed : {wind} m/s
        Description : {desc}

        Instruction: Give explaination in simple english in 7 sentences.

    """

    # result = llm.invoke(llm_input)
    # print(result.content)

    resp = ""

    for chunk in llm.stream(llm_input):
        words = chunk.content.split(" ")
        for word in words:
            print(word + " ", end="", flush=True)
        resp += chunk.content
        time.sleep(0.05)

    break
    