import os 
import requests
import json 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {  # header creates HTTP request header dictionary which will sent to API
    "Authorization" : f"Bearer {api_key}", # passes api_key as a security token
    "content-type" : "application/json"  # it requests the data to the server in the json format
}

user_prompt = input("Ask anything...")

req_data = {
    "model" : "llama-3.3-70b-versatile",
    "messages" : [
        {"role" : "user", "content" : user_prompt}
    ],
}

response = requests.post(url, data=json.dumps(req_data), headers=headers) 
print("Status:", response.status_code)
print(response.json()) 