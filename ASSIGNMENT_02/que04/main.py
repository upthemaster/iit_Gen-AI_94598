import requests

api_key = "1a8d2da4ea7eb8ae80674a5d44f40a0f"
city = input("Enter City: ")

url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)

print("status code:", response.status_code)
data = response.json()

print("Weather Description:", data["weather"][0]["description"])
print("Temperature:", data["main"]["temp"])
print("Humidity:", data["main"]["humidity"])
print("Wind Speed:", data["wind"]["speed"])

# print("resp data:", data)
