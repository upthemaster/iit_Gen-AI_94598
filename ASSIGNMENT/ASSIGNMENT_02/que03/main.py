import requests
import json

try:
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    print("status code:", response.status_code)
    # print("response text:", response.text)
    data = response.json()
    print("resp data: ", data)

    with open("posts.json", "w") as file:
        json.dump(data, file, indent=4)
        
    print("Data saved to posts.json")

except:
    print("Some error occured.")