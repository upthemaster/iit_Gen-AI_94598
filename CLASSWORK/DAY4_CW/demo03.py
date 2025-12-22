import streamlit as st
import requests
import time
import os
import json
from dotenv import load_dotenv

st.title("My Chatbot")
load_dotenv()

api_key =("dummy_key")
url = "http://127.0.0.1:1234/v1/chat/completions"
headers = {
    "Authorization" : f"Bearer {api_key}",
    "Content-Type" : "application/json"

}

user_prompt = st.chat_input("Ask anything...")
if user_prompt :
    req_data = {
        "model" : "google/gemma-3n-e4b-it",
        "messages" : [
            {"role" : "user", "content" : user_prompt}

        ],
        
    }
    time1 = time.perf_counter()
    response = requests.post(url, data=json.dumps(req_data), headers=headers)
    time2 = time.perf_counter()
    resp = response.json()
    print("Status:", response.status_code)
    st.write(resp["choices"][0]["message"]["content"])
    
