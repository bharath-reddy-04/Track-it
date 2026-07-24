import requests

url = "https://api.themoviedb.org/3/movie/popular"

params = {
    "api_key": "9b9907bb78eb3efdb412f8e58607c15c"
}

response = requests.get(url, params=params)
print(response.json())