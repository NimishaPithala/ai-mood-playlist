import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

#spotify access

def get_access_token():
    response = requests.post(
        TOKEN_URL,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET)
    )
    response.raise_for_status()
    token = response.json()["access_token"]
    return token

#search tracks by genre
def search_tracks_by_genre(genre, limit=5):
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": f"genre:{genre}", "type": "track", "limit": limit}
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    response.raise_for_status()

    items = response.json()["tracks"]["items"]
    tracks = [
        {"title": item["name"], "artist": item["artists"][0]["name"]}
        for item in items
    ]
    return tracks
